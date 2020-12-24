# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/utils/cache.py
# Compiled at: 2018-10-05 05:15:57
# Size of source mod 2**32: 6432 bytes
from time import time
import threading
from functools import partial
from django.utils.functional import cached_property
from django.core.cache import cache
try:
    import asyncio
except (ImportError, SyntaxError):
    asyncio = None

__all__ = [
 'cached_property',
 'cached_property_with_ttl',
 'memoize',
 'cached',
 'cache_get_or_set']

class memoize(object):
    __doc__ = "Decorator that caches a function's return value each time it is called.\n    If called later with the same arguments, the cached value is returned, and\n    not re-evaluated.\n    "

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = (self.func)(*args)
            self.cache[args] = value
            return value
        except TypeError:
            return (self.func)(*args)

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        fn = partial(self.__call__, obj)
        fn.reset = self._reset
        return fn

    def _reset(self):
        self.cache = {}


class cached(memoize):
    pass


def cache_get_or_set(key, value, ttl):
    return cache.get_or_set(key, value, ttl)


class cached_property:
    __doc__ = "\n    Decorator that converts a method with a single self argument into a\n    property cached on the instance.\n\n    Optional ``name`` argument allows you to make cached properties of other\n    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )\n    "

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        """
        Call the function and put the return value in instance.__dict__ so that
        subsequent attribute access on the instance returns the cached value
        instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        else:
            res = instance.__dict__[self.name] = self.func(instance)
            return res


class threaded_cached_property(object):
    __doc__ = '\n    A cached_property version for use in environments where multiple threads\n    might concurrently try to access the property.\n    '

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj_dict = obj.__dict__
        name = self.func.__name__
        with self.lock:
            try:
                return obj_dict[name]
            except KeyError:
                return obj_dict.setdefault(name, self.func(obj))


class cached_property_with_ttl(object):
    __doc__ = '\n    A property that is only computed once per instance and then replaces itself\n    with an ordinary attribute. Setting the ttl to a number expresses how long\n    the property will last before being timed out.\n    '

    def __init__(self, ttl=None):
        if callable(ttl):
            func = ttl
            ttl = None
        else:
            func = None
        self.ttl = ttl
        self._prepare_func(func)

    def __call__(self, func):
        self._prepare_func(func)
        return self

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            now = time()
            obj_dict = obj.__dict__
            name = self.__name__
            try:
                value, last_updated = obj_dict[name]
            except KeyError:
                pass

            ttl_expired = self.ttl and self.ttl < now - last_updated
            if not ttl_expired:
                return value
            value = self.func(obj)
            obj_dict[name] = (value, now)
            return value

    def __delete__(self, obj):
        obj.__dict__.pop(self.__name__, None)

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = (
         value, time())

    def _prepare_func(self, func):
        self.func = func
        if func:
            self.__doc__ = func.__doc__
            self.__name__ = func.__name__
            self.__module__ = func.__module__


cached_property_ttl = cached_property_with_ttl
timed_cached_property = cached_property_with_ttl

class threaded_cached_property_with_ttl(cached_property_with_ttl):
    __doc__ = '\n    A cached_property version for use in environments where multiple threads\n    might concurrently try to access the property.\n    '

    def __init__(self, ttl=None):
        super(threaded_cached_property_with_ttl, self).__init__(ttl)
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        with self.lock:
            return super(threaded_cached_property_with_ttl, self).__get__(obj, cls)


threaded_cached_property_ttl = threaded_cached_property_with_ttl
timed_threaded_cached_property = threaded_cached_property_with_ttl