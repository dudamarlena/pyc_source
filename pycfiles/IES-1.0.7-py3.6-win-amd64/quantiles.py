# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\lib\quantiles.py
# Compiled at: 2018-04-03 04:51:51
# Size of source mod 2**32: 363 bytes
"""
Algorithms for computing quantiles on numpy arrays.
"""
from numpy.lib import apply_along_axis
from pandas import qcut

def quantiles(data, nbins_or_partition_bounds):
    """
    Compute rowwise array quantiles on an input.
    """
    return apply_along_axis(qcut,
      1,
      data,
      q=nbins_or_partition_bounds,
      labels=False)