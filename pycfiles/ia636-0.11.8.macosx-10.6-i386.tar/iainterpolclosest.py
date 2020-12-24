# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iainterpolclosest.py
# Compiled at: 2014-08-21 22:30:04


def iainterpolclosest(f, pts):
    import numpy as np
    ptsi = np.rint(pts).astype(int)
    ptsi[ptsi < 0] = 0
    if ptsi.ndim == 1:
        ptsi.shape = (
         1, ptsi.size)
    for i in range(0, f.ndim):
        ptsi[i] = np.minimum(ptsi[i], f.shape[i] - 1)

    return f[list(ptsi)]