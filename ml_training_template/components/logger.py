import logging
import os
import traceback
from logging.config import dictConfig
from pathlib import Path

import yaml


def setup_logging():
    """
    This function can be invoked in order to setup logging based on a yaml config in the
    root dir of this project
    """
    try:
        default_log_config = Path(__file__).parent.parent / "logging.yaml"
        with open(
            os.environ.get(
                "LOGGING_CONFIG", default_log_config
            ),
            "rt",
        ) as f:
            config = yaml.safe_load(f.read())
        dictConfig(config)
    except Exception:
        print("Error in Logging Configuration. Using default configs")
        print(traceback.format_exc())
        logging.basicConfig(level=logging.INFO)
