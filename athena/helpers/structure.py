import os
import json
from typing import Dict

from athena.helpers.exception import EnvironmentException


ATTACH = '__attachments__'
MESSAGE = 'message'


def structure(clz=None):
    """
    The structure decorator provides an interface to create structured data by defining inner data
    classes within a Python object.  It respects Python typing and attribute syntax: object type
    annotations are applied when deserializing JSON, and exceptions are thrown in cases where
    underlying data is not represented and no default value has been provided.  In cases where a
    default value is provided, the data within the structured source will override the underlying
    default if present.
    """
    attachments = []
    # we look at annotations too, since attributes will not exist for required attachments
    for att_name in set(getattr(clz, '__annotations__', ())).union(set(dir(clz)) - set(dir(object))):
        # we don't want to consider class attributes
        if not att_name.startswith('__'):
            attachments.append(att_name)
    setattr(clz, ATTACH, attachments)
    return clz


def cast(obj, value):
    if getattr(obj, '__annotations__', None):
        clazz = obj.__annotations__.get(value)
        if getattr(obj, value, False) is not None:  # don't try to cast a typed None
            if clazz == bool:
                return lambda val: str(val) in ["True", "true", "TRUE", "t", "T", "1"]
            return clazz
    return lambda val: val


def object_to_attributes(obj, retrieve):
    for clz_name in (set(dir(obj)) - set(dir(object))):
        clz = getattr(obj, clz_name)
        if hasattr(clz, ATTACH):
            clz = clz()  # reset attachments from prior runs
            for att_name in getattr(clz, ATTACH):
                value = retrieve(att_name, None)
                if value is None and not hasattr(clz, att_name):
                    exception_message = f"Missing required configuration: '{att_name}'"
                    raise EnvironmentException(exception_message)
                setattr(clz, att_name, cast(clz, att_name)(value or getattr(clz, att_name, None)))
            setattr(obj, clz_name, clz)


def object_to_dictionary(obj) -> Dict[str, any]:
    message = {}
    for clz_name in (set(dir(obj)) - set(dir(object))):
        clz = getattr(obj, clz_name)
        if hasattr(clz, ATTACH):
            for att_name in getattr(clz, ATTACH):
                attribute = getattr(clz, att_name, None)
                if attribute:
                    message[att_name] = attribute
    return message


def read_message(path=''):
    if os.path.exists('%smessage.json' % path):
        with open('%smessage.json' % path) as input_message:
            message = json.loads(input_message.read())
            return message

    return {}


def write_message(message: Dict[str, any], path=''):
    if not os.path.exists(path):
        os.makedirs(path)

    if len(message) > 0:
        with open('%smessage.json' % path, 'w') as file:
            file.write(json.dumps(message))
