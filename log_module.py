import os
import logging
from logging.handlers import RotatingFileHandler

def init_logger(logger_name, file_name, log_directory='logs', max_log_size=5*1024*1024, backup_count=1):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger(logger_name)
    handler = RotatingFileHandler(os.path.join(log_directory, file_name), 
                                  maxBytes=max_log_size, backupCount=backup_count)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
