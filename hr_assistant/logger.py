"""
Shared logger module used by every other module in the project. 

Log structure:

logs/
    date-month/
        run_2026-10-04_15-30-20.log
        run_2026-10-04_16-45-10.log

    date-month/
        run_2026-10-05_09-20-15.log

This module is responsible for logging messages to the console and to a log file. 
It is configured to log messages at the DEBUG level and above.

Every module in this project should import this logger and use it for logging messages. 
This ensures that all log messages are consistent and can be easily managed.
"""


import logging
import os
from datetime import datetime

# ============================================================
# LOG DIRECTORY
# ============================================================
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ============================================================
# APPLICATION RUN TIME
# ============================================================
_run_started_at = datetime.now()

# ============================================================
# DATE FOLDER
# ============================================================
_date_folder = _run_started_at.strftime("%d-%b")
DATE_LOG_DIR = os.path.join(LOG_DIR, _date_folder)
os.makedirs(DATE_LOG_DIR, exist_ok=True)


# ============================================================
# LOG FILE
# ============================================================
_run_timestamp = _run_started_at.strftime("%Y-%m-%d_%H-%M-%S")
RUN_LOG_FILE = os.path.join(DATE_LOG_DIR, f"run_{_run_timestamp}.log")


# ============================================================
# LOGGING CONFIGURATION
# ============================================================
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s -| %(message)s",
    handlers=[
        logging.FileHandler(RUN_LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ],
)


# ============================================================
# LOGGER FACTORY
# ============================================================
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A logger instance.
    """
    return logging.getLogger(name)