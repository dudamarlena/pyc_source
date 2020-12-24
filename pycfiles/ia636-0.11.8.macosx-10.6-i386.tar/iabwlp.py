# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iabwlp.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *
import string

def iabwlp(fsize, tc, n, option='circle'):
    from iafftshift import iafftshift

    def test_exp(x, y):
        try:
            return x ** (2 * y)
        except:
            return 1e+300

    rows, cols = fsize[0], fsize[1]
    mh, mw = rows / 2, cols / 2
    rr, cc = meshgrid(arange(-mh, rows - mh), arange(-mw, cols - mw), indexing='ij')
    if string.find(string.upper(option), 'SQUARE') != -1:
        H = 1.0 / (1.0 + (sqrt(2) - 1) * (maximum(abs(1.0 * rr / rows), abs(1.0 * cc / cols)) * tc) ** (2 * n))
    else:
        aux1 = ravel(sqrt((1.0 * rr / rows) ** 2 + (1.0 * cc / cols) ** 2) * tc)
        aux2 = 0.0 * aux1 + n
        aux = reshape(map(test_exp, aux1, aux2), cc.shape)
        H = 1.0 / (1 + (sqrt(2) - 1) * aux)
    H = iafftshift(H)
    return H