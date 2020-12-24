# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/decorators.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 1369 bytes
from random import randint
from functools import wraps
from datetime import timedelta
from cachelib import SimpleCache
from sovereign.logs import LOG
from sovereign.statistics import stats
cache = SimpleCache()

def memoize(timeout, jitter=0):
    """
    Decorator to cache a function by name/args

    :param timeout: How long to keep the result
    :param jitter: Randomize the timeout by this many seconds
    """
    if isinstance(timeout, timedelta):
        timeout = timeout.seconds
    timeout += randint(-jitter / 2, jitter)

    def decorator(decorated):

        @wraps(decorated)
        def wrapper(*args, **kwargs):
            key = f"{decorated.__name__}{args}{kwargs}"
            ret = cache.get(key)
            metrics_tags = [
             f"function:{decorated.__name__}"]
            if ret is None:
                stats.increment('cache.miss', tags=metrics_tags)
                ret = decorated(*args, **kwargs)
                try:
                    cache.set(key, ret, timeout=timeout)
                except AttributeError:
                    stats.increment('cache.fail', tags=metrics_tags)
                    LOG.warn(event='failed to write result to cache', key=key)

            else:
                stats.increment('cache.hit', tags=metrics_tags)
            return ret

        return wrapper

    return decorator