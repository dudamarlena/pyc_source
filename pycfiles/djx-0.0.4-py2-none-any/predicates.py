# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/prototypes/predicates.py
# Compiled at: 2019-02-14 00:35:16
"""
 This module houses the GEOS ctypes prototype functions for the
 unary and binary predicate operations on geometries.
"""
from ctypes import c_char, c_char_p, c_double
from django.contrib.gis.geos.libgeos import GEOM_PTR, GEOSFuncFactory
from django.contrib.gis.geos.prototypes.errcheck import check_predicate

class UnaryPredicate(GEOSFuncFactory):
    """For GEOS unary predicate functions."""
    argtypes = [
     GEOM_PTR]
    restype = c_char
    errcheck = staticmethod(check_predicate)


class BinaryPredicate(UnaryPredicate):
    """For GEOS binary predicate functions."""
    argtypes = [
     GEOM_PTR, GEOM_PTR]


geos_hasz = UnaryPredicate('GEOSHasZ')
geos_isclosed = UnaryPredicate('GEOSisClosed')
geos_isempty = UnaryPredicate('GEOSisEmpty')
geos_isring = UnaryPredicate('GEOSisRing')
geos_issimple = UnaryPredicate('GEOSisSimple')
geos_isvalid = UnaryPredicate('GEOSisValid')
geos_contains = BinaryPredicate('GEOSContains')
geos_covers = BinaryPredicate('GEOSCovers')
geos_crosses = BinaryPredicate('GEOSCrosses')
geos_disjoint = BinaryPredicate('GEOSDisjoint')
geos_equals = BinaryPredicate('GEOSEquals')
geos_equalsexact = BinaryPredicate('GEOSEqualsExact', argtypes=[GEOM_PTR, GEOM_PTR, c_double])
geos_intersects = BinaryPredicate('GEOSIntersects')
geos_overlaps = BinaryPredicate('GEOSOverlaps')
geos_relatepattern = BinaryPredicate('GEOSRelatePattern', argtypes=[GEOM_PTR, GEOM_PTR, c_char_p])
geos_touches = BinaryPredicate('GEOSTouches')
geos_within = BinaryPredicate('GEOSWithin')