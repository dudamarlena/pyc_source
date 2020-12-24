# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iadctmatrix.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iadctmatrix(N):
    from iameshgrid import iameshgrid
    x, u = iameshgrid(range(N), range(N))
    alpha = ones((N, N)) * sqrt(2.0 / N)
    alpha[0, :] = sqrt(1.0 / N)
    A = alpha * cos((2 * x + 1) * u * pi / (2.0 * N))
    return A