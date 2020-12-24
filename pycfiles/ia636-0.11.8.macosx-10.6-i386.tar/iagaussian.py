# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iagaussian.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iagaussian(s, mu, cov):
    d = len(s)
    n = np.prod(s)
    x = np.indices(s).reshape((d, n))
    xc = x - mu
    k = 1.0 * xc * np.dot(np.linalg.inv(cov), xc)
    k = np.sum(k, axis=0)
    g = 1.0 / ((2 * np.pi) ** (d / 2.0) * np.sqrt(np.linalg.det(cov))) * np.exp(-1.0 / 2 * k)
    return g.reshape(s)