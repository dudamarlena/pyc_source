# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wursterk/code/tinyflow/venv/lib/python3.6/site-packages/tinyflow/tools.py
# Compiled at: 2017-03-15 20:58:04
# Size of source mod 2**32: 853 bytes
"""Assorted tools for working with streaming data."""
import itertools as it

class NULL(object):
    __doc__ = 'A sentinel for when ``None`` is a valid value or default.'


def slicer(iterable, chunksize):
    """
    Read an iterator in chunks.
    Example:
        >>> for p in slicer(range(5), 2):
        ...     print(p)
        (0, 1)
        (2, 3)
        (4,)
    Parameters
    ----------
    iterable : iter
        Input stream.
    chunksize : int
        Number of records to include in each chunk.  The last chunk will be
        incomplete unless the number of items in the stream is evenly
        divisible by `size`.
    Yields
    ------
    tuple
    """
    iterable = iter(iterable)
    while True:
        v = tuple(it.islice(iterable, chunksize))
        if v:
            yield v
        else:
            raise StopIteration