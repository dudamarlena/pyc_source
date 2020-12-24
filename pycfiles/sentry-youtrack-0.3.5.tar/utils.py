# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adambogdal/git/sentry-youtrack/sentry_youtrack/utils.py
# Compiled at: 2015-08-24 17:34:10
from hashlib import md5
from sentry.utils.cache import cache

def cache_this(timeout=60):

    def decorator(func):

        def wrapper(*args, **kwargs):

            def get_cache_key(*args, **kwargs):
                params = list(args) + kwargs.values()
                return md5(('').join(map(str, params))).hexdigest()

            key = get_cache_key(func.__name__, *args, **kwargs)
            result = cache.get(key)
            if not result:
                result = func(*args, **kwargs)
                cache.set(key, result, timeout)
            return result

        return wrapper

    return decorator


def get_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default