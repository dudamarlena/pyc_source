# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/decorators.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

def cachedmethod(f, cache={}):
    """
    Method with a cached content

    Reference: http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
    """

    def _(*args, **kwargs):
        try:
            key = (
             f, tuple(args), frozenset(kwargs.items()))
        except:
            key = ('').join(str(_) for _ in (f, args, kwargs))

        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return _