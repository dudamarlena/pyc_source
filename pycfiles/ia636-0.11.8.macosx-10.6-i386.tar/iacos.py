# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iacos.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iacos(s, t, theta, phi):
    r, c = np.indices(s)
    tc = t / np.cos(theta)
    tr = t / np.sin(theta)
    f = np.cos(2 * np.pi * (r / tr + c / tc) + phi)
    return f