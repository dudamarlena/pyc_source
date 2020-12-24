# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iarectangle.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iarectangle(s, r, c):
    rows, cols = s[0], s[1]
    rrows, rcols = r[0], r[1]
    rr0, cc0 = c[0], c[1]
    rr, cc = meshgrid(range(rows), range(cols), indexing='ij')
    min_row, max_row = rr0 - rrows / 2.0, rr0 + rrows / 2.0
    min_col, max_col = cc0 - rcols / 2.0, cc0 + rcols / 2.0
    g1 = (min_row <= rr) & (max_row > rr)
    g2 = (min_col <= cc) & (max_col > cc)
    g = g1 & g2
    return g