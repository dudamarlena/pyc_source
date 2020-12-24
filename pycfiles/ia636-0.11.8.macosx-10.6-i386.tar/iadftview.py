# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iadftview.py
# Compiled at: 2014-08-28 20:26:26
from numpy import *

def iadftview(F):
    from ia636 import iafftshift
    from ia636 import ianormalize
    FM = iafftshift(log(abs(F) + 1))
    return ianormalize(FM).astype(uint8)