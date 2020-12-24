# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dcollins/.env/deleteme/lib/python2.7/site-packages/croi/decorators.py
# Compiled at: 2015-03-14 18:42:29
from functools import wraps

def lazy(func):
    cache = {}

    @wraps(func)
    def wrap(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrap


def lazy_property(func):
    canary = object()
    prop_name = '_prop_' + func.func_name

    @property
    @wraps(func)
    def wrap(self, *args, **kwargs):
        value = getattr(self, prop_name, canary)
        if value is canary:
            value = func(self, *args, **kwargs)
            setattr(self, prop_name, value)
        return value

    return wrap