# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\TestLibs\np_rw_buffer\np_rw_buffer\circular_indexes.py
# Compiled at: 2018-11-13 11:38:32
# Size of source mod 2**32: 987 bytes
"""
Fast method to get the proper indexes for a circular buffer.

See history of version control. Python C tuple '_circular_indexes.c' building a tuple was much slower.
"""
import numpy as np

def get_indexes(start, length, maxsize):
    """Return the indexes from the given start position to the given length."""
    stop = start + length
    if stop > maxsize:
        try:
            return np.concatenate((np.arange(start, maxsize),
             np.arange(0, stop % maxsize)))
        except ZeroDivisionError:
            return []

    else:
        if stop < 0:
            return np.concatenate((np.arange(start, -1, -1),
             np.arange(maxsize, maxsize - stop, -1)))
        try:
            return slice(start, stop, length // abs(length))
        except ZeroDivisionError:
            return slice(start, stop)