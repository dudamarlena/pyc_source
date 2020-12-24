# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/serialize.py
# Compiled at: 2020-04-12 15:15:49
# Size of source mod 2**32: 1832 bytes
"""JSON Serializer."""
import uuid, ipaddress, datetime, types
from functools import singledispatch

@singledispatch
def serialize(obj):
    """Recursively serialise objects."""
    return obj


@serialize.register(types.FunctionType)
@serialize.register(types.MethodType)
def _(obj):
    return obj.__name__


@serialize.register(dict)
def _(obj):
    return {str(k):serialize(v) for k, v in obj.items()}


@serialize.register(list)
@serialize.register(set)
@serialize.register(tuple)
def _(obj):
    return [serialize(v) for v in obj]


@serialize.register(datetime.datetime)
@serialize.register(uuid.UUID)
@serialize.register(ipaddress.IPv4Address)
def _(obj):
    return str(obj)


def serializable_string(cls):
    """Decorator for classes that can be serialized as dicts."""

    def decorator(cls):

        @serialize.register(cls)
        def _(obj):
            return str(obj)

        return cls

    return decorator(cls)


def serializable_dict(cls):
    """Decorator for classes that can be serialized as dicts."""

    def decorator(cls):

        @serialize.register(cls)
        def _(obj):
            return serialize(obj.to_dict())

        return cls

    return decorator(cls)