# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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