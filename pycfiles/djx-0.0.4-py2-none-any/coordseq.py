# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/prototypes/coordseq.py
# Compiled at: 2019-02-14 00:35:16
from ctypes import POINTER, c_double, c_int, c_uint
from django.contrib.gis.geos.libgeos import CS_PTR, GEOM_PTR, GEOSFuncFactory
from django.contrib.gis.geos.prototypes.errcheck import GEOSException, last_arg_byref

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


class CsInt(GEOSFuncFactory):
    """For coordinate sequence routines that return an integer."""
    argtypes = [
     CS_PTR, POINTER(c_uint)]
    restype = c_int
    errcheck = staticmethod(check_cs_get)


class CsOperation(GEOSFuncFactory):
    """For coordinate sequence operations."""
    restype = c_int

    def get_func(self, ordinate=False, get=False):
        if get:
            self.errcheck = check_cs_get
            dbl_param = POINTER(c_double)
        else:
            self.errcheck = check_cs_op
            dbl_param = c_double
        if ordinate:
            self.argtypes = [CS_PTR, c_uint, c_uint, dbl_param]
        else:
            self.argtypes = [
             CS_PTR, c_uint, dbl_param]
        return super(CsOperation, self).get_func()


class CsOutput(GEOSFuncFactory):
    restype = CS_PTR

    def get_func(self, argtypes):
        self.argtypes = argtypes
        return super(CsOutput, self).get_func()

    @staticmethod
    def errcheck(result, func, cargs):
        if not result:
            raise GEOSException('Error encountered checking Coordinate Sequence returned from GEOS C function "%s".' % func.__name__)
        return result


cs_clone = CsOutput('GEOSCoordSeq_clone', [CS_PTR])
create_cs = CsOutput('GEOSCoordSeq_create', [c_uint, c_uint])
get_cs = CsOutput('GEOSGeom_getCoordSeq', [GEOM_PTR])
cs_getordinate = CsOperation('GEOSCoordSeq_getOrdinate', ordinate=True, get=True)
cs_setordinate = CsOperation('GEOSCoordSeq_setOrdinate', ordinate=True)
cs_getx = CsOperation('GEOSCoordSeq_getX', get=True)
cs_gety = CsOperation('GEOSCoordSeq_getY', get=True)
cs_getz = CsOperation('GEOSCoordSeq_getZ', get=True)
cs_setx = CsOperation('GEOSCoordSeq_setX')
cs_sety = CsOperation('GEOSCoordSeq_setY')
cs_setz = CsOperation('GEOSCoordSeq_setZ')
cs_getsize = CsInt('GEOSCoordSeq_getSize')
cs_getdims = CsInt('GEOSCoordSeq_getDimensions')