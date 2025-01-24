import logging
import os

LOG_FILE_NAME = 'autosave.log'
LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOG_FILE_NAME)
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO

_logger_initialized = False

def setup_logger():
    global _logger_initialized
    if not _logger_initialized:
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE_PATH, filemode='a')
        _logger_initialized = True