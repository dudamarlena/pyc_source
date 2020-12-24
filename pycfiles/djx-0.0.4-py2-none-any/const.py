# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/gdal/raster/const.py
# Compiled at: 2019-02-14 00:35:16
"""
GDAL - Constant definitions
"""
from ctypes import c_double, c_float, c_int16, c_int32, c_ubyte, c_uint16, c_uint32
GDAL_PIXEL_TYPES = {0: 'GDT_Unknown', 
   1: 'GDT_Byte', 
   2: 'GDT_UInt16', 
   3: 'GDT_Int16', 
   4: 'GDT_UInt32', 
   5: 'GDT_Int32', 
   6: 'GDT_Float32', 
   7: 'GDT_Float64', 
   8: 'GDT_CInt16', 
   9: 'GDT_CInt32', 
   10: 'GDT_CFloat32', 
   11: 'GDT_CFloat64'}
GDAL_INTEGER_TYPES = [
 1, 2, 3, 4, 5]
GDAL_TO_CTYPES = [
 None, c_ubyte, c_uint16, c_int16, c_uint32, c_int32,
 c_float, c_double, None, None, None, None]
GDAL_RESAMPLE_ALGORITHMS = {'NearestNeighbour': 0, 
   'Bilinear': 1, 
   'Cubic': 2, 
   'CubicSpline': 3, 
   'Lanczos': 4, 
   'Average': 5, 
   'Mode': 6}