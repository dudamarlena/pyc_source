# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iapercentile.py
# Compiled at: 2014-08-21 22:30:04


def iapercentile(f, p=1):
    import numpy as np
    k = (f.size - 1) * p / 100.0
    dw = np.floor(k).astype(int)
    up = np.ceil(k).astype(int)
    g = np.sort(f.ravel())
    d = g[dw]
    d0 = d * (up - k)
    d1 = g[up] * (k - dw)
    return np.where(dw == up, d, d0 + d1)