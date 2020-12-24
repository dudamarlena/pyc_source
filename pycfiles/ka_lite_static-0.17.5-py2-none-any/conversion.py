# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/db/models/sql/conversion.py
# Compiled at: 2018-07-11 18:15:30
"""
This module holds simple classes used by GeoQuery.convert_values
to convert geospatial values from the database.
"""

class BaseField(object):
    empty_strings_allowed = True

    def get_internal_type(self):
        """Overloaded method so OracleQuery.convert_values doesn't balk."""
        return


class AreaField(BaseField):
    """Wrapper for Area values."""

    def __init__(self, area_att):
        self.area_att = area_att


class DistanceField(BaseField):
    """Wrapper for Distance values."""

    def __init__(self, distance_att):
        self.distance_att = distance_att


class GeomField(BaseField):
    """
    Wrapper for Geometry values.  It is a lightweight alternative to 
    using GeometryField (which requires a SQL query upon instantiation).
    """
    pass