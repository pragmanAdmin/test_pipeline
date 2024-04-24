import base64
import logging
import pathlib
import re
import sys
import uuid
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def img_to_bytes(img_path):
    img_bytes = pathlib.Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def download_button(
    object_to_download, download_filename, button_text  # , pickle_it=False
):
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    dl_link = (
        f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
    )
    return dl_link


def get_pragman_config(current_path, file_name):
    return pragmanConfiguration(
        config_path=current_path,
        config_filename=file_name,
    ).configuration


def get_icon_name(name, icon, icon_size=40, font_size=1):
    if not name:
        return f'<img style="vertical-align:middle;margin:5px 5px" src="{icon}" width="{icon_size}" height="{icon_size}">'
    return (
        f'<p style="font-size:{font_size}px">'
        f'<img style="vertical-align:middle;margin:1px 5px" src="{icon}" width="{icon_size}" height="{icon_size}">'
        f"{name}</p>"
    )


def render_config(config, component, help_str=None, parent_key=None):
    if config is None:
        return

    prefix = "" if parent_key is None else f"{parent_key}."
    if help_str is not None:
        # Flask/Django alternative for expander
        pass

    for k, v in config.items():
        if k == "_target_":
            continue

        if isinstance(v, dict):
            render_config(v, component, None, k)
        elif isinstance(v, list):
            if len(v) == 0:
                continue
            is_object = isinstance(v[0], dict)
            if is_object:
                for idx, sub_element in enumerate(v):
                    render_config(sub_element, component, None, f"{k}[{idx}]")
            else:
                # Flask/Django alternative for text_area
                pass
        elif isinstance(v, bool):
            # Flask/Django alternative for radio
            pass
        else:
            tokens = k.split("_")
            is_secret = tokens[-1] in ["key", "password", "token", "secret"]
            # Flask/Django alternative for text_input
            pass


def generate_python(generate_config):
    return f"""
from pragman.configuration import pragmanConfiguration

# This is pragman workflow path and filename
config_path = "./"
config_filename = "workflow.yml"

# Extract config via yaml file using `config_path` and `config_filename`
pragman_configuration = pragmanConfiguration(config_path=config_path, config_filename=config_filename)

# Initialize objects using configuration
source_config = pragman_configuration.initialize_instance("source_config")
source = pragman_configuration.initialize_instance("source")
analyzer = pragman_configuration.initialize_instance("analyzer")
analyzer_config = pragman_configuration.initialize_instance("analyzer_config")
sink_config = pragman_configuration.initialize_instance("sink_config")
sink = pragman_configuration.initialize_instance("sink")

# This will fetch information from configured source ie twitter, app store etc
source_response_list = source.lookup(source_config)

# This will execute analyzer (Sentiment, classification etc) on source data with provided analyzer_config
# Analyzer will it's output to `segmented_data` inside `analyzer_response`
analyzer_response_list = analyzer.analyze_input(
    source_response_list=source_response_list,
    analyzer_config=analyzer_config
)

# This will send analyzed output to configure sink ie Slack, Zendesk etc
sink_response_list = sink.send_data(analyzer_response_list, sink_config)
"""


def generate_yaml(generate_config):
    return yaml.dump(generate_config)


def execute_workflow(generate_config, component=None, log_components=None):
    progress_show = None
    if component:
        # Flask/Django alternative for progress show
        pass
    try:
        pragman_configuration = pragmanConfiguration(configuration=generate_config)

        source_config = pragman_configuration.initialize_instance("source_config")
        source = pragman_configuration.initialize_instance("source")

        analyzer = pragman_configuration.initialize_instance("analyzer")
        analyzer_config = pragman_configuration.initialize_instance("analyzer_config")

        sink_config = pragman_configuration.initialize_instance("sink_config")
        sink = pragman_configuration.initialize_instance("sink")

        source_response_list = source.lookup(source_config)
        log_components["source"].write([vars(response) for response in source_response_list])

        analyzer_response_list = analyzer.analyze_input(
            source_response_list=source_response_list, analyzer_config=analyzer_config
        )
        log_components["analyzer"].write([vars(response) for response in analyzer_response_list])

        sink_response_list = sink.send_data(analyzer_response_list, sink_config)
        if sink.TYPE == 'Pandas':
            log_components["sink"].write(sink_response_list)
        elif sink_response_list is not None:
            log_components["sink"].write([vars(response) for response in sink_response_list])
        else:
            log_components["sink"].write("No Data")

        if progress_show:
            # Flask/Django alternative for processing complete message
            pass
    except Exception as ex:
        if progress_show:
            # Flask/Django alternative for processing failure message
            pass

        raise ex


def handle_source_form_submission(form_data):
    # Process form data for source
    pass


def handle_analyzer_form_submission(form_data):
    # Process form data for analyzer
    pass


def handle_sink_form_submission(form_data):
    # Process form data for sink
    pass


def handle_config_form_submission(form_data):
    # Process form data for config
    pass
