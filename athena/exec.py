from athena import get_logger
from athena import ENVIRONMENT, ENV
from athena.helpers.structure import read_message
from athena.state import State

logger = get_logger(__name__)


STATE = 'state'
MAIN = 'main'


def run(func):
    func = getattr(func, MAIN, func)
    wrapped = getattr(func, '__wrapped__', func)
    state = getattr(wrapped, '__annotations__', {}).get(STATE, State)

    if ENV == ENVIRONMENT.LOCAL:
        for output_state in execute_message(func, state, read_message()):
            logger.info(output_state)


def execute_message(func, state, message):
    return func(state(message))
