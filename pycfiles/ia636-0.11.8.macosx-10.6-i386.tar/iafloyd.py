# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iafloyd.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iafloyd(f):
    from ianormalize import ianormalize
    f_ = 1.0 * ianormalize(f, [0, 255])
    g = zeros(f_.shape)
    for i in range(f_.shape[0]):
        for j in range(f_.shape[1]):
            if f_[(i, j)] >= 128:
                g[(i, j)] = 255
            erro = f_[(i, j)] - g[(i, j)]
            if j < f_.shape[1] - 1:
                f_[(i, j + 1)] = f_[(i, j + 1)] + 7 * erro / 16.0
            if i < f_.shape[0] - 1 and j > 0:
                f_[(i + 1, j - 1)] = f_[(i + 1, j - 1)] + 3 * erro / 16.0
            if i < f_.shape[0] - 1:
                f_[(i + 1, j)] = f_[(i + 1, j)] + 5 * erro / 16.0
            if i < f_.shape[0] - 1 and j < f_.shape[1] - 1:
                f_[(i + 1, j + 1)] = f_[(i + 1, j + 1)] + erro / 16.0

    g = g > 0
    return g