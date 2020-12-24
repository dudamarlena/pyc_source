# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_joblib.py
# Compiled at: 2013-01-11 05:03:40
"""Test if doctests work with decorated functions."""
import functools
from joblib import Memory
mem = Memory('test')

def twice(func):
    """
    Double the result of func().
    
    >>> fun(10)
    22
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """This docstring will be replaced by functools.wraps()."""
        return 2 * func(*args, **kwargs)

    return wrapper


@twice
def fun(x):
    """
    Increase x by 1.
    
    >>> fun(10)
    22
    """
    return x + 1


@mem.cache
def cached(x):
    """
    Increase x by 1.
    
    >>> cached(10)
    """
    return x + 1


def manually_cached(x):
    """
    Increase x by 1.
    
    >>> manually_cached(10)
    11
    """
    return x + 1


manually_cached = twice(mem.cache(manually_cached))