# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fluid/common/window_mean.py
# Compiled at: 2006-12-04 09:19:16
"""Window means"""
try:
    import numpy as N
except:
    try:
        import numarray as N
    except:
        import Numeric as N

def window_mean(y, x=None, x_out=None, method='rectangular', boxsize=None):
    """Windowed means along 1-D array
    
    Input:
        - x [0,1,2,3,...] =>
        - x_out [x] =>
        - method [rectangular]:
            + rectangular => All data in window have same weight
        - boxsize [mean space] =>
    Output:

    Apply windowed means on a 1-D data array. Selecting adequate x_out
    and boxsize could define boxmeans or smooth filters. Method defines
    the weight method.

    An important point of this function is the ability to work with 
    unhomogenious spaced samples. Data ([1,2,3]) colected at [1,2,4] 
    times would be different if was collected at [1,2,3].
    """
    if x == None:
        x = N.arange(N.size(y))
    if x_out == None:
        x_out = x
    y_out = N.zeros(N.size(x_out), N.Float)
    if boxsize == None:
        boxsize = (max(x) - min(x)) / (N.size(x_out) * 1.0)
    half_boxsize = boxsize / 2.0
    for i in range(N.size(x_out)):
        x_i = x_out[i]
        hi_limit = x_i + half_boxsize
        lo_limit = x_i - half_boxsize
        index = N.less_equal(x, hi_limit) * N.greater_equal(x, lo_limit)
        x_tmp = N.compress(index, x) - x_i
        y_tmp = N.compress(index, y)
        weight = window_weight(x_tmp, boxsize, method)
        y_out[i] = N.sum(y_tmp * weight)

    return y_out


def window_weight(x, boxsize=None, method='rectangular'):
    """Window weights
    """
    if method == 'rectangular':
        weight = N.ones(N.shape(x), N.Float)
    elif method == 'triangular':
        half_size = boxsize / 2.0
        left = N.less_equal(x, 0) * (x + half_size)
        right = N.greater(x, 0) * (half_size - x)
        weight = left + right
    else:
        return
    weight = weight / N.sum(weight)
    return weight