# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iacrop.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iacrop(f, side='all', color='black'):
    from ianeg import ianeg
    f = asarray(f)
    if len(f.shape) == 1:
        f = f[newaxis, :]
    if color == 'white':
        f = ianeg(f)
    aux1, aux2 = sometrue(f, 0), sometrue(f, 1)
    col, row = flatnonzero(aux1), flatnonzero(aux2)
    if side == 'left':
        g = f[:, col[0]::]
    elif side == 'right':
        g = f[:, 0:col[(-1)] + 1]
    elif side == 'top':
        g = f[row[0]::, :]
    elif side == 'bottom':
        g = f[0:row[(-1)] + 1, :]
    else:
        g = f[row[0]:row[(-1)] + 1, col[0]:col[(-1)] + 1]
    if color == 'white':
        g = ianeg(g)
    return g