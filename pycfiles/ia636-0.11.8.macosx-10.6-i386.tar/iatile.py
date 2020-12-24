# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iatile.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iatile(f, new_size):
    f = asarray(f)
    if len(f.shape) == 1:
        f = f[newaxis, :]
    aux = resize(f, (new_size[0], f.shape[1]))
    aux = transpose(aux)
    aux = resize(aux, (new_size[1], new_size[0]))
    g = transpose(aux)
    return g