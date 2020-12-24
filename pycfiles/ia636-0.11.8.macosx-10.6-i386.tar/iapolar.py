# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iapolar.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iapolar(f, domain, thetamax=2 * pi):
    from ia636 import iainterpollin
    f = array(f)
    m, n = f.shape
    dm, dn = domain
    Ry, Rx = floor(array(f.shape) / 2)
    b = min(Ry, Rx) / dm
    a = thetamax / dn
    y, x = indices(domain)
    XI = Rx + b * y * cos(a * x)
    YI = Ry + b * y * sin(a * x)
    g = iainterpollin(f, array([YI.ravel(), XI.ravel()]))
    g.shape = domain
    return g