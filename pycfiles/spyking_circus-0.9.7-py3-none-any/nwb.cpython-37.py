# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/nwb.py
# Compiled at: 2020-03-11 05:17:13
# Size of source mod 2**32: 309 bytes
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