# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/prototypes/misc.py
# Compiled at: 2018-07-11 18:15:30
"""
 This module is for the miscellaneous GEOS routines, particularly the
 ones that return the area, distance, and length.
"""
from ctypes import c_int, c_double, POINTER
from django.contrib.gis.geos.libgeos import GEOM_PTR, GEOS_PREPARE
from django.contrib.gis.geos.prototypes.errcheck import check_dbl, check_string
from django.contrib.gis.geos.prototypes.geom import geos_char_p
from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc
from django.utils.six.moves import xrange
__all__ = [
 'geos_area', 'geos_distance', 'geos_length']

def dbl_from_geom(func, num_geom=1):
    """
    Argument is a Geometry, return type is double that is passed
    in by reference as the last argument.
    """
    argtypes = [ GEOM_PTR for i in xrange(num_geom) ]
    argtypes += [POINTER(c_double)]
    func.argtypes = argtypes
    func.restype = c_int
    func.errcheck = check_dbl
    return func


geos_area = dbl_from_geom(GEOSFunc('GEOSArea'))
geos_distance = dbl_from_geom(GEOSFunc('GEOSDistance'), num_geom=2)
geos_length = dbl_from_geom(GEOSFunc('GEOSLength'))
if GEOS_PREPARE:
    geos_isvalidreason = GEOSFunc('GEOSisValidReason')
    geos_isvalidreason.argtypes = [GEOM_PTR]
    geos_isvalidreason.restype = geos_char_p
    geos_isvalidreason.errcheck = check_string
    __all__.append('geos_isvalidreason')