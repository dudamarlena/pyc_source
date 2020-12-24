# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iacomb.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iacomb(s, delta, offset):
    s = asarray(s)
    if product(s.shape) == 1:
        g = zeros(s)
        g[offset::delta] = 1
    elif s.size >= 2:
        g = zeros((s[0], s[1]))
        g[offset[0]::delta[0], offset[1]::delta[1]] = 1
    if s.size == 3:
        aux = zeros(s)
        for i in range(offset[2], s[2], delta[2]):
            aux[:, :, i] = g

        g = aux
    return g