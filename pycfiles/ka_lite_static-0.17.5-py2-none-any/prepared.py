# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/prototypes/prepared.py
# Compiled at: 2018-07-11 18:15:30
from ctypes import c_char
from django.contrib.gis.geos.libgeos import GEOM_PTR, PREPGEOM_PTR
from django.contrib.gis.geos.prototypes.errcheck import check_predicate
from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc
geos_prepare = GEOSFunc('GEOSPrepare')
geos_prepare.argtypes = [GEOM_PTR]
geos_prepare.restype = PREPGEOM_PTR
prepared_destroy = GEOSFunc('GEOSPreparedGeom_destroy')
prepared_destroy.argtpes = [PREPGEOM_PTR]
prepared_destroy.restype = None

def prepared_predicate(func):
    func.argtypes = [
     PREPGEOM_PTR, GEOM_PTR]
    func.restype = c_char
    func.errcheck = check_predicate
    return func


prepared_contains = prepared_predicate(GEOSFunc('GEOSPreparedContains'))
prepared_contains_properly = prepared_predicate(GEOSFunc('GEOSPreparedContainsProperly'))
prepared_covers = prepared_predicate(GEOSFunc('GEOSPreparedCovers'))
prepared_intersects = prepared_predicate(GEOSFunc('GEOSPreparedIntersects'))