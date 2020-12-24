# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/emio.py
# Compiled at: 2016-11-29 20:56:28
"""

Created on Wed Jan 28 14:27:31 2015

@author: jingpeng
"""
import numpy as np, h5py, tifffile

def imread(fname):
    """
    Read volumetirc data.

    Args:
        fname: Name of the file to read (hdf5 or tiff).

    Returns:
        data: Numpy 3D or 4D array.
    """
    if '.hdf5' in fname or '.h5' in fname:
        f = h5py.File(fname)
        data = np.asarray(f['/main'])
        f.close()
    elif '.tif' in fname:
        data = tifffile.imread(fname)
    else:
        raise RuntimeError('only hdf5 and tiff formats are supported')
    return data


def imsave(data, fname):
    """
    Save volumetric data.

    Args:
        data: Numpy array to save.
        fname: Name of the file to save (hdf5 or tiff).
    """
    if '.hdf5' in fname or '.h5' in fname:
        f = h5py.File(fname)
        f.create_dataset('/main', data=data)
        f.close()
    elif '.tif' in fname:
        tifffile.imsave(fname, data)
    else:
        raise RuntimeError('only hdf5 and tiff formats are supported')