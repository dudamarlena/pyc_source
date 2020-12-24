# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/bcferries/lib/python2.7/site-packages/bcferries/decorators.py
# Compiled at: 2014-12-29 07:01:11
import datetime
from functools import wraps
from fuzzydict import FuzzyDict

def cacheable(f):

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        ignore_cache = kwargs.pop('ignore_cache', False)
        if ignore_cache is True:
            self._api.ignore_cache = True
            result = f(self, *args, **kwargs)
            self._api.ignore_cache = False
            return result
        else:
            if datetime.datetime.now() - self._api.last_cleared > self._api.cache_for:
                self._api._flush_cache()
            return f(self, *args, **kwargs)

    return wrapper


def fuzzy(f):

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        keys_only = kwargs.pop('keys_only', False)
        result = f(self, *args, **kwargs)
        if keys_only:
            return [ {'name': x} for x in result.keys() ]
        else:
            return FuzzyDict(result)

    return wrapper


def lazy_cache(f):
    name = '__' + f.__name__

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, name):
            setattr(self, name, f(self, *args, **kwargs))
        return getattr(self, name)

    return wrapper