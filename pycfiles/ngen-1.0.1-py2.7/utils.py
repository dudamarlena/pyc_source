# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/utils.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import unicode_literals, absolute_import, print_function
from functools import wraps
import time
DEFAULT_PATH = b'_tmp.log'

def simple_timer(func):
    """
        a simple decorator that can be used to wrap a given function in order
        to record how much time it took to complete the execution.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        finish = time.time()
        delta = finish - start
        with open(DEFAULT_PATH, b'a') as (_file):
            _file.write(b'simple_timer: "%s" took %fs to complete.\n' % (
             func.__name__, delta))
        return ret

    return wrapper


class TimerContext(object):
    """
        a context manager that can be used to record the time taken to execute
        a sequence of functions.
    """
    start = None
    finish = None
    delta = None

    def __init__(self, path=None, name=None):
        self.path = path or DEFAULT_PATH
        self.name = name or b'None'

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, tracebk):
        self.finish = time.time()
        self.delta = self.finish - self.start
        with open(self.path, b'a') as (_file):
            _file.write(b'TimerContext: "%s" took %fs to complete.\n' % (
             self.name, self.delta))


def timer(path=None):
    """
        a decorator that can be used to track time taken to execute the
        wrapped function, it accepts a path argument.
    """
    _path = path or DEFAULT_PATH

    def _timer(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            finish = time.time()
            delta = finish - start
            with open(_path, b'a') as (_file):
                _file.write(b'timer: "%s" took %fs to complete.\n' % (
                 func.__name__, delta))
            return ret

        return wrapper

    return _timer


class cached_property(object):
    """
        Decorator that converts a method with a single self argument into a
        property cached on the instance.

        Optional ``name`` argument allows you to make cached properties of
        other methods.
        (e.g.  url = cached_property(get_absolute_url, name='url') )
    """

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, b'__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        else:
            res = instance.__dict__[self.name] = self.func(instance)
            return res


def chunk(array, size, strict=False):
    last = None if not strict else len(array) // size
    return [ array[idx:idx + size] for idx in range(0, len(array), size)
           ][:last]