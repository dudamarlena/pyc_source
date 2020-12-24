# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/io/test_partial_h5.py
# Compiled at: 2019-11-30 21:58:33
# Size of source mod 2**32: 921 bytes
"""
This script creates a partial h5py file then tests the process class with it.
Created on: Jul 12, 2019
Author: Emily Costa

from tests.io.data_utils import make_sparse_sampling_file
import pyUSID as usid
from pyUSID.io import dtype_utils, hdf_utils
import h5py
import numpy as np
from tests.io.simple_process import SimpleProcess
import os

# Creates incomplete h5py dataset object in current path
h5_path = 'sparse_sampling.h5'
if not os.path.exists(h5_path):
    make_sparse_sampling_file()
h5_f = h5py.File(h5_path, mode='r+')
hdf_utils.print_tree(h5_f)
h5_main0 = h5_f['Measurement_000/Channel_000/Raw_Data']
h5_main1 = h5_f['Measurement_000/Channel_001/Raw_Data']

print(hdf_utils.simple.check_if_main(h5_main0, verbose=True))
#dtype_utils.check_dtype(h5_maini)

if __name__ == '__main__':
    simp = SimpleProcess(h5_main0)
    #print(simp.test())
    #simp.test()
    #simp.plot_test()
    simp.compute()
"""