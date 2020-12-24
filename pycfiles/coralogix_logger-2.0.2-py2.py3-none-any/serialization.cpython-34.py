# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\serialization.py
# Compiled at: 2015-12-23 07:43:25
# Size of source mod 2**32: 1799 bytes
__doc__ = '\nImplements the data models used throughout the SDK.\n'
import json
from coralogix import CORALOGIX_ENCODING

class Serializable(object):
    """Serializable"""

    def __init__(self, **kwargs):
        """
        Default implementation. Ignores missing attributes and doesn't set any extra attributes (i.e. attributes not in self.__serializable__).
        Can be overridden by subclasses.
        """
        for attr, field in self.__serializable__:
            if attr in kwargs:
                setattr(self, attr, kwargs.pop(attr))
                continue

    def serialize(self):
        field_values = {}
        for attr, field in self.__serializable__:
            if field:
                value = getattr(self, attr)
                if isinstance(value, Serializable):
                    value = value.serialize()
                field_values[field] = value
                continue

        return field_values

    def tojson(self):
        return json.dumps(self.serialize()).encode(CORALOGIX_ENCODING)

    @classmethod
    def deserialize(cls, fields):
        if not hasattr(cls, '__deserializable__'):
            cls.__deserializable__ = dict([(v, k) for v, k in cls.__serializable__])
        init_kwargs = dict([(cls.__deserializable__[field], value) for field, value in fields.items() if field in cls.__deserializable__])
        return cls(**init_kwargs)

    @classmethod
    def fromjson(cls, json_string):
        json_dict = json.loads(json_string.decode(CORALOGIX_ENCODING))
        return cls.deserialize(json_dict)