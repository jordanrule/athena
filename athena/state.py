from typing import Dict

from athena import get_logger
from athena.environment import Environment
from athena.helpers.structure import structure, object_to_attributes, object_to_dictionary

logger = get_logger(__name__)

ENVIRONMENT = 'environment'


class State:

    environment: Environment

    @structure
    class Initialization:
        environment: Dict[str, any] = None  # environment can be use to overwrite system environment

    def __init__(self, message: Dict[str, any]):
        object_to_attributes(self, message.get)
        self.environment = self.__annotations__[ENVIRONMENT](self.Initialization.environment)
        self.iter = True  # flag used for iterable subclass

    def to_message(self, environment=False) -> Dict[str, any]:
        message = object_to_dictionary(self)

        if self.environment and environment:
            message[ENVIRONMENT] = object_to_dictionary(self.environment)

        return message

    def __str__(self):
        return self.to_message()

    def __iter__(self):
        return self

    def __next__(self):
        """
        Return self once if iterated upon
        """
        if self.iter:
            self.iter = False
            return self
        raise StopIteration
