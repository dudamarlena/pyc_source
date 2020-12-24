# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/toolware/utils/profiler.py
# Compiled at: 2018-08-18 10:25:00
# Size of source mod 2**32: 367 bytes
import cProfile, functools

def profileit(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + '.profile'
        prof = cProfile.Profile()
        retval = (prof.runcall)(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper