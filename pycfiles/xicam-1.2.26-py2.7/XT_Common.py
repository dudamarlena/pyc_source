# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\tomography\tomocam\XT_Common.py
# Compiled at: 2018-08-27 17:21:07
import numpy as np, tomopy, afnumpy as afnp

def padmat(x, siz, value):
    n = siz[0]
    if siz.size < 2:
        m = n
    elif siz.size == 2:
        m = siz[1]
    else:
        n, m = siz.shape
    N, M = x.shape
    y = np.zeros((n, m)) + value
    y[0:N, 0:M] = x
    y = np.roll(np.roll(y, np.int16(np.fix((n - N) / 2)), axis=0), np.int16(np.fix((m - M) / 2)), axis=1)
    return y


def padmat_v2(x, siz, value, y):
    n = siz[0]
    if siz.size < 2:
        m = n
    elif siz.size == 2:
        m = siz[1]
    else:
        n, m = siz.shape
    N, M = x.shape
    y[0:N, 0:M] = x
    y = np.roll(np.roll(y, afnp.int16(np.fix((n - N) / 2)), axis=0), np.int16(afnp.fix((m - M) / 2)), axis=1)
    return y