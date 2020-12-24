# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iahistogram.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iahistogram(f):
    return np.bincount(f.ravel())


def iahistogram_eq(f):
    from numpy import amax, zeros, arange, sum
    n = amax(f) + 1
    h = zeros((n,), int)
    for i in arange(n):
        h[i] = sum(i == f)

    return h


def iahistogram_eq1(f):
    import numpy as np
    n = f.size
    m = f.max() + 1
    haux = np.zeros((m, n), int)
    fi = f.ravel()
    i = xrange(n)
    haux[(fi, i)] = 1
    h = haux.sum(axis=1)
    return h