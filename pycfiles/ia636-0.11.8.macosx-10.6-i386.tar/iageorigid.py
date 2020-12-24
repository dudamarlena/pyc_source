# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iageorigid.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iageorigid(f, scale, theta, t):
    from iaffine import iaffine
    Ts = [
     [
      scale[1], 0, 0], [0, scale[0], 0], [0, 0, 1]]
    Trot = [[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]]
    Tx = [[1, 0, t[1]], [0, 1, t[0]], [0, 0, 1]]
    g = iaffine(f, dot(dot(Tx, Trot), Ts))
    return g