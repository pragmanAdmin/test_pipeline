from typing import Dict, List

from pydantic.main import BaseModel

from pragman.analyzer.base_analyzer import BaseAnalyzerConfig
from pragman.analyzer.classification_analyzer import ClassificationAnalyzerConfig


class ClassifierRequest(BaseModel):
    texts: List[str]
    analyzer_config: BaseAnalyzerConfig

    class Config:
        arbitrary_types_allowed = True


class ClassifierResponse(BaseModel):
    data: List[Dict[str, float]]


class ScheduleResponse(BaseModel):
    id: str
    run_frequency: str
    next_run: str

    class Config:
        arbitrary_types_allowed = True


class WorkflowAddResponse(BaseModel):
    id: str
