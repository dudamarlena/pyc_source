# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iavarfilter.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iavarfilter(f, h, CV=True):
    from ia636 import iapconv
    f = asarray(f).astype(float64)
    h = asarray(h).astype(bool)[::-1, ::-1]
    n = sum(ravel(h))
    h = h / float(n)
    fm = iapconv(f, h)
    f2m = iapconv(f ** 2, h)
    g = f2m - fm ** 2
    if CV:
        fm = fm + 1e-320 * (fm == 0)
        g[g < 0.0] = 0.0
        g = sqrt(g) / fm
    return g