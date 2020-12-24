# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iaffine3.py
# Compiled at: 2014-08-21 22:30:04


def iaffine3(f, T, interpol='CLOSEST', destshape='SAME', destorg=(0, )):
    import numpy as np
    from ia636 import iainterpollin
    from ia636 import iainterpolclosest
    if T.ndim != 2 or T.shape[0] != T.shape[1]:
        raise ValueError, 'T must be a square matrix'
    dim = T.shape[0] - 1
    if dim != 2 and dim != 3:
        raise ValueError, 'T must be either 3x3 or 4x4 (2D or 3D transform)'
    if f.ndim < dim:
        raise ValueError, 'dimention of f is not compatible with the transform matrix'
    cor = f.ndim > dim
    sht = f.shape[f.ndim - dim:]
    shh = f.shape[:f.ndim - dim]
    invT = np.linalg.inv(T.astype(np.float))
    shmin = np.asarray(destorg).astype(int)
    fshapecol = np.asarray(sht)
    fshapecol.shape = (dim, 1)
    if destshape == 'SAME':
        shmax = np.asarray(sht)
        shmin = np.zeros(1, int)
    elif destshape == 'FIT':
        if dim == 2:
            M = np.asarray([[0, 0, 1, 1], [0, 1, 0, 1]]).astype(float)
        else:
            M = np.asarray([[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]]).astype(float)
        M *= np.asarray(fshapecol) - 1
        M = np.vstack((M, np.ones((1, M.shape[1]))))
        M = np.dot(T, M)
        shmax = np.ceil(np.max(M, 1)[:-1]).astype(int)
        shmin = np.floor(np.min(M, 1)[:-1]).astype(int)
    else:
        shmin = np.asarray(destorg).astype(int)
        shmax = np.asarray(destshape).astype(int) + shmin
    shimincol = np.reshape(shmin, (shmin.shape[0], 1))
    ind = np.indices(shmax - shmin)
    ind.shape = (ind.shape[0], np.prod(ind.shape[1:]))
    ind += shimincol
    dstshape = tuple(shmax - shmin)
    tind = np.vstack((ind, np.ones((1, np.size(ind[0]))))).astype(float)
    oind = np.dot(invT, tind)
    oindr = oind.copy()
    oindr[:-1, :] = np.maximum(oind[:-1, :], 0)
    oindr[:-1, :] = np.minimum(oindr[:-1, :], fshapecol - 1)
    if interpol == 'LINEAR':
        interpolfunc = iainterpollin
    elif interpol == 'CLOSEST':
        interpolfunc = iainterpolclosest
    else:
        interpolfunc = interpol
    if cor:
        count = np.prod(shh)
        fr = np.reshape(f, (count,) + sht)
        interpshape = (count,) + (np.prod(dstshape),)
        g = np.empty(interpshape)
        for i in range(count):
            g[i] = interpolfunc(fr[i], oindr[0:-1, :])
            g[(i, np.not_equal(np.sum(np.not_equal(oindr, oind), 0), 0))] = 0

        g.shape = shh + dstshape
    else:
        g = interpolfunc(f, oindr[0:-1, :])
        g[np.not_equal(np.sum(np.not_equal(oindr, oind), 0), 0)] = 0
        g.shape = dstshape
    return g