from importlib import import_module
import unittest
import os
import logging

from athena.helpers.structure import read_message
from athena.exec import execute_message
from athena.state import State

logger = logging.getLogger(__name__)

STATE = 'state'


class Validation:
    """
    Validation can be imported to automatically validate all functions that have automatically
    generated inputs and outputs, for example:

    class TestExample(Validation.ValidateAll):
        pass
    """
    class ValidateAll(unittest.TestCase):
        def validate(self):
            if os.path.exists('tests/input'):
                for module_name in os.listdir('tests/input'):
                    module = import_module(module_name)

                    for function_name in os.listdir('tests/input/%s' % module_name):
                        func_names = function_name.split('.')
                        func = module.__dict__[func_names[0]]

                        for func_name in func_names[1:]:
                            func = getattr(func, func_name)

                        for case in os.listdir('tests/input/%s/%s' % (module_name, function_name)):
                            message_input = read_message('tests/input/%s/%s/%s/' % (module_name, function_name, case))

                            func = getattr(func, '__wrapped__', func)
                            state = getattr(func, '__annotations__', {}).get(STATE, State)
                            message_actual = execute_message(func,
                                                             state,
                                                             message_input).to_message(config=True)
                            message_expected = read_message('tests/output/%s/%s/%s/' % (module_name, function_name, case))
                            self.assertEquals(sorted(message_expected), sorted(message_actual),
                                              '%s/%s/%s case failed.' % (module_name, function_name, case))
