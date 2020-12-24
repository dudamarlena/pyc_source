# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/ialog.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def ialog(s, mu, sigma):

    def test_exp(x, sigma):
        try:
            return exp(-(x / (2.0 * sigma ** 2)))
        except:
            return 0

    mu = array(mu)
    if product(shape(s)) == 1:
        x = arange(s)
        r2 = (x - mu) ** 2
    else:
        rr, cc = indices(s)
        r2 = (rr - mu[0]) ** 2 + (cc - mu[1]) ** 2
    r2_aux = ravel(r2)
    aux = reshape(map(test_exp, r2_aux, 0 * r2_aux + sigma), r2.shape)
    g = -((r2 - 2 * sigma ** 2) / (sigma ** 4 * pi) * aux)
    return g