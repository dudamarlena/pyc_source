# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\serialization.py
# Compiled at: 2015-12-23 07:43:25
# Size of source mod 2**32: 1799 bytes
"""
Implements the data models used throughout the SDK.
"""
import json
from coralogix import CORALOGIX_ENCODING

class Serializable(object):
    __doc__ = 'Provides a serialization interface to subclasses.'

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