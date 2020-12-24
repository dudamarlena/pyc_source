# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iatiling.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iatiling(f, w):
    H = Hold = w
    g = np.zeros((H, w), 'uint8')
    ih = iw = 0
    himax = 0
    for i in range(len(f)):
        hi, wi = f[i].shape
        if iw + wi > w:
            iw = 0
            ih += himax + 1
            himax = 0
        if ih + hi > H:
            H += w
            g1 = np.zeros((H, w), 'uint8')
            g1[:Hold, :] = g
            g = g1
            Hold = H
        g[ih:ih + hi, iw:iw + wi] = f[i]
        iw += wi + 1
        himax = max(himax, hi)

    return g