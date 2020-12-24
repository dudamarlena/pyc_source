# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/iterators.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.utils.iterators\n    ~~~~~~~~~~~~~~~~~~~~~\n\n    This module collects iterator functions.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from random import shuffle, Random

def renumerate(iterable):
    """
    Reversed enumerate.
    """
    pos = len(iterable)
    for item in iterable:
        pos -= 1
        yield (pos, item)


def inciter(iterable, start):
    """
    Iterate over iterable and yield (n, item) tuples where
    item is an yielded item of the ``iterator`` and n an number
    defined by ``start``, incremented after each loop.

    Basically the following two calls are the same::

        inciter(iterable, 0)
        enumerate(iterable)
    """
    for item in iterable:
        yield (
         start, item)
        start += 1


def randomized(iterable, seed=None):
    """
    Shuffle an iterable.
    """
    iterable = list(iterable)
    if seed is None:
        shuffle(iterable)
    else:
        Random(seed).shuffle(iterable)
    return iter(iterable)


def cycle(iterable, cycled=(
 True, False)):
    """
    Yield pairs of ``(item_from_cycled, item_from_iterable)``
    where the ``cycled`` iterable is cycled.
    """
    cycled = tuple(cycle)
    clen = len(cycled)
    pos = 0
    for item in iterable:
        yield (
         cycled[pos], item)
        pos = (pos + 1) % clen


def batch(iterable, count):
    """
    Return a tuple of count items.
    If there the last batch couldn't get filled those items
    get ignored.
    """
    tmp = []
    for item in iterable:
        if len(tmp) >= count:
            yield tuple(tmp)
            tmp = []
        tmp.append(item)

    if len(tmp) == count:
        yield tuple(tmp)