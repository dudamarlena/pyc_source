# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/memory.py
# Compiled at: 2019-06-21 10:14:48
# Size of source mod 2**32: 598 bytes
"""This file contains several functions for memory usage.

Taken from the numpy tricks : http://ipython-books.github.io/featured-01/
"""
import numpy as np

def id(x):
    """Get the memory block address of an array."""
    return x.__array_interface__['data'][0]


def get_data_base(arr):
    """For a given array, finds the base array that "owns" the actual data."""
    base = arr
    while isinstance(base.base, np.ndarray):
        base = base.base

    return base


def arrays_share_data(x, y):
    """Return if two arrays share an offset."""
    return get_data_base(x) is get_data_base(y)