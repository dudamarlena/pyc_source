# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/streamio/stat.py
# Compiled at: 2013-11-20 21:18:21
"""stat"""

def minmax(xs):
    """Return the min and max values for the given iterable

    :param xs: An iterable of values
    :type xs: Any iterable of single numerical values.

    This function returns both the min and max of the given iterable
    by computing both at once and iterating/consuming the iterable once.
    """
    it = iter(xs)
    x = next(it)
    _min, _max = x, x
    for x in it:
        if x < _min:
            _min = x
        if x > _max:
            _max = x

    return (
     _min, _max)


__all__ = ('minmax', )