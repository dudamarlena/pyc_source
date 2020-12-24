# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/Divmod-release/Imaginary/imaginary/iterutils.py
# Compiled at: 2006-04-11 01:41:38
"""Utilities for dealing with iterators and such.
"""

def interlace(x, i):
    """interlace(x, i) -> i0, x, i1, x, ..., x, iN
    """
    i = iter(i)
    try:
        yield i.next()
    except StopIteration:
        return
    else:
        for e in i:
            yield x
            yield e