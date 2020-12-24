# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaisdftsym.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iaisdftsym(F):
    if len(F.shape) == 1:
        F = F[newaxis, newaxis, :]
    if len(F.shape) == 2:
        F = F[newaxis, :, :]
    n, m, p = F.shape
    x, y, z = indices((n, m, p))
    Xnovo = mod(-1 * x, n)
    Ynovo = mod(-1 * y, m)
    Znovo = mod(-1 * z, p)
    aux = conjugate(F[(Xnovo, Ynovo, Znovo)])
    return alltrue(abs(F - aux) < 0.001)