# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fastsom/core/decorators.py
# Compiled at: 2020-04-24 11:45:18
# Size of source mod 2**32: 699 bytes
"""
Shamelessly stolen from https://github.com/sevamoo/SOMPY/blob/master/sompy/decorators.py
"""
import logging
from functools import wraps
from time import time

def timeit(log_level=logging.INFO, alternative_title=None):

    def wrap(f):

        @wraps(f)
        def wrapped_f(*args, **kwargs):
            t0 = time()
            result = f(*args, **kwargs)
            ts = round(time() - t0, 6)
            title = alternative_title or f.__name__
            print(f" {title} took: {ts} seconds")
            return result

        return wrapped_f

    return wrap