# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\file_helpers.py
# Compiled at: 2014-12-08 16:25:53
import h5py

def file_exists(filename):
    """
    Check if filename refers to an HDF5 file
    """
    if not isinstance(filename, str):
        raise TypeError('String expected.')
    result = False
    try:
        result = h5py.h5f.is_hdf5(filename)
    except Exception:
        pass

    return result