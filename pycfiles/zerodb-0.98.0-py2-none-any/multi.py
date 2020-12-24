# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/storage/multi.py
# Compiled at: 2016-03-08 18:12:41
"""
Combine multiple server storages in one class
"""
import six
from types import MethodType, FunctionType
from ZEO.StorageServer import ZEOStorage

def _is_method(f):
    if six.PY2:
        return isinstance(f, MethodType)
    else:
        return isinstance(f, FunctionType)


class ServerStorageMeta(type):

    def __init__(cls, name, bases, dct):
        dct = dict(dct)
        extensions = set(cls.extensions)
        for base in reversed(bases):
            if hasattr(base, 'extensions'):
                extensions.update(base.extensions)
            else:
                for attr in dir(base):
                    meth = getattr(base, attr)
                    if not attr.startswith('_') and _is_method(meth) and not hasattr(ZEOStorage, attr):
                        extensions.add(meth)

        cls.extensions = list(extensions)
        super(ServerStorageMeta, cls).__init__(name, bases, dct)


class MultiStorage(six.with_metaclass(ServerStorageMeta, ZEOStorage, object)):
    pass