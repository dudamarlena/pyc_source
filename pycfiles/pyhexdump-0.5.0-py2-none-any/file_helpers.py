# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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