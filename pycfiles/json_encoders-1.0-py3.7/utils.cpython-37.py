# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/json_encoders/utils.py
# Compiled at: 2020-05-11 10:02:35
# Size of source mod 2**32: 1203 bytes
from enum import Enum

def is_elemental(obj):
    return isinstance(obj, (int, float, Enum))


def is_collection(obj):
    return isinstance(obj, (list, dict, tuple, set))


def is_custom_class(obj):
    return not isinstance(obj, (int, float, Enum, list, dict, tuple, set)) and hasattr(obj, '__dict__')


def hashable(obj):
    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True


def to_hashable(obj):
    if isinstance(obj, (list, tuple)):
        return list_to_hashable(obj)
    if isinstance(obj, dict):
        return dict_to_hashable(obj)
    if isinstance(obj, set):
        return set_to_hashable(obj)
    return id(obj)


def set_to_hashable(obj):
    converted = list(obj)
    converted.sort(key=(lambda x: id(x)))
    return list_to_hashable(converted)


def list_to_hashable(obj):
    return tuple(((item if hashable(item) else id(item)) for item in obj))


def dict_to_hashable(obj):
    converted = [(k, v) for k, v in obj.items()]
    converted.sort(key=(lambda x: id(x[0])))
    keys = tuple(((x[0] if hashable(x[0]) else id(x[0])) for x in converted))
    values = tuple(((x[1] if hashable(x[1]) else id(x[1])) for x in converted))
    return (keys, values)