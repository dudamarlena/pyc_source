# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iahadamardmatrix.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iahadamardmatrix(N):
    from iameshgrid import iameshgrid

    def bitsum(x):
        s = 0 * x
        while x.any():
            s += x & 1
            x >>= 1

        return s

    n = floor(log(N) / log(2))
    if 2 ** n != N:
        raise Exception, 'error: size ' + str(N) + ' is not multiple of power of 2'
    u, x = iameshgrid(range(N), range(N))
    A = (-1) ** bitsum(x & u) / sqrt(N)
    return A