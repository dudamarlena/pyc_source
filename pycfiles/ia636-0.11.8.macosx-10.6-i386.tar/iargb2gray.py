# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iargb2gray.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iargb2gray(f):
    g = f[0, :, :] * 0.299 + f[1, :, :] * 0.587 + f[2, :, :] * 0.114
    return g.astype(f.dtype)