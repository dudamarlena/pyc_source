# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../OrthNet/orthnet/utils/timeit.py
# Compiled at: 2018-04-05 14:31:03
# Size of source mod 2**32: 376 bytes
import time
from functools import wraps

def timeit(loglevel):

    def _timeit(func):

        @wraps(func)
        def timed(*args, **kw):
            t1 = time.time()
            res = func(*args, **kw)
            print(func.__name__, time.time() - t1)
            return res

        def untimed(*args, **kw):
            return func(*args, **kw)

        if loglevel == 0:
            return untimed
        if loglevel == 1:
            return timed

    return _timeit