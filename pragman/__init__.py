import logging

from pragman._version import __version__

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)

init_logger: logging.Logger = logging.getLogger(__name__)

installation_message: str = """ Run the venv for all imports"""

init_logger.warning(installation_message)
