# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/util/cache.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1120 bytes
from __future__ import absolute_import
import functools
from time import time

def memoize(timeout, dynamic_timeout=False):
    """
    Memoization decorator with support for timeout.
    
    If dynamic_timeout is set, the cache timeout is doubled if the cached function 
    takes longer time to run than the timeout time
    """
    cache = {'timeout': timeout}

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            if 'time' not in cache or start - cache['time'] > cache['timeout']:
                cache['result'] = func(*args, **kwargs)
                cache['time'] = time()
                if dynamic_timeout:
                    if cache['time'] - start > cache['timeout']:
                        cache['timeout'] *= 2
            return cache['result']

        def clear_cache():
            if 'time' in cache:
                del cache['time']
            if 'result' in cache:
                del cache['result']

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator