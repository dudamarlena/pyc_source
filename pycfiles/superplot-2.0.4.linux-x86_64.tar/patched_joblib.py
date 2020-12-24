# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/statslib/patched_joblib.py
# Compiled at: 2016-09-09 23:03:24
"""
Patch the joblib's caching classes so that cached functions can be
doctested. For this the decorator must return a function with correct
__doc__ attribute.
"""
from joblib import Memory
from tempfile import mkdtemp
from functools import update_wrapper

class PatchedMemory(Memory):
    """
    Patch joblib's Memory class so that it may be doctested.
    """

    def cache(self, func, *args, **kwargs):

        def cfunc(*fargs, **fkwargs):
            return Memory.cache(self, func, *args, **kwargs).__call__(*fargs, **fkwargs)

        update_wrapper(cfunc, func)
        return cfunc


cachedir = mkdtemp()
memory = PatchedMemory(cachedir=cachedir, verbose=0)

@memory.cache
def test_function():
    """
    >>> test_function() == test_function()
    True
    """
    from random import random
    return random()


if __name__ == '__main__':
    import doctest
    doctest.testmod()