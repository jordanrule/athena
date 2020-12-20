from functools import wraps
from athena.helpers.structure import write_message

LOCAL = 'local'


def validate(func):
    @wraps(func)
    def generate_testcase(input_state):
        output_state = func(input_state)

        if input_state.config.Var.ENVIRONMENT == LOCAL:
            write_message(input_state.generate_payload(config=True, compress=False),
                          'tests/input/%s/%s/%s/' %
                          (func.__module__,
                           func.__qualname__,
                           input_state.config.Var.FREEZE_PATH))

        if input_state.config.Var.ENVIRONMENT in [LOCAL, TEST]:
            write_message(output_state.generate_payload(config=True, compress=False),
                          'tests/output/%s/%s/%s/' %
                          (func.__module__,
                           func.__qualname__,
                           input_state.config.Var.FREEZE_PATH))

        return output_state
    return generate_testcase
