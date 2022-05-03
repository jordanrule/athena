from functools import wraps
from athena.helpers.structure import write_message

LOCAL = 'local'


def validate(func):
    """
    The validate decorator will automatically generate validation test cases to be run via Python
    unittest as defined within athena.test.  Note that validate expects that these functions
    are static and receive and produce a State (or State generator).
    """
    @wraps(func)
    def generate_testcase(input_state):
        output_state = func(input_state)

        if input_state.environment.Init.ENV == LOCAL:
            write_message(input_state.to_message(environment=True),
                          'tests/input/%s/%s/%s/' %
                          (func.__module__,
                           func.__qualname__,
                           input_state.environment.Init.VALIDATE_PATH))

        if input_state.environment.Init.ENV == LOCAL:
            write_message(output_state.to_message(environment=True),
                          'tests/output/%s/%s/%s/' %
                          (func.__module__,
                           func.__qualname__,
                           input_state.environment.Init.VALIDATE_PATH))

        return output_state
    return generate_testcase
