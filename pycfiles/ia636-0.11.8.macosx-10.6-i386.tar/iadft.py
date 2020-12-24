# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iadft.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iadft(f):
    from ia636 import iadftmatrix
    f = asarray(f).astype(float64)
    if len(f.shape) == 1:
        m = len(f)
        A = iadftmatrix(f.shape[0])
        F = sqrt(m) * dot(A, f)
    elif len(f.shape) == 2:
        m, n = f.shape
        A = iadftmatrix(m)
        B = iadftmatrix(n)
        F = sqrt(m * n) * dot(dot(A, f), B)
    else:
        p, m, n = f.shape
        A = iadftmatrix(m)
        B = iadftmatrix(n)
        C = iadftmatrix(p)
        Faux = dot(A, f)
        Faux = dot(Faux, B)
        F = sqrt(p) * sqrt(m) * sqrt(n) * dot(C, Faux)
    return F