# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/write_netcdf.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 535 bytes
from netCDF4 import Dataset
from numpy import arange, dtype
nx = 4
ny = 4
nz = 1
ncfile = Dataset('test_xyz.nc', 'w')
data_out = arange(nx * ny * nz)
print(data_out)
data_out.shape = (nx, ny, nz)
ncfile.createDimension('x', nx)
ncfile.createDimension('y', ny)
ncfile.createDimension('z', nz)
data = ncfile.createVariable('data', dtype('float32').char, ('x', 'y', 'z'))
data[:] = data_out
print(ncfile.variables)
print('Wrote file!')