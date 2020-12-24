# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaotsu.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iaotsu(f):
    n = product(shape(f))
    h = 1.0 * bincount(f.ravel()) / n
    if len(h) == 1:
        return (1, 1)
    x = arange(product(shape(h)))
    w0 = cumsum(h)
    w1 = 1 - w0
    eps = 1e-10
    m0 = cumsum(x * h) / (w0 + eps)
    mt = m0[(-1)]
    m1 = (mt - m0[0:-1] * w0[0:-1]) / w1[0:-1]
    sB2 = w0[0:-1] * w1[0:-1] * (m0[0:-1] - m1) ** 2
    t = argmax(sB2)
    v = sB2[t]
    st2 = sum((x - mt) ** 2 * h)
    eta = v / st2
    return (t, eta)