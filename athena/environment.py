import os
from typing import Dict

from athena.helpers.structure import structure, object_to_attributes
from athena import ENV

BASE = 'base'


class Environment:
    """
    Environment represents variables as they are defined within the running container.

    In cases where a specific environment wants to be represented by the user, for example
    during validation or to override container definitions, the "environment" key can be utilized
    within the JSON representation of the State.
    """

    @structure
    class Init:
        ENV: str = ENV  # environment is used to determine deployed environment
        VALIDATE_PATH: str = BASE  # validate path is used to serialize @validate to disk

    def __init__(self, environment: Dict[str, any] = None):
        if environment:
            object_to_attributes(self, environment.get)
        else:
            object_to_attributes(self, os.getenv)

        self.init = True

    def __setattr__(self, name, value):
        """
        Disallow setting attributes to values other than represented in environment.
        """
        if not hasattr(self, 'init'):
            super().__setattr__(name, value)
