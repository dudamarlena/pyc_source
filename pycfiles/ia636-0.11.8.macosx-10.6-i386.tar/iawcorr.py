# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iawcorr.py
# Compiled at: 2014-08-21 22:30:04


def iawcorr(im1, im2, w):
    import numpy as np
    w = w.astype(float)
    wf = w.ravel()
    sw = np.sum(wf)
    im1f = im1.astype(float).ravel()
    im2f = im2.astype(float).ravel()
    mim1f = np.sum(im1f * wf) / sw
    mim2f = np.sum(im2f * wf) / sw
    im1x = im1f - mim1f
    im2x = im2f - mim2f
    cov12 = np.sum(im1x * im2x * wf) / sw
    cov11 = np.sum(im1x * im1x * wf) / sw
    cov22 = np.sum(im2x * im2x * wf) / sw
    return cov12 / np.sqrt(cov11 * cov22)