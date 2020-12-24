# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/stats.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 3996 bytes
"""
This module is for statistics.
"""
from __future__ import absolute_import, division, print_function
import six, numpy as np, scipy.stats
from skxray.core.utils import _defaults
import logging
logger = logging.getLogger(__name__)

def statistics_1D(x, y, stat='mean', nx=None, min_x=None, max_x=None):
    """
    Bin the values in y based on their x-coordinates

    Parameters
    ----------
    x : array
        position
    y : array
        intensity
    stat: str or func, optional
        statistic to be used on the binned values defaults to mean
        see scipy.stats.binned_statistic
    nx : integer, optional
        number of bins to use defaults to default bin value
    min_x : float, optional
        Left edge of first bin defaults to minimum value of x
    max_x : float, optional
        Right edge of last bin defaults to maximum value of x

    Returns
    -------
    edges : array
        edges of bins, length nx + 1

    val : array
        statistics of values in each bin, length nx
    """
    if min_x is None:
        min_x = np.min(x)
    if max_x is None:
        max_x = np.max(x)
    if nx is None:
        nx = _defaults['bins']
    bins = np.linspace(start=min_x, stop=max_x, num=nx + 1, endpoint=True)
    val, _, _ = scipy.stats.binned_statistic(x, y, statistic=stat, bins=bins)
    return (
     bins, val)