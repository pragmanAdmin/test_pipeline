import logging
import os
from typing import List

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.base import BaseScheduler
from fastapi import FastAPI, HTTPException, Body

from pragman.configuration import pragmanConfiguration
from pragman.processor import Processor
from pragman.analyzer.base_analyzer import BaseAnalyzerConfig, BaseAnalyzer
from rest_api.api_request_response import ScheduleResponse, WorkflowAddResponse, ClassifierRequest, ClassifierResponse
from pragman.workflow.workflow import WorkflowConfig, Workflow
from rest_api.global_utils import get_application, sink_map, source_map
from rest_api.rate_limiter import RequestLimiter
from pragman.workflow.store import WorkflowStore

logger = logging.getLogger(__name__)

pragman_config: pragmanConfiguration

workflow_store: WorkflowStore
scheduler: BaseScheduler
analyzer: BaseAnalyzer
processor: Processor
rate_limiter: RequestLimiter

app = get_application()

def process_scheduled_job(workflow: Workflow):
    try:
        if workflow:
            processor.process(
                workflow=workflow,
                sink=sink_map[workflow.config.sink_config.TYPE],
                source=source_map[workflow.config.source_config.TYPE],
            )
    except Exception as ex:
        logger.error(f'Exception occur: {ex}')

def schedule_workflows():
    workflows = workflow_store.get_all()
    jobs = []
    for workflow in workflows:
        jobs.append(
            scheduler.add_job(
                func=process_scheduled_job,
                kwargs={"workflow": workflow},
                trigger='interval',
                seconds=workflow.config.time_in_seconds,
                id=workflow.id,
            )
        )

def scheduler_init():
    global scheduler

    try:
        scheduler = pragman_config.initialize_instance("workflow_scheduler")
        scheduler.start()
        logger.info("Created Schedule Object")
        schedule_workflows()
    except Exception as ex:
        logger.error(f'Unable to Create Schedule Object, error: {ex.__cause__}')
        raise ex

def logging_init():
    log_config = pragman_config.get_logging_config()

    logging.basicConfig(**log_config["base_config"])

    logging.root.setLevel(log_config["base_config"]["level"])
    logging.root.propagate = True

    gunicorn_logger = logging.getLogger('gunicorn.error')
    gunicorn_logger.setLevel(log_config["base_config"]["level"])
    gunicorn_logger.propagate = True

def init_workflow_store():
    global workflow_store
    workflow_store = pragman_config.initialize_instance("workflow_store")

def init_analyzer():
    global analyzer
    analyzer = pragman_config.initialize_instance("analyzer")

def init_processor():
    global processor
    global analyzer
    # TODO generalize it, so based on analyzer config it initialise
    processor = Processor(analyzer=analyzer)

def init_rate_limiter():
    global rate_limiter
    rate_limiter = pragman_config.initialize_instance("rate_limiter")

def config_init() -> None:
    global pragman_config
    pragman_config = pragmanConfiguration(
        config_path=os.getenv('pragman_CONFIG_PATH', "../config"),
        config_filename=os.getenv('pragman_CONFIG_FILENAME', "rest.yaml")
    )

@app.on_event("startup")
def app_init():
    config_init()
    logging_init()
    init_analyzer()
    init_processor()
    init_workflow_store()
    scheduler_init()
    init_rate_limiter()

    logger.info("Open http://127.0.0.1:9898/redoc or http://127.0.0.1:9898/docs to see API Documentation.")

@app.get(
    "/workflows/schedules/",
    response_model=List[ScheduleResponse],
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def get_scheduled_syncs():
    global rate_limiter
    global scheduler
    with rate_limiter.run():
        schedules = []
        for job in scheduler.get_jobs():
            schedules.append(
                ScheduleResponse(
                    id=str(job.id),
                    run_frequency=str(job.trigger),
                    next_run=str(job.next_run_time)
                )
            )
        return schedules

@app.get(
    "/workflows/",
    response_model=List[Workflow],
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def get_all_workflows():
    global rate_limiter
    global workflow_store
    with rate_limiter.run():
        return workflow_store.get_all()

@app.get(
    "/workflows/{workflow_id}",
    response_model=Workflow,
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def get_workflow(workflow_id: str):
    global rate_limiter
    global workflow_store
    with rate_limiter.run():
        return workflow_store.get(workflow_id)

@app.delete(
    "/workflows/{workflow_id}",
    response_model=WorkflowAddResponse,
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def delete_workflow(workflow_id: str):
    global rate_limiter
    global workflow_store
    global scheduler
    with rate_limiter.run():
        try:
            scheduler.remove_job(job_id=workflow_id)
        except JobLookupError as ex:
            logger.warning(f'Workflow {workflow_id} not found. Error: {ex.__cause__}')

        try:
            workflow_store.delete_workflow(workflow_id)
        except Exception as ex:
            logger.warning(f'Workflow {workflow_id} not able to delete. Error: {ex.__cause__}')
            raise HTTPException(
                status_code=404,
                detail=f'Workflow {workflow_id} not found'
            )

        return WorkflowAddResponse(id=workflow_id)

@app.post(
    "/workflows/{workflow_id}",
    response_model=WorkflowAddResponse,
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def update_workflow(workflow_id: str, request: WorkflowConfig):
    global rate_limiter
    global workflow_store
    global scheduler
    with rate_limiter.run():
        try:
            scheduler.remove_job(job_id=workflow_id)
        except JobLookupError as ex:
            logger.warning(f'Job {workflow_id} not found. Error: {ex.__cause__}')

        workflow_detail = Workflow(id=workflow_id, config=request)
        workflow_store.update_workflow(workflow_detail)
        scheduler.add_job(
            func=process_scheduled_job,
            kwargs={"workflow": workflow_detail},
            trigger='interval',
            seconds=workflow_detail.config.time_in_seconds,
            id=workflow_detail.id,
        )

        return WorkflowAddResponse(id=workflow_detail.id)

@app.post(
    "/workflows/",
    response_model=WorkflowAddResponse,
    response_model_exclude_unset=True,
    tags=["workflow"]
)
async def add_workflow(request: WorkflowConfig):
    global rate_limiter
    global workflow_store
    global scheduler
    with rate_limiter.run():
        workflow_detail = Workflow(config=request)
        workflow_store.add_workflow(workflow_detail)
        scheduler.add_job(
            func=process_scheduled_job,
            kwargs={"workflow": workflow_detail},
            trigger='interval',
            seconds=workflow_detail.config.time_in_seconds,
            id=workflow_detail.id,
        )

        return WorkflowAddResponse(id=workflow_detail.id)

@app.post(
    "/classifier",
    response_model=ClassifierResponse,
    response_model_exclude_unset=True,
    tags=["api"]
)
def classify_texts(request: ClassifierRequest):
    global rate_limiter
    global analyzer
    with rate_limiter.run():
        analyzer_requests: List[BaseAnalyzer] = [
            BaseAnalyzer(
                processed_text=text,
                source_name="API"
            )
            for text in request.texts
        ]
        analyzer_responses = analyzer.analyze_input(
            source_response_list=analyzer_requests,
            analyzer_config=request.analyzer_config,
        )

        response = []
        for analyzer_response in analyzer_responses:
            response.append(analyzer_response.segmented_data)

        return ClassifierResponse(data=response)

@app.post(
    "/create_report",
    response_model=WorkflowAddResponse,
    response_model_exclude_unset=True,
    tags=["report"]
)
async def create_report(
    source: str = Body(...),
    analyzer: str = Body(...),
    sink: str = Body(...),
    config: dict = Body(...)
):
    global rate_limiter
    global workflow_store
    global scheduler
    with rate_limiter.run():
        # Create a new WorkflowConfig based on the provided configurations
        workflow_config = WorkflowConfig(
            source_config={"TYPE": source, **config['source']},
            analyzer_config={"TYPE": analyzer, **config['analyzer']},
            sink_config={"TYPE": sink, **config['sink']},
            time_in_seconds=3600  # Example value, adjust as needed
        )
        
        workflow_detail = Workflow(config=workflow_config)
        workflow_store.add_workflow(workflow_detail)
        
        scheduler.add_job(
            func=process_scheduled_job,
            kwargs={"workflow": workflow_detail},
            trigger='interval',
            seconds=workflow_detail.config.time_in_seconds,
            id=workflow_detail.id,
        )
        
        return WorkflowAddResponse(id=workflow_detail.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9898)
