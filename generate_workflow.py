import openai
import yaml

# Set your OpenAI API key
openai.api_key = 'sk-proj-48G4jIgkHlQlXA0hhuXwT3BlbkFJjoeC77Q6uurs4LpWc86M'

def get_user_input(prompt):
    return input(prompt + '\n')

def generate_workflow_config():
    source = get_user_input("Enter the source:")
    source_config = get_user_input("Enter the source configuration:")
    analyzer = get_user_input("Enter the analyzer:")
    analyzer_config = get_user_input("Enter the analyzer configuration:")
    sink = get_user_input("Enter the sink:")
    sink_config = get_user_input("Enter the sink configuration:")

    workflow_config = {
        "analyzer": {
            "_target_": analyzer,
            "device": "auto",
            "model_name_or_path": analyzer_config
        },
        "analyzer_config": {
            "_target_": analyzer + "Config",
            "labels": [],  # You can prompt the user to provide labels if needed
            "multi_class_classification": True,
            "use_splitter_and_aggregator": True,
            "splitter_config": {
                "_target_": "pragman.preprocessor.text_splitter.TextSplitterConfig",
                "max_split_length": 300,
                "split_stride": 10
            },
            "aggregator_config": {
                "_target_": "pragman.postprocessor.inference_aggregator.InferenceAggregatorConfig",
                "aggregate_function": {
                    "_target_": "pragman.postprocessor.inference_aggregator_function.ClassificationAverageScore",
                    "score_threshold": 0.4
                }
            }
        },
        "sink": {
            "_target_": sink,
            "sink_config": {
                "_target_": sink + "Config"
            }
        },
        "source": {
            "_target_": source,
            "source_config": {
                "_target_": source + "Config",
                "fetch_article": True,
                "lookup_period": "1d",
                "max_results": "3",
                "query": source_config
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
    workflow_config = generate_workflow_config()
    execute_workflow(workflow_config)
    print("Workflow executed successfully.")

if __name__ == "__main__":
    main()
