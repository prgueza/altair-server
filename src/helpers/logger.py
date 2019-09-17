import logging
import sys


def init_logger():
    """
    Logger default configuration for outputting info leve logs to the console with a log-like format.
    """
    log_formatter = logging.Formatter('%(asctime)s [  %(threadName)-12.12s] [ %(levelname)-5.5s] %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
