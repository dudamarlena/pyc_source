# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iadftmatrix.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iadftmatrix(N):
    x = arange(N).reshape(N, 1)
    u = x
    Wn = exp(complex(0.0, -2.0) * pi / N)
    A = 1.0 / sqrt(N) * Wn ** dot(u, x.T)
    return A