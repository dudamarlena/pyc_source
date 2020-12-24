# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/prototypes/coordseq.py
# Compiled at: 2018-07-11 18:15:30
from ctypes import c_double, c_int, c_uint, POINTER
from django.contrib.gis.geos.libgeos import GEOM_PTR, CS_PTR
from django.contrib.gis.geos.prototypes.errcheck import last_arg_byref, GEOSException
from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc

def check_cs_ptr(result, func, cargs):
    """Error checking on routines that return Geometries."""
    if not result:
        raise GEOSException('Error encountered checking Coordinate Sequence returned from GEOS C function "%s".' % func.__name__)
    return result


def check_cs_op(result, func, cargs):
    """Checks the status code of a coordinate sequence operation."""
    if result == 0:
        raise GEOSException('Could not set value on coordinate sequence')
    else:
        return result


def check_cs_get(result, func, cargs):
    """Checking the coordinate sequence retrieval."""
    check_cs_op(result, func, cargs)
    return last_arg_byref(cargs)


def cs_int(func):
    """For coordinate sequence routines that return an integer."""
    func.argtypes = [
     CS_PTR, POINTER(c_uint)]
    func.restype = c_int
    func.errcheck = check_cs_get
    return func


def cs_operation(func, ordinate=False, get=False):
    """For coordinate sequence operations."""
    if get:
        func.errcheck = check_cs_get
        dbl_param = POINTER(c_double)
    else:
        func.errcheck = check_cs_op
        dbl_param = c_double
    if ordinate:
        func.argtypes = [CS_PTR, c_uint, c_uint, dbl_param]
    else:
        func.argtypes = [
         CS_PTR, c_uint, dbl_param]
    func.restype = c_int
    return func


def cs_output(func, argtypes):
    """For routines that return a coordinate sequence."""
    func.argtypes = argtypes
    func.restype = CS_PTR
    func.errcheck = check_cs_ptr
    return func


cs_clone = cs_output(GEOSFunc('GEOSCoordSeq_clone'), [CS_PTR])
create_cs = cs_output(GEOSFunc('GEOSCoordSeq_create'), [c_uint, c_uint])
get_cs = cs_output(GEOSFunc('GEOSGeom_getCoordSeq'), [GEOM_PTR])
cs_getordinate = cs_operation(GEOSFunc('GEOSCoordSeq_getOrdinate'), ordinate=True, get=True)
cs_setordinate = cs_operation(GEOSFunc('GEOSCoordSeq_setOrdinate'), ordinate=True)
cs_getx = cs_operation(GEOSFunc('GEOSCoordSeq_getX'), get=True)
cs_gety = cs_operation(GEOSFunc('GEOSCoordSeq_getY'), get=True)
cs_getz = cs_operation(GEOSFunc('GEOSCoordSeq_getZ'), get=True)
cs_setx = cs_operation(GEOSFunc('GEOSCoordSeq_setX'))
cs_sety = cs_operation(GEOSFunc('GEOSCoordSeq_setY'))
cs_setz = cs_operation(GEOSFunc('GEOSCoordSeq_setZ'))
cs_getsize = cs_int(GEOSFunc('GEOSCoordSeq_getSize'))
cs_getdims = cs_int(GEOSFunc('GEOSCoordSeq_getDimensions'))