# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Sascha\Documents\PycharmProjects\maverig\maverig\data\components\utils\dataObject.py
# Compiled at: 2014-12-11 18:17:41
# Size of source mod 2**32: 3592 bytes
from collections import OrderedDict
from datetime import datetime
from PySide import QtCore
from numpy import ndarray

def fast_deepcopy(x):
    """ deepcopy hierachical objects containing any of the following types:
    ObjectDict, OrderedDict, dict, set, list, tuple, datetime, string, int, float, bool, NoneType """
    if isinstance(x, QtCore.QPointF):
        return QtCore.QPointF(x)
    if isinstance(x, (str, int, float, bool)) or x is None:
        result = x
        return result
    if isinstance(x, datetime):
        return datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, x.tzinfo)
    if isinstance(x, ObjectDict):
        result = ObjectDict.__new__(ObjectDict)
        super(type(result), result).__init__([(fast_deepcopy(key), fast_deepcopy(value)) for key, value in x.items()])
        return result
    if isinstance(x, OrderedDict):
        return OrderedDict([(fast_deepcopy(key), fast_deepcopy(value)) for key, value in x.items()])
    if isinstance(x, dict):
        return {fast_deepcopy(key):fast_deepcopy(value) for key, value in x.items()}
    if isinstance(x, set):
        return {fast_deepcopy(key) for key in x}
    if isinstance(x, list):
        return [fast_deepcopy(item) for item in x]
    if isinstance(x, tuple):
        return tuple([fast_deepcopy(item) for item in x])
    if isinstance(x, Data):
        result = x.__new__(type(x))
        if hasattr(x, '__dict__'):
            for attr, value in x.__dict__.items():
                if not isinstance(getattr(type(x), attr), property):
                    setattr(result, attr, fast_deepcopy(value))
                    continue

        return result
    if isinstance(x, ndarray):
        return x
    print('datatype %s not supported.' % str(type(x)))


class Data:
    __doc__ = ' base class for any model containing modifiable data in class attributes\n\n    class attributes are copied to instances\n    in order to modify attribute objects on instance level\n    '

    def __init__(self):
        """ copies class attributes to instance """
        super().__init__()

        def deep_attributes(in_cls):
            result = {}
            for base in in_cls.__bases__:
                result.update(deep_attributes(base))

            result.update(in_cls.__dict__)
            return result

        for attr, value in deep_attributes(self.__class__).items():
            if not attr.startswith('__') and not callable(value) and not isinstance(value, property):
                setattr(self, attr, fast_deepcopy(value))
                continue


class ObjectDict(OrderedDict):
    __doc__ = " return a dict with objects mapped to their names:\n\n    Usage: classes AClass and BClass given with AClass.name = 'A' and BClass.name = 'B'\n           ObjectDict([AClass, BClass]) will return\n               {'A': AClass(), 'B': BClass()}\n    "

    def __init__(self, classes=[]):
        super().__init__([(cls.name, cls()) for cls in classes])

    def __add__(self, other):
        if isinstance(other, list):
            for cls in other:
                self[cls.name] = cls()

        else:
            if isinstance(other, ObjectDict):
                for cls_name, cls_instance in other.items():
                    self[cls_name] = cls_instance

            elif isinstance(other, type(Data)):
                if hasattr(other, 'name'):
                    cls = other
                    self[cls.name] = cls()