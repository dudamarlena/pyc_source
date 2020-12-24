# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iacorr.py
# Compiled at: 2014-08-21 22:30:04


def iacorr(im1, im2):
    import numpy as np
    avim1 = np.average(im1.astype(float).flat)
    avim2 = np.average(im2.astype(float).flat)
    im1x = im1.astype(float) - avim1
    im2x = im2.astype(float) - avim2
    cov = np.average(im1x * im2x)
    v1 = np.average(im1x * im1x)
    v2 = np.average(im2x * im2x)
    return cov / np.sqrt(v1 * v2)