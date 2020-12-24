# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/util.py
# Compiled at: 2016-08-09 13:43:28
# Size of source mod 2**32: 1448 bytes
"""WebCore common utilities."""
from __future__ import unicode_literals
from threading import RLock
from marrow.package.canonical import name
sentinel = object()

def safe_name(thing):
    """Attempt to resolve the canonical name for an object, falling back on the `repr()` if unable to do so."""
    try:
        return name(thing)
    except:
        return repr(thing)


class lazy(object):
    __doc__ = 'Lazily record the result of evaluating a function and cache the result.\n\t\n\tThis is a non-data descriptor which tells Python to allow the instance __dict__ to override. Intended to be used\n\tby extensions to add zero-overhead (if un-accessed) values to the context.\n\t'

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__
        self.lock = RLock()
        self.func = func

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        with self.lock:
            value = instance.__dict__.get(self.__name__, sentinel)
            if value is sentinel:
                value = instance.__dict__[self.__name__] = self.func(instance)
        return value