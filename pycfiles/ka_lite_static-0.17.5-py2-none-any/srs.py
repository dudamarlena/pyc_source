# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/utils/srs.py
# Compiled at: 2018-07-11 18:15:30
from django.contrib.gis.gdal import SpatialReference

def add_srs_entry(srs, auth_name='EPSG', auth_srid=None, ref_sys_name=None, database=None):
    """
    This function takes a GDAL SpatialReference system and adds its information
    to the `spatial_ref_sys` table of the spatial backend.  Doing this enables
    database-level spatial transformations for the backend.  Thus, this utility
    is useful for adding spatial reference systems not included by default with
    the backend -- for example, the so-called "Google Maps Mercator Projection"
    is excluded in PostGIS 1.3 and below, and the following adds it to the
    `spatial_ref_sys` table:

    >>> from django.contrib.gis.utils import add_srs_entry
    >>> add_srs_entry(900913)

    Keyword Arguments:
     auth_name:
       This keyword may be customized with the value of the `auth_name` field.
       Defaults to 'EPSG'.

     auth_srid:
       This keyword may be customized with the value of the `auth_srid` field.
       Defaults to the SRID determined by GDAL.

     ref_sys_name:
       For SpatiaLite users only, sets the value of the `ref_sys_name` field.
       Defaults to the name determined by GDAL.

     database:
      The name of the database connection to use; the default is the value
      of `django.db.DEFAULT_DB_ALIAS` (at the time of this writing, it's value
      is 'default').
    """
    from django.db import connections, DEFAULT_DB_ALIAS
    if not database:
        database = DEFAULT_DB_ALIAS
    connection = connections[database]
    if not hasattr(connection.ops, 'spatial_version'):
        raise Exception('The `add_srs_entry` utility only works with spatial backends.')
    if connection.ops.oracle or connection.ops.mysql:
        raise Exception('This utility does not support the Oracle or MySQL spatial backends.')
    SpatialRefSys = connection.ops.spatial_ref_sys()
    if not isinstance(srs, SpatialReference):
        srs = SpatialReference(srs)
    if srs.srid is None:
        raise Exception('Spatial reference requires an SRID to be compatible with the spatial backend.')
    kwargs = {'srid': srs.srid, 'auth_name': auth_name, 
       'auth_srid': auth_srid or srs.srid, 
       'proj4text': srs.proj4}
    if connection.ops.postgis:
        kwargs['srtext'] = srs.wkt
    if connection.ops.spatialite:
        kwargs['ref_sys_name'] = ref_sys_name or srs.name
    try:
        sr = SpatialRefSys.objects.using(database).get(srid=srs.srid)
    except SpatialRefSys.DoesNotExist:
        sr = SpatialRefSys.objects.using(database).create(**kwargs)

    return


add_postgis_srs = add_srs_entry