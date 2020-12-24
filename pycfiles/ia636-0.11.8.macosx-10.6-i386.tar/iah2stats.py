# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iah2stats.py
# Compiled at: 2014-08-21 22:30:04


def iah2stats(h):
    import numpy as np, ia636 as ia
    hn = 1.0 * h / h.sum()
    v = np.zeros(11)
    n = len(h)
    v[0] = np.sum(np.arange(n) * hn)
    v[1] = np.sum(np.power(np.arange(n) - v[0], 2) * hn)
    v[2] = np.sum(np.power(np.arange(n) - v[0], 3) * hn) / np.power(v[1], 1.5)
    v[3] = np.sum(np.power(np.arange(n) - v[0], 4) * hn) / np.power(v[1], 2) - 3
    v[4] = -(hn[(hn > 0)] * np.log(hn[(hn > 0)])).sum()
    v[5] = np.argmax(h)
    v[6:] = ia.iah2percentile(h, np.array([1, 10, 50, 90, 99]))
    return v