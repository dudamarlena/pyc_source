# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaidft.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iaidft(F):
    from ia636 import iadftmatrix
    s = F.shape
    if len(F.shape) == 1:
        F = F[newaxis, newaxis, :]
    if len(F.shape) == 2:
        F = F[newaxis, :, :]
    p, m, n = F.shape
    A = iadftmatrix(m)
    B = iadftmatrix(n)
    C = iadftmatrix(p)
    Faux = dot(conjugate(A), F)
    Faux = dot(Faux, conjugate(B))
    f = dot(conjugate(C), Faux) / (sqrt(p) * sqrt(m) * sqrt(n))
    return f.reshape(s)