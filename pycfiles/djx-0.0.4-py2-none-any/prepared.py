# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/geos/prototypes/prepared.py
# Compiled at: 2019-02-14 00:35:16
from ctypes import c_char
from django.contrib.gis.geos.libgeos import GEOM_PTR, PREPGEOM_PTR, GEOSFuncFactory
from django.contrib.gis.geos.prototypes.errcheck import check_predicate
geos_prepare = GEOSFuncFactory('GEOSPrepare', argtypes=[GEOM_PTR], restype=PREPGEOM_PTR)
prepared_destroy = GEOSFuncFactory('GEOSPreparedGeom_destroy', argtypes=[PREPGEOM_PTR])

class PreparedPredicate(GEOSFuncFactory):
    argtypes = [
     PREPGEOM_PTR, GEOM_PTR]
    restype = c_char
    errcheck = staticmethod(check_predicate)


prepared_contains = PreparedPredicate('GEOSPreparedContains')
prepared_contains_properly = PreparedPredicate('GEOSPreparedContainsProperly')
prepared_covers = PreparedPredicate('GEOSPreparedCovers')
prepared_crosses = PreparedPredicate('GEOSPreparedCrosses')
prepared_disjoint = PreparedPredicate('GEOSPreparedDisjoint')
prepared_intersects = PreparedPredicate('GEOSPreparedIntersects')
prepared_overlaps = PreparedPredicate('GEOSPreparedOverlaps')
prepared_touches = PreparedPredicate('GEOSPreparedTouches')
prepared_within = PreparedPredicate('GEOSPreparedWithin')