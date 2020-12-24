# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iamosaic.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *
import scipy

def iamosaic(f, N, s=1.0):
    f = asarray(f)
    d, h, w = f.shape
    nLines = ceil(float(d) / N)
    nCells = nLines * N
    fullf = resize(f, (nCells, h, w))
    fullf[d:nCells, :, :] = 0
    Y, X = indices((nLines * h, N * w))
    Pts = array([
     (floor(Y / h) * N + floor(X / w)).ravel(),
     mod(Y, h).ravel(),
     mod(X, w).ravel()]).astype(int).reshape((3, nLines * h, N * w))
    g = scipy.ndimage.interpolation.zoom(fullf[(Pts[0], Pts[1], Pts[2])], s, order=5)
    return g