# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alonso/Science/Codes/ReformCodes/NaMaster/test/testutils.py
# Compiled at: 2019-12-25 17:21:57
# Size of source mod 2**32: 525 bytes
import numpy as np

def normdiff(v1, v2):
    return np.amax(np.fabs(v1 - v2))


def read_flat_map(filename, i_map=0):
    """
    Reads a flat-sky map and the details of its pixelization scheme.
    The latter are returned as a FlatMapInfo object.
    i_map : map to read. If -1, all maps will be read.
    """
    from astropy.io import fits
    from astropy.wcs import WCS
    hdul = fits.open(filename)
    w = WCS(hdul[0].header)
    maps = hdul[i_map].data
    ny, nx = maps.shape
    hdul.close()
    return (
     w, maps)