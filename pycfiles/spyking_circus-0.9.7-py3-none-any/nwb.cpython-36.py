# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/nwb.py
# Compiled at: 2018-05-04 09:08:14
# Size of source mod 2**32: 345 bytes
import numpy, re, sys
from .hdf5 import H5File
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    import h5py

class NWBFile(H5File):
    description = 'nwb'
    extension = ['.nwb', '.h5', '.hdf5']
    parallel_write = h5py.get_config().mpi
    is_writable = True