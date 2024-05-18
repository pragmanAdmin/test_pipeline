import openai
import yaml

# Set your OpenAI API key
openai.api_key = 'sk-proj-48G4jIgkHlQlXA0hhuXwT3BlbkFJjoeC77Q6uurs4LpWc86M'

def get_user_input(prompt):
    return input(prompt + '\n')

def generate_workflow_config(source_target, analyzer_target, sink_target, query):
    # Mapping from target names to actual module paths for sources, analyzers, and sinks
    source_mapping = {
        "appstore_scrapper": "pragman.source.appstore_scrapper.AppStoreScrapperSource",
        "base_source": "pragman.source.base_source.BaseSource",
        "email_source": "pragman.source.email_source.EmailSource",
        "facebook_source": "pragman.source.facebook_source.FacebookSource",
        "google_maps_reviews": "pragman.source.google_maps_reviews.GoogleMapsReviewsSource",
        "google_news_source": "pragman.source.google_news_source.GoogleNewsSource",
        "pandas_source": "pragman.source.pandas_source.PandasSource",
        "playstore_reiews": "pragman.source.playstore_reiews.PlaystoreReviewsSource",
        "playstore_scrapper": "pragman.source.playstore_scrapper.PlaystoreScrapperSource",
        "reddit_scrapper": "pragman.source.reddit_scrapper.RedditScrapperSource",
        "reddit_source": "pragman.source.reddit_source.RedditSource",
        "twitter_source": "pragman.source.twitter_source.TwitterSource",
        "website_crawler_source": "pragman.source.website_crawler_source.WebsiteCrawlerSource",
        "youtube_reviews": "pragman.source.youtube_reviews.YoutubeReviewsSource",
        "youtube_scrapper": "pragman.source.youtube_scrapper.YoutubeScrapperSource",
    }

    analyzer_mapping = {
        "base_analyzer": "pragman.analyzer.base_analyzer.BaseAnalyzer",
        "classification_analyzer": "pragman.analyzer.classification_analyzer.ClassificationAnalyzer",
        "dummy_analyzer": "pragman.analyzer.dummy_analyzer.DummyAnalyzer",
        "ner_analyzer": "pragman.analyzer.ner_analyzer.NerAnalyzer",
        "pii_analyzer": "pragman.analyzer.pii_analyzer.PiiAnalyzer",
        "sentiment_analyzer": "pragman.analyzer.sentiment_analyzer.SentimentAnalyzer",
        "translation_analyzer": "pragman.analyzer.translation_analyzer.TranslationAnalyzer",
    }

    sink_mapping = {
        "base_sink": "pragman.sink.base_sink.BaseSink",
        "dailyget_sink": "pragman.sink.dailyget_sink.DailygetSink",
        "elasticsearch_sink": "pragman.sink.elasticsearch_sink.ElasticsearchSink",
        "http_sink": "pragman.sink.http_sink.HttpSink",
        "jira_sink": "pragman.sink.jira_sink.JiraSink",
        "logger_sink": "pragman.sink.logger_sink.LoggerSink",
        "pandas_sink": "pragman.sink.pandas_sink.PandasSink",
        "slack_sink": "pragman.sink.slack_sink.SlackSink",
        "zendesk_sink": "pragman.sink.zendesk_sink.ZendeskSink",
    }

    workflow_config = {
        "analyzer": {
            "_target_": analyzer_mapping.get(analyzer_target),
            # Add other configuration parameters for the selected analyzer if needed
        },
        "sink": {
            "_target_": sink_mapping.get(sink_target),
            # Add other configuration parameters for the selected sink if needed
        },
        "source": {
            "_target_": source_mapping.get(source_target),
            # Add other configuration parameters for the selected source if needed
            "source_config": {
                "_target_": source_mapping.get(source_target) + "Config",
                # Add source-specific configuration parameters here
                "fetch_article": True,  # Example configuration parameter
                "lookup_period": "1d",  # Example configuration parameter
                "max_results": "3",  # Example configuration parameter
                "query": query
            }
        }
    }

    return workflow_config

def execute_workflow(workflow_config):
    # Convert the workflow config to YAML format
    workflow_yaml = yaml.dump(workflow_config)
    
    # Call the OpenAI API to execute the workflow
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=workflow_yaml,
        temperature=0,
        max_tokens=1000,
        n=1,
        stop=["C:"]
    )
    
    # Extract the generated workflow code from the API response
    generated_code = response.choices[0].text.strip()
    
    # Execute the generated code
    exec(generated_code)

    return generated_code

def main():
    source_target = get_user_input("Enter the source target:")
    analyzer_target = get_user_input("Enter the analyzer target:")
    sink_target = get_user_input("Enter the sink target:")
    query = get_user_input("Enter the query:")
    
    workflow_config = generate_workflow_config(source_target, analyzer_target, sink_target, query)
    execute_workflow(workflow_config)
    print("Workflow executed successfully.")

if __name__ == "__main__":
    main()
