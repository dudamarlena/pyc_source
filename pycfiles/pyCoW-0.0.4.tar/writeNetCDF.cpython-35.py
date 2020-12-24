# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/writeNetCDF.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 524 bytes
from netCDF4 import Dataset
from numpy import arange, dtype
nx = 4
ny = 4
nz = 4
ncfile = Dataset('test_xy.nc', 'w')
data_out = arange(nx * ny)
print(data_out)
data_out.shape = (nx, ny)
ncfile.createDimension('x', nx)
ncfile.createDimension('y', ny)
data = ncfile.createVariable('data', dtype('float32').char, ('x', 'y'))
data[:] = data_out
print(ncfile.variables)
print('Wrote file!')