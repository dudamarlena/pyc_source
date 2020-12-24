# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/iterables.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 3646 bytes
from __future__ import absolute_import
from builtins import map
from builtins import object
try:
    from itertools import zip_longest
except:
    from itertools import izip_longest as zip_longest

def flatten(iterables):
    """ Flatten an iterable, except for string elements. """
    for it in iterables:
        if isinstance(it, str):
            yield it
        else:
            for element in it:
                yield element


class concat(object):
    __doc__ = "\n    A literal iterable that lets you combine sequence literals (lists, set) with generators or list\n    comprehensions. Instead of\n\n    >>> [ -1 ] + [ x * 2 for x in range( 3 ) ] + [ -1 ]\n    [-1, 0, 2, 4, -1]\n\n    you can write\n\n    >>> list( concat( -1, ( x * 2 for x in range( 3 ) ), -1 ) )\n    [-1, 0, 2, 4, -1]\n\n    This is slightly shorter (not counting the list constructor) and does not involve array\n    construction or concatenation.\n\n    Note that concat() flattens (or chains) all iterable arguments into a single result iterable:\n\n    >>> from builtins import range\n    >>> list( concat( 1, range( 2, 4 ), 4 ) )\n    [1, 2, 3, 4]\n\n    It only does so one level deep. If you need to recursively flatten a data structure,\n    check out crush().\n\n    If you want to prevent that flattening for an iterable argument, wrap it in concat():\n\n    >>> from builtins import range\n    >>> list( concat( 1, concat( range( 2, 4 ) ), 4 ) )\n    [1, range(2, 4), 4]\n\n    Some more example.\n\n    >>> list( concat() ) # empty concat\n    []\n    >>> list( concat( 1 ) ) # non-iterable\n    [1]\n    >>> list( concat( concat() ) ) # empty iterable\n    []\n    >>> list( concat( concat( 1 ) ) ) # singleton iterable\n    [1]\n    >>> list( concat( 1, concat( 2 ), 3 ) ) # flattened iterable\n    [1, 2, 3]\n    >>> list( concat( 1, [2], 3 ) ) # flattened iterable\n    [1, 2, 3]\n    >>> list( concat( 1, concat( [2] ), 3 ) ) # protecting an iterable from being flattened\n    [1, [2], 3]\n    >>> list( concat( 1, concat( [2], 3 ), 4 ) ) # protection only works with a single argument\n    [1, 2, 3, 4]\n    >>> list( concat( 1, 2, concat( 3, 4 ), 5, 6 ) )\n    [1, 2, 3, 4, 5, 6]\n    >>> list( concat( 1, 2, concat( [ 3, 4 ] ), 5, 6 ) )\n    [1, 2, [3, 4], 5, 6]\n\n    Note that while strings are technically iterable, concat() does not flatten them.\n\n    >>> list( concat( 'ab' ) )\n    ['ab']\n    >>> list( concat( concat( 'ab' ) ) )\n    ['ab']\n    "

    def __init__(self, *args):
        super(concat, self).__init__()
        self.args = args

    def __iter__(self):

        def expand(x):
            if isinstance(x, concat):
                if len(x.args) == 1:
                    i = x.args
            elif not isinstance(x, str):
                try:
                    i = x.__iter__()
                except AttributeError:
                    i = (
                     x,)

            else:
                i = x
            return i

        return flatten(map(expand, self.args))