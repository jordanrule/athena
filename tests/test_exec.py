from unittest import TestCase
from athena.exec import execute_message
from athena.state import State


class TestExec(TestCase):
    def setUp(self):
        pass

    def test_execute_message(self):
        """
        Test that execute_message generates expected output message
        """
        func = lambda x: x.environment.Init.ENV
        message = {'environment': {'ENV': 'NOSE'}}
        self.assertEquals(execute_message(func, State, message), 'NOSE')
