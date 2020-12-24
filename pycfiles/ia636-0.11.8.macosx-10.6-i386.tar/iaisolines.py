# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaisolines.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np, ia636 as ia

def iaisolines(f, nc=10, n=1):
    maxi = np.ceil(f.max())
    mini = np.floor(f.min())
    d = int(np.ceil(1.0 * (maxi - mini) / nc))
    m = np.zeros((d, 1))
    m[0:n, :] = 1
    m = np.resize(m, (maxi - mini, 1))
    m = np.concatenate((np.zeros((mini, 1)), m))
    m = np.concatenate((m, np.zeros((256 - maxi, 1))))
    m = np.concatenate((m, m, m), 1)
    ct = m * ia.iacolormap('hsv') + (1 - m) * ia.iacolormap('gray')
    g = ia.iaapplylut(f, ct)
    return g