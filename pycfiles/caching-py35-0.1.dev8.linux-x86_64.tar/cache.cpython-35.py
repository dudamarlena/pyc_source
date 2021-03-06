# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/caching/cache.py
# Compiled at: 2018-09-14 01:12:44
# Size of source mod 2**32: 5297 bytes
import pickle
from collections import OrderedDict
from functools import wraps
from typing import Union, Callable
from .storage import SQLiteStorage
MISS = object()

def make_key(*args, **kwargs):
    if kwargs:
        return (args, *(x for kv in sorted(kwargs.items()) for x in kv))
    else:
        return args


def _type_names(args, kwargs):
    arg_type_names = (
     *map(_type_name, args),)
    kwarg_type_names = (*(_type_name(v) for k, v in sorted(kwargs.items())),)
    return (arg_type_names, kwarg_type_names)


def _type_name(obj):
    klass = type(obj)
    return '{klass.__module__}.{klass.__qualname__}'.format(klass=klass)


def _function_name(fn):
    return '{fn.__module__}.{fn.__qualname__}'.format(fn=fn)


class Cache:
    __doc__ = 'Cache.\n\n    Can be used as a function decorator and as a dict-like key-value store.\n    '

    def __init__(self, *, maxsize: int=1024, ttl: Union[(float, int)]=-1, filepath: Union[(str, None)]=None, policy: str='FIFO', key: Callable=make_key, only_on_errors=False, **kwargs):
        """
        Args:
            maxsize: maximum number of keys in cache.
            ttl: amount of time in seconds since the item is added to cache
                before the item is deleted from cache.
            filepath: if a string is passed then file path where the cache
                is stored on disk. If `None` is passed then the cache is stored
                in memory.
            policy: one of: FIFO, LRU, LFU.
                Cache replacement (or eviction) policy.
            key: a function which takes the arguments and keyword arguments of
                the decorated by the `Cache` instance function and retuns
                something which will be used as a key under which the function's
                return value will be stored in cache.
            only_on_errors: exception or a tuple of exceptions. Return cached
                results only in case of the exceptions are raisd in the
                decorated function.
        """
        self.params = OrderedDict(maxsize=maxsize, ttl=ttl, filepath=filepath, policy=policy, key=key, only_on_errors=only_on_errors, **kwargs)
        self.only_on_errors = only_on_errors
        self.make_key = key
        self.storage = SQLiteStorage(filepath=filepath or ':memory:', ttl=ttl, maxsize=maxsize, policy=policy)

    def __repr__(self):
        return '{self.__class__.__name__}'.format(self=self) + '({})'.format(', '.join('{k}={v}'.format(k=k, v=repr(v)) for k, v in self.params.items()))

    def _decorator(self, fn):
        if not callable(fn):
            raise TypeError('{fn} is not callable'.format(fn=fn))
        key_prefix = _function_name(fn)
        make_key_ = self.make_key

        @wraps(fn)
        def wrapper(*args, **kwargs):
            global MISS
            key = (
             
              key_prefix, *make_key_(*args, **kwargs))
            if self.only_on_errors:
                try:
                    res = fn(*args, **kwargs)
                except self.only_on_errors as e:
                    res = self.get(key, MISS)
                    if res is MISS:
                        raise e
                else:
                    self[key] = res
            else:
                res = self.get(key, MISS)
            if res is MISS:
                res = self[key] = fn(*args, **kwargs)
            return res

        wrapper._cache = self
        return wrapper

    def __call__(self, fn=None, **kwargs):
        if fn is None and kwargs:
            return self.copy(**kwargs)(fn)
        else:
            if callable(fn) and not kwargs:
                return self._decorator(fn)
            return self._decorator

    def __getitem__(self, key):
        return self.decode(self.storage[self.encode(key)])

    def __setitem__(self, key, value):
        self.storage[self.encode(key)] = self.encode(value)

    def __delitem__(self, key):
        del self.storage[self.encode(key)]

    def __contains__(self, key):
        return self.get(key, MISS) is not MISS

    def items(self):
        return ((self.decode(k), self.decode(v)) for k, v in self.storage.items())

    def get(self, key, default=None):
        res = self.storage.get(self.encode(key), default)
        if res is not default:
            res = self.decode(res)
        return res

    def clear(self):
        self.storage.clear()

    def close(self):
        self.storage.close()

    def copy(self, **kwargs):
        return self.__class__(**{**(self.params), **kwargs})

    def encode(self, obj):
        return pickle.dumps(obj)

    def decode(self, data):
        return pickle.loads(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.storage.close()

    def remove(self):
        self.storage.remove()