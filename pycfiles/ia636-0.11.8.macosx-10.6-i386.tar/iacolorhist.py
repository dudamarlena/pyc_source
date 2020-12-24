# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iacolorhist.py
# Compiled at: 2014-08-21 22:30:04


def iacolorhist(f, mask=None):
    import numpy as np
    from iahistogram import iahistogram
    WFRAME = 5
    f = np.asarray(f)
    if len(f.shape) == 1:
        f = f[np.newaxis, :]
    if not f.dtype == 'uint8':
        raise Exception, 'error, can only process uint8 images'
    if not f.shape[0] == 3:
        raise Exception, 'error, can only process 3-band images'
    r, g, b = f[0].astype(np.int), f[1].astype(np.int), f[2].astype(np.int)
    n_zeros = 0
    if mask:
        n_zeros = f.shape[0] * f.shape[1] - len(np.nonzero(np.ravel(mask)))
        r, g, b = mask * r, mask * g, mask * b
    hrg = np.zeros((256, 256), np.int32)
    hbg = hrg + 0
    hrb = hrg + 0
    img = 256 * r + g
    m1 = img.max()
    aux = iahistogram(img.astype(np.int32))
    aux[0] = aux[0] - n_zeros
    np.put(np.ravel(hrg), range(m1 + 1), aux)
    img = 256 * b + g
    m2 = img.max()
    aux = iahistogram(img.astype(np.int32))
    aux[0] = aux[0] - n_zeros
    np.put(np.ravel(hbg), range(m2 + 1), aux)
    img = 256 * r + b
    m3 = img.max()
    aux = iahistogram(img.astype(np.int32))
    aux[0] = aux[0] - n_zeros
    np.put(np.ravel(hrb), range(m3 + 1), aux)
    m = max(hrg.max(), hbg.max(), hrb.max())
    hc = m * np.ones((3 * WFRAME + 512, 3 * WFRAME + 512))
    hc[WFRAME:WFRAME + 256, WFRAME:WFRAME + 256] = np.transpose(hrg)
    hc[WFRAME:WFRAME + 256, 2 * WFRAME + 256:2 * WFRAME + 512] = np.transpose(hbg)
    hc[2 * WFRAME + 256:2 * WFRAME + 512, WFRAME:WFRAME + 256] = np.transpose(hrb)
    return hc