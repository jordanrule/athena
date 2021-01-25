from typing import Dict

from athena import get_logger
from athena.environment import Environment
from athena.helpers.structure import structure, object_to_attributes, object_to_dictionary

logger = get_logger(__name__)

ENVIRONMENT = 'env'


class State:
    """
    State represents the parameterization of a piece of distributed computation.  It utilizes
    the structure decorator to transparently deserialize JSON to a Python object for arbitrary
    transformation, and then serialize the resulting Python object back to JSON for transport
    over a distributed cluster.
    """

    env: Environment

    @structure
    class Init:
        environment: Dict[str, any] = None  # environment can be use to overwrite system environment

    def __init__(self, message: Dict[str, any]):
        object_to_attributes(self, message.get)
        self.env = self.__annotations__[ENVIRONMENT](self.Init.environment)
        self.iter = True  # flag used for iterable subclass

    def to_message(self, environment=False) -> Dict[str, any]:
        message = object_to_dictionary(self)

        if self.env and environment:
            message[ENVIRONMENT] = object_to_dictionary(self.env)

        return message

    def __str__(self):
        return str(self.to_message())

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
