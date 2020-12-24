# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/io/netcdf/_constants.py
# Compiled at: 2015-03-08 15:32:37
_DIMENSION_NAMES = [
 'ni', 'nj', 'nk']
_AXES_NAMES = ['x', 'y', 'z']
_NP_TO_NC_TYPE = {'float32': 'f4', 
   'float64': 'f8', 
   'int8': 'i1', 
   'int16': 'i2', 
   'int32': 'i4', 
   'int64': 'i8', 
   'uint8': 'u1', 
   'uint16': 'u2', 
   'uint32': 'u4', 
   'uint64': 'u8', 
   'bool': 'i1'}
_AXIS_DIMENSION_NAMES = [
 'nk', 'nj', 'ni']
_AXIS_COORDINATE_NAMES = ['z', 'y', 'x']
_DIMENSION_NAMES = set(_AXIS_DIMENSION_NAMES + ['nt'])
_COORDINATE_NAMES = set(_AXIS_COORDINATE_NAMES + ['t'])