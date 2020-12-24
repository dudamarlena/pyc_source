# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iah2percentile.py
# Compiled at: 2014-08-21 22:30:04


def iah2percentile(h, p):
    import numpy as np
    s = h.sum()
    k = (s - 1) * p / 100.0 + 1
    dw = np.floor(k)
    up = np.ceil(k)
    hc = np.cumsum(h)
    if isinstance(p, int):
        k1 = np.argmax(hc >= dw)
        k2 = np.argmax(hc >= up)
    else:
        k1 = np.argmax(hc >= dw[:, np.newaxis], axis=1)
        k2 = np.argmax(hc >= up[:, np.newaxis], axis=1)
    d0 = k1 * (up - k)
    d1 = k2 * (k - dw)
    return np.where(dw == up, k1, d0 + d1)