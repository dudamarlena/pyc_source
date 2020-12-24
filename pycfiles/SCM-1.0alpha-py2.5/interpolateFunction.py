# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/epscComp/interpolateFunction.py
# Compiled at: 2009-05-29 13:49:18
from scipy import interpolate

def linearInterp1D(x, y, x_new):
    """ Linear 1D interpolation."""
    f = interpolate.interp1d(x, y)
    y_new = f(x_new)
    return y_new


def splineInterp1D(x, y, x_new):
    """ Spline 1D interpolation."""
    tck = interpolate.splrep(x, y, s=0)
    y_new = interpolate.splev(x_new, tck, der=0)
    return y_new


if __name__ == '__main__':
    x = arange(0, -10, -1)
    y = exp(-x / 3.0)
    x = x[::-1]
    y = y[::-1]
    x_new = arange(0, -12, -1)
    x_new = x_new[::-1]
    y_new = splineInterp1D(x, y, x_new)