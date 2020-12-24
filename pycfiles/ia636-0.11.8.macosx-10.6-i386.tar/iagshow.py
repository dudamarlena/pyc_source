# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iagshow.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iagshow(X, X1=None, X2=None, X3=None, X4=None, X5=None, X6=None):
    if X.dtype == np.bool:
        X = np.where(X, 255, 0).astype('uint8')
    r = X
    g = X
    b = X
    if X1 is not None:
        if X1.dtype != np.bool:
            raise Exception, 'X1 must be binary overlay'
        r = np.where(X1, 255, r)
        g = np.where(~X1, g, 0)
        b = np.where(~X1, b, 0)
    if X2 is not None:
        if X2.dtype != np.bool:
            raise Exception, 'X2 must be binary overlay'
        r = np.where(~X2, r, 0)
        g = np.where(X2, 255, g)
        b = np.where(~X2, b, 0)
    if X3 is not None:
        if X3.dtype != np.bool:
            raise Exception, 'X3 must be binary overlay'
        r = np.where(~X3, r, 0)
        g = np.where(~X3, g, 0)
        b = np.where(X3, 255, b)
    if X4 is not None:
        if X4.dtype != np.bool:
            raise Exception, 'X4 must be binary overlay'
        r = np.where(X4, 255, r)
        g = np.where(~X4, g, 0)
        b = np.where(X4, 255, b)
    if X5 is not None:
        if X5.dtype != np.bool:
            raise Exception, 'X5 must be binary overlay'
        r = np.where(X5, 255, r)
        g = np.where(X5, 255, g)
        b = np.where(~X5, b, 0)
    if X6 is not None:
        if X6.dtype != np.bool:
            raise Exception, 'X6 must be binary overlay'
        r = np.where(~X6, r, 0)
        g = np.where(X6, 255, g)
        b = np.where(X6, 255, b)
    return np.array([r, g, b])