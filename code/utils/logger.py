from colorlog import ColoredFormatter
import logging

TIMESTAMP_FORMAT = '%(cyan)s%(asctime)s%(reset)s'
NAME_FORMAT = '%(blue)s%(name)s%(reset)s'
LEVEL_FORMAT = '%(log_color)s%(levelname)s%(reset)s'
MESSAGE_FORMAT = '%(message)s'

LOG_FORMAT = f'[{TIMESTAMP_FORMAT}][{NAME_FORMAT}][{LEVEL_FORMAT}] - {MESSAGE_FORMAT}'
LOG_COLORS = {
    "DEBUG": "purple",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red",
}


def create_colorlog_logger(fmt: str = LOG_FORMAT, name: str = "COLORLOG", level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a logger with a custom formatter.
    :param fmt: format of the logger. Default is LOG_FORMAT.
    :type fmt: str
    :param name: name of the logger.
    :type name: str
    :param level: level of the logger. Default is logging.DEBUG.
    :type level: int
    :return: the created logger.
    :rtype: logging.Logger
    """
    stream = logging.StreamHandler()
    stream.setLevel(level)
    stream.setFormatter(ColoredFormatter(fmt=fmt, log_colors=LOG_COLORS))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(stream)
    return logger