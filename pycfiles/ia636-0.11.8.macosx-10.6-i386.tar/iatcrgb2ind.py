# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iatcrgb2ind.py
# Compiled at: 2014-08-21 22:30:04
import numpy as np

def iatcrgb2ind(f):
    f = np.asarray(f)
    r, g, b = f[0].astype(np.int), f[1].astype(np.int), f[2].astype(np.int)
    c = r + 256 * g + 65536 * b
    t, i = np.unique(c, return_inverse=True)
    n = len(t)
    rt = np.reshape(map(lambda k: int(k % 256), t), (n, 1))
    gt = np.reshape(map(lambda k: int(k % 65536 / 256.0), t), (n, 1))
    bt = np.reshape(map(lambda k: int(k), t / 65536.0), (n, 1))
    cm = np.concatenate((rt, gt, bt), axis=1)
    fi = i.reshape(r.shape)
    return (fi, cm)