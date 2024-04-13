import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    ".github/workflows/.gitkeep",
    f"pragman/analyzer/__init__.py",
    f"pragman/analyzer/base_analyzer.py",
    f"pragman/analyzer/classification_analyzer.py",
    f"pragman/analyzer/dummy_analyzer.py",
    f"pragman/analyzer/ner_analyzer.py",
    f"pragman/analyzer/pii_analyzer.py",
    f"pragman/analyzer/sentiment_analyzer.py",
    f"pragman/analyzer/translation_analyzer.py",
    f"pragman/misc/__init__.py",
    f"pragman/misc/gpu_util.py",
    f"pragman/misc/utils.py",
    f"pragman/misc/web_search.py",
    f"pragman/misc/youtube_reviews_scrapper.py",
    f"pragman/postprocessor/__init__.py",
    f"pragman/postprocessor/base_postprocessor.py",
    f"pragman/postprocessor/inference_aggregator_function.py",
    f"pragman/postprocessor/inference_aggregator.py",
    f"pragman/preprocessor/__init__.py",
    f"pragman/preprocessor/base_preprocessor.py",
    f"pragman/preprocessor/text_cleaner.py",
    f"pragman/preprocessor/text_cleaning_function.py",
    f"pragman/preprocessor/text_splitter.py",
    f"pragman/preprocessor/text_tokenizer.py",
    f"pragman/sink/__init__.py",
    f"pragman/sink/base_sink.py",
    f"pragman/sink/dailyget_sink.py",
    f"pragman/sink/elasticsearch_sink.py",
    f"pragman/sink/http_sink.py",
    f"pragman/sink/jira_sink.py",
    f"pragman/sink/logger_sink.py",
    f"pragman/sink/pandas_sink.py",
    f"pragman/sink/slack_sink.py",
    f"pragman/sink/zendesk_sink.py",
    f"pragman/source/__init__.py",
    f"pragman/source/appstore_scrapper.py",
    f"pragman/source/base_source.py",
    f"pragman/source/email_source.py",
    f"pragman/source/facebook_source.py",
    f"pragman/source/google_maps_reviews.py",
    f"pragman/source/google_news_source.py",
    f"pragman/source/pandas_source.py",
    f"pragman/source/playstore_reiews.py",
    f"pragman/source/playstore_scrapper.py",
    f"pragman/source/reddit_scrapper.py",
    f"pragman/source/reddit_source.py",
    f"pragman/source/twitter_source.py",
    f"pragman/source/website_crawler_source.py",
    f"pragman/source/youtube_reviews.py",
    f"pragman/source/youtube_scrapper.py",
    f"pragman/workflow/__init__.py",
    f"pragman/workflow/base_store.py",
    f"pragman/workflow/store.py",
    f"pragman/workflow/workflow.py",
    f"pragman/__init__.py",
    f"pragman/_version.py",
    f"pragman/configuration.py",
    f"pragman/payload.py",
    f"pragman/process_workflow.py",
    f"pragman/processor.py"    
]


# Code to Run the all the above created file structure

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
            
    else:
        logging.info(f"{filename} is already exists")