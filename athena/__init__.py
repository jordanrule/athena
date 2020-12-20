import logging
import sys
import os
from enum import Enum


class LOG(Enum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG


INFO = 'info'
LEVEL = 'LOG_LEVEL'
LOG_LEVEL = str(os.getenv(LEVEL, INFO)).upper()


class ENVIRONMENT(Enum):
    DEV = 'dev'
    QA = 'qa'
    PROD = 'prod'
    LOCAL = 'local'
    TEST = 'test'


LOCAL = 'LOCAL'
ENVIRON = 'ENVIRONMENT'
ENV = os.getenv(ENVIRON, ENVIRONMENT[LOCAL])

# set a root logger on WARNING level
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)-8s] [%(name)s:%(lineno)d] %(message)s',
    stream=sys.stderr)


# use this function to initialize e.g. `logger = get_logger(__name__)`
def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(LOG[LOG_LEVEL].value)
    return logger
