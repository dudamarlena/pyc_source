# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/io/binary.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4223 bytes
from __future__ import absolute_import, division, print_function
import numpy as np, six, logging
logger = logging.getLogger(__name__)

def read_binary(filename, nx, ny, nz, dtype_str, headersize):
    """
    docstring, woo!

    Parameters
    ----------
    filename : String
        The name of the file to open
    nx : integer
        The number of data elements in the x-direction
    ny : integer
        The number of data elements in the y-direction
    nz : integer
        The number of data elements in the z-direction
    dtype_str : str
        A valid argument for np.dtype(some_str). See read_binary.dsize
        attribute
    headersize : integer
        The size of the file header in bytes

    Returns
    -------
    data : ndarray
            data.shape = (x, y, z) if z > 1
            data.shape = (x, y) if z == 1
            data.shape = (x,) if y == 1 && z == 1
    header : String
            header = file.read(headersize)
    """
    with open(filename, 'rb') as (opened_file):
        header = opened_file.read(headersize)
        data = np.fromfile(file=opened_file, dtype=np.dtype(dtype_str), count=-1)
    if nz is not 1:
        data.resize(nx, ny, nz)
    elif ny is not 1:
        data.resize(nx, ny)
    return (
     data, header)


read_binary.dtype_str = sorted(np.typeDict, key=str)