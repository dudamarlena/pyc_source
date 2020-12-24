# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/utils/cached_property.py
# Compiled at: 2018-05-09 08:59:44
# Size of source mod 2**32: 3615 bytes
import asyncio
from time import time
import threading

class CachedProperty:
    __doc__ = '\n    一般缓存\n    '

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            value = obj.__dict__[self.func.__name__] = self.func(obj)
            return value


class AsyncCachedProperty(CachedProperty):
    __doc__ = '\n    一般缓存\n    '

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    @asyncio.coroutine
    def __get__(self, obj, cls):
        if obj is None:
            return self
        else:
            if asyncio.iscoroutinefunction(self.func):
                v = yield from self.func(obj)
            else:
                v = self.func(obj)
            value = obj.__dict__[self.func.__name__] = v
            return value
        if False:
            yield None


class ThreadedCachedProperty:
    __doc__ = '\n    用于多线程场景的缓存\n    '

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


class CachedPropertyWithTtl:
    __doc__ = '\n    带失效时间的缓存，单位秒\n    '

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


class ThreadedCachedPropertyWithTtl(CachedPropertyWithTtl):
    __doc__ = '\n    用于多线程场景的带失效时间的缓存\n    单位秒\n    '

    def __init__(self, ttl=None):
        super(ThreadedCachedPropertyWithTtl, self).__init__(ttl)
        self.lock = threading.RLock()

    def __get__(self, obj, cls):
        with self.lock:
            return super(ThreadedCachedPropertyWithTtl, self).__get__(obj, cls)


cached_property = CachedProperty
async_cached_property = AsyncCachedProperty
cached_property_ttl = CachedPropertyWithTtl
timed_cached_property = CachedPropertyWithTtl
threaded_cached_property = ThreadedCachedProperty
threaded_cached_property_ttl = ThreadedCachedPropertyWithTtl
timed_threaded_cached_property = ThreadedCachedPropertyWithTtl