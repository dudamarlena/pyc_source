# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaellipse.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *
import math

def iaellipse(s, r, c, theta=0):
    rows, cols = s[0], s[1]
    rr0, cc0 = c[0], c[1]
    rr, cc = meshgrid(range(rows), range(cols), indexing='ij')
    rr = rr - rr0
    cc = cc - cc0
    cos = math.cos(theta)
    sen = math.sin(theta)
    i = cos / r[1]
    j = sen / r[0]
    m = -sen / r[1]
    n = cos / r[0]
    g = (i * cc + m * rr) ** 2 + (j * cc + n * rr) ** 2 <= 1
    return g