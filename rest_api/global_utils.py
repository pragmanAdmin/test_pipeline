import logging
from typing import Dict

from fastapi import APIRouter, FastAPI, HTTPException
from flask import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from pragman.sink.base_sink import BaseSink
from pragman.sink.dailyget_sink import DailyGetSink
from pragman.sink.elasticsearch_sink import ElasticSearchSink
from pragman.sink.http_sink import HttpSink
from pragman.sink.jira_sink import JiraSink
from pragman.sink.logger_sink import LoggerSink
from pragman.sink.slack_sink import SlackSink
from pragman.sink.zendesk_sink import ZendeskCredInfo
from pragman.source.appstore_scrapper import AppStoreScrapperSource
from pragman.source.base_source import BaseSource
from pragman.source.email_source import EmailSource
from pragman.source.playstore_reiews import PlayStoreSource
from pragman.source.playstore_scrapper import PlayStoreScrapperSource
from pragman.source.reddit_scrapper import RedditScrapperSource
from pragman.source.reddit_source import RedditSource
from pragman.source.twitter_source import TwitterSource

logger = logging.getLogger(__name__)

source_map: Dict[str, BaseSource] = {
    "Twitter": TwitterSource(),
    "PlayStore": PlayStoreSource(),
    "PlayStoreScrapper": PlayStoreScrapperSource(),
    "AppStoreScrapper": AppStoreScrapperSource(),
    "RedditScrapper": RedditScrapperSource(),
    "Reddit": RedditSource(),
    "Email": EmailSource()
}

sink_map: Dict[str, BaseSink] = {
    "Http": HttpSink(),
    "Jira": JiraSink(),
    "DailyGet": DailyGetSink(),
    "Elasticsearch": ElasticSearchSink(),
    "Zendesk": ZendeskCredInfo(),
    "Slack": SlackSink(),
    "Logging": LoggerSink()
}

router = APIRouter()


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


def get_application() -> FastAPI:
    application = FastAPI(
        title="pragman-APIs",
        debug=True,
        description="Observe, Analyze and Inform"
    )

    application.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)

    application.include_router(router)

    return application
