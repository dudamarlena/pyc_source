# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iahaarmatrix.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iahaarmatrix(N):
    from iameshgrid import iameshgrid
    n = floor(log(N) / log(2))
    if 2 ** n != N:
        raise Exception, 'error: size ' + str(N) + ' is not multiple of power of 2'
    z, k = iameshgrid(1.0 * arange(N) / N, 1.0 * arange(N))
    p = floor(log(maximum(1, k)) / log(2))
    q = k - 2 ** p + 1
    z1 = (q - 1) / 2 ** p
    z2 = (q - 0.5) / 2 ** p
    z3 = q / 2 ** p
    A = 1 / sqrt(N) * (2 ** (p / 2.0) * ((z >= z1) & (z < z2)) + -2 ** (p / 2.0) * ((z >= z2) & (z < z3)))
    A[0, :] = 1 / sqrt(N)
    return A