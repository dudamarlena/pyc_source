# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/HackerNewsAPI/utils.py
# Compiled at: 2014-10-18 15:01:38
__author__ = 'Robert P. Cope'
from functools import wraps
import time

def rate_limit(wait_time=10):
    wait_time /= 1000.0

    def wrapper(func):
        last_call = [
         0.0]

        @wraps(func)
        def rate_limited_func(*args, **kwargs):
            time_elapsed = time.clock() - last_call[0]
            if time_elapsed < wait_time:
                time.sleep(wait_time - time_elapsed)
            ret_val = func(*args, **kwargs)
            last_call[0] = time.clock()
            return ret_val

        return rate_limited_func

    return wrapper