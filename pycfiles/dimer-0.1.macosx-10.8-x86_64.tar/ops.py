# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/ops.py
# Compiled at: 2013-07-12 15:51:29
"""
common operations on numpy arrays
@author: odenas
"""
import numpy as np

def fit(x, axis=None, nans=0.0):
    """scale values of x in the interval [-1, 1]
    
    @param x: ndarray
    @param axis: passed to numpy.max and numpy.min
    @param nans: if nan values are produced replace them with this
    @return: scaled values of x"""
    M = x.max(axis=axis)
    m = x.min(axis=axis)
    mid_p = (M + m) / 2
    rng = M - m
    fitx = 2 * (x - mid_p) / rng
    fitx[np.isnan(fitx)] = nans
    return fitx


def standardize(x, axis=None, nans=0.0):
    """transform each component of flattened X examples to 0 mean and 1 std
    So the values of track t at position i are 0 mean and 1 std

    x: a pandas data panel of the form <anchors> X <tracks> X <genome position>
    return: (the shifted input,
    the mean for each input component, the sd of each input component)
    the latter 2 are arrays of shape(<tracks>, <genome position>)
    """
    m = x.mean(axis=axis)
    v = x.std(axis=axis)
    normX = (x - m) / v
    normX[np.isnan(normX)] = nans
    return (
     normX, m, v)