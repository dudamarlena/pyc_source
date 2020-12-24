# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/prototypes/geom.py
# Compiled at: 2019-02-14 00:35:16
from ctypes import POINTER, c_char_p, c_int, c_size_t, c_ubyte
from django.contrib.gis.geos.libgeos import CS_PTR, GEOM_PTR, GEOSFuncFactory
from django.contrib.gis.geos.prototypes.errcheck import check_geom, check_minus_one, check_sized_string, check_string, check_zero
c_uchar_p = POINTER(c_ubyte)

class geos_char_p(c_char_p):
    pass


class BinConstructor(GEOSFuncFactory):
    """Generates a prototype for binary construction (HEX, WKB) GEOS routines."""
    argtypes = [
     c_char_p, c_size_t]
    restype = GEOM_PTR
    errcheck = staticmethod(check_geom)


class BinOutput(GEOSFuncFactory):
    """Generates a prototype for the routines that return a sized string."""
    argtypes = [
     GEOM_PTR, POINTER(c_size_t)]
    restype = c_uchar_p
    errcheck = staticmethod(check_sized_string)


class GeomOutput(GEOSFuncFactory):
    """For GEOS routines that return a geometry."""
    restype = GEOM_PTR
    errcheck = staticmethod(check_geom)

    def get_func(self, argtypes):
        self.argtypes = argtypes
        return super(GeomOutput, self).get_func()


class IntFromGeom(GEOSFuncFactory):
    """Argument is a geometry, return type is an integer."""
    argtypes = [
     GEOM_PTR]
    restype = c_int

    def get_func(self, zero=False):
        if zero:
            self.errcheck = check_zero
        else:
            self.errcheck = check_minus_one
        return super(IntFromGeom, self).get_func()


class StringFromGeom(GEOSFuncFactory):
    """Argument is a Geometry, return type is a string."""
    argtypes = [
     GEOM_PTR]
    restype = geos_char_p
    errcheck = staticmethod(check_string)


from_hex = BinConstructor('GEOSGeomFromHEX_buf')
from_wkb = BinConstructor('GEOSGeomFromWKB_buf')
from_wkt = GeomOutput('GEOSGeomFromWKT', [c_char_p])
to_hex = BinOutput('GEOSGeomToHEX_buf')
to_wkb = BinOutput('GEOSGeomToWKB_buf')
to_wkt = StringFromGeom('GEOSGeomToWKT')
geos_normalize = IntFromGeom('GEOSNormalize')
geos_type = StringFromGeom('GEOSGeomType')
geos_typeid = IntFromGeom('GEOSGeomTypeId')
get_dims = GEOSFuncFactory('GEOSGeom_getDimensions', argtypes=[GEOM_PTR], restype=c_int)
get_num_coords = IntFromGeom('GEOSGetNumCoordinates')
get_num_geoms = IntFromGeom('GEOSGetNumGeometries')
create_point = GeomOutput('GEOSGeom_createPoint', [CS_PTR])
create_linestring = GeomOutput('GEOSGeom_createLineString', [CS_PTR])
create_linearring = GeomOutput('GEOSGeom_createLinearRing', [CS_PTR])
create_polygon = GeomOutput('GEOSGeom_createPolygon', None)
create_empty_polygon = GeomOutput('GEOSGeom_createEmptyPolygon', None)
create_collection = GeomOutput('GEOSGeom_createCollection', None)
get_extring = GeomOutput('GEOSGetExteriorRing', [GEOM_PTR])
get_intring = GeomOutput('GEOSGetInteriorRingN', [GEOM_PTR, c_int])
get_nrings = IntFromGeom('GEOSGetNumInteriorRings')
get_geomn = GeomOutput('GEOSGetGeometryN', [GEOM_PTR, c_int])
geom_clone = GEOSFuncFactory('GEOSGeom_clone', argtypes=[GEOM_PTR], restype=GEOM_PTR)
destroy_geom = GEOSFuncFactory('GEOSGeom_destroy', argtypes=[GEOM_PTR])
geos_get_srid = GEOSFuncFactory('GEOSGetSRID', argtypes=[GEOM_PTR], restype=c_int)
geos_set_srid = GEOSFuncFactory('GEOSSetSRID', argtypes=[GEOM_PTR, c_int])