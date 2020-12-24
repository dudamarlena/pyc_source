# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iapad.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iapad(f, thick=[
 1, 1], value=0):
    f, thick = asarray(f), asarray(thick)
    g = (value * ones(array(f.shape) + 2 * thick)).astype(f.dtype.char)
    g[thick[0]:-thick[0], thick[1]:-thick[1]] = f
    return g