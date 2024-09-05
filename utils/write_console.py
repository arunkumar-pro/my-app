import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os


class Logger:
    def __init__(self, log_dir='/home/dell/Desktop/arun-app/logs', log_level=logging.INFO):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Define the log file path with a unique timestamp
        log_file = os.path.join(log_dir, f'arun_{current_time}.log')

        # Create the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Define the RotatingFileHandler
        handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        handler.setLevel(log_level)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger (only if it's not already added)
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

