# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaapplylut.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iaapplylut(fi, it):
    g = it[fi]
    if len(g.shape) == 3:
        aux = zeros((3, g.shape[0], g.shape[1]), fi.dtype.name)
        for i in range(3):
            aux[i, :, :] = g[:, :, i]

        g = aux
    return g