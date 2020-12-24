# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/singleton.py
# Compiled at: 2016-10-06 14:34:19
"""
Singleton

This module defines a "super singleton" class that verifies only once instance
is actually created.  It allows the class designating itself as a singleton to
be inherited, still retains its singletoness, but makes sure that derived classes
aren't created first.

Test classes A -> B -> C where A is a singleton.  B can be created before A, and
calls for A will return the instance of B.  But if B is created, C cannot be created,
since a new C would imply a new instance of B.
"""
from . import debugging

class _SingletonMetaclass(type):

    def __init__(cls, *args):
        cls._singleton_instance = None
        old_cls_init = cls.__init__

        def __init_trap__(self, *args, **kwargs):
            if cls._singleton_instance:
                raise RuntimeError('instance of ' + cls.__name__ + ' has already been created')
            old_cls_init(self, *args, **kwargs)
            cls._singleton_instance = self

        cls.__init__ = __init_trap__
        super(_SingletonMetaclass, cls).__init__(*args)
        return

    def __call__(cls, *args, **kwargs):
        if cls._singleton_instance is None:
            cls._singleton_instance = super(_SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls._singleton_instance


class Singleton(object):
    __metaclass__ = _SingletonMetaclass


class _SingletonLoggingMetaclass(_SingletonMetaclass, debugging._LoggingMetaclass):
    pass


class SingletonLogging(object):
    __metaclass__ = _SingletonLoggingMetaclass