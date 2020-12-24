# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/utils/memo.py
# Compiled at: 2019-06-30 09:25:49
# Size of source mod 2**32: 308 bytes
from functools import wraps

def memoize(func):
    cache = dict()

    @wraps(func)
    def memoized_func(*args):
        cargs = str(args)
        if cargs in cache:
            return cache[cargs]
        else:
            result = func(*args)
            cache[cargs] = result
            return result

    return memoized_func