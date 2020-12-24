# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Utilities/init_multigrid.py
# Compiled at: 2017-06-20 08:49:49
from scipy.interpolate import RegularGridInterpolator as rgi
from numpy.lib.stride_tricks import as_strided
import numpy as np

def init_multigrid(proj, geo, alpha, alg):
    if alg == 'SART':
        from Algorithms.SART import SART as italg
    if alg == 'SIRT':
        from Algorithms.SIRT import SIRT as italg
    finalsize = geo.nVoxel
    maxval = max(proj.ravel())
    minval = min(proj.ravel())
    geo.nVoxel = np.array([16, 16, 16])
    geo.dVoxel = geo.sVoxel / geo.nVoxel
    if (geo.nVoxel > finalsize).all():
        return np.zeros(finalsize, dtype=np.float32)
    niter = 100
    initres = np.zeros(geo.nVoxel, dtype=np.float32)
    while (geo.nVoxel != finalsize).all():
        geo.dVoxel = geo.sVoxel / geo.nVoxel
        initres = italg(proj, geo, alpha, niter, init=initres, verbose=False)
        geo.nVoxel = geo.nVoxel * 2
        geo.nVoxel[geo.nVoxel > finalsize] = finalsize[(geo.nVoxel > finalsize)]
        geo.dVoxel = geo.sVoxel / geo.nVoxel
        x, y, z = np.linspace(minval, maxval, geo.nVoxel[0] / 2, dtype=np.float32), np.linspace(minval, maxval, geo.nVoxel[1] / 2, dtype=np.float32), np.linspace(minval, maxval, geo.nVoxel[2] / 2, dtype=np.float32)
        xv, yv, zv = tile_array(tile_array(x, 2), geo.nVoxel[0] ** 2), tile_array(tile_array(y, 2), geo.nVoxel[0] ** 2), tile_array(tile_array(x, 2), geo.nVoxel[0] ** 2)
        initres = rgi((x, y, z), initres)(np.column_stack((xv, yv, zv)))
        initres = initres.reshape(geo.nVoxel)

    return initres


def tile_array(mat, b1):
    r, = mat.shape
    rs, = mat.strides
    x = as_strided(mat, (r, b1), (rs, 0))
    return x.reshape(r * b1)