# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iapca.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iapca(X):
    n, dim = X.shape
    mu = X.mean(axis=0)
    X = X - mu
    C = np.dot(X.T, X) / (n - 1)
    e, V = np.linalg.eigh(C)
    indexes = np.argsort(e)[::-1]
    e = e[indexes]
    V = V[:, indexes]
    return (V, e, mu)