# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iasub2ind.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iasub2ind(dim, x, y):
    x, y = asarray(x), asarray(y)
    i = x * dim[1] + y
    i = i.astype(int32)
    return i