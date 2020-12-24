# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/ianshow.py
# Compiled at: 2014-08-21 22:30:04
import ia636 as ia, numpy as np

def t(s, dt=1):
    a = ia.iatext(s)
    b = np.pad(a, ((9 - dt, 9 - dt), (3 - dt, 3 - dt)), 'constant', constant_values=((False, False), (False, False)))
    c = np.pad(b, ((dt, dt), (dt, dt)), 'constant', constant_values=((True, True), (True, True)))
    return c


def timg(f, dt=1):
    tFalse = t('   ', dt)
    dy, dx = tFalse.shape
    tTrue = np.zeros_like(tFalse)
    z = np.empty(tuple(np.array(f.shape) * np.array([dy, dx]))).astype(bool)
    if f.dtype == 'bool':
        for x in np.arange(f.shape[(-1)]):
            for y in np.arange(f.shape[(-2)]):
                if f[(y, x)]:
                    z[y * dy:y * dy + dy, x * dx:x * dx + dx] = tFalse
                else:
                    z[y * dy:y * dy + dy, x * dx:x * dx + dx] = tTrue

        z = ~np.pad(z, ((1, 1), (1, 1)), 'constant')
    else:
        for x in np.arange(f.shape[(-1)]):
            for y in np.arange(f.shape[(-2)]):
                z[y * dy:y * dy + dy, x * dx:x * dx + dx] = t('%3d' % f[(y, x)], dt)

        z = np.pad(~z, ((1, 1), (1, 1)), 'constant')
    return z


def ianshow(X, X1=None, X2=None, X3=None, X4=None, X5=None, X6=None):
    x = timg(X)
    x1, x2, x3, x4, x5, x6 = (None, None, None, None, None, None)
    if X1 is not None:
        x1 = ~timg(X1, 3)
    if X2 is not None:
        x2 = ~timg(X2, 3)
    if X3 is not None:
        x3 = ~timg(X3, 3)
    if X4 is not None:
        x4 = ~timg(X4, 3)
    if X5 is not None:
        x5 = ~timg(X5, 3)
    if X6 is not None:
        x6 = ~timg(X6, 3)
    return ia.iagshow(x, x1, x2, x3, x4, x5, x6)