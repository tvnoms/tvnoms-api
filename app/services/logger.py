import logging
import os
import sys
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    if getattr(logger, '_tvnoms_configured', False):
        return logger

    log_level = os.getenv('TVNOMS_LOG_LEVEL', 'INFO').upper()
    log_file = os.getenv('TVNOMS_LOG_FILE', '/tmp/tvnoms.log')

    formatter = logging.Formatter(
        fmt='%(levelname)s %(asctime)s [%(name)s] %(message)s'
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file)
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.setLevel(log_level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger._tvnoms_configured = True
    return logger
