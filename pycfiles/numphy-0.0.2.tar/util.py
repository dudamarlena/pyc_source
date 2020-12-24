# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: numphy/util.py
# Compiled at: 2018-05-02 13:10:51
"""
Helpful utility functions.
"""
__all__ = [
 'empty_slice', 'is_lazy_iterable', 'expand_ellipsis', 'no_value']
import types, collections, six
empty_slice = slice(None)

def is_lazy_iterable(obj):
    """
    Returns whether *obj* is iterable lazily, such as generators, range objects, etc.
    """
    return isinstance(obj, (
     types.GeneratorType, collections.MappingView, six.moves.range, enumerate))


def expand_ellipsis(values, size):
    if Ellipsis not in values:
        return values
    n = size - len(values) + 1
    if n <= 0:
        raise Exception(('size {}\xa0not sufficient to expand ellipsis').format(size))
    idx = values.index(Ellipsis)
    return values[:idx] + n * (empty_slice,) + values[idx + 1:]


class NoValue(object):

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False


no_value = NoValue()