# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Pycharm\PycharmProjects\locationfield\mapbox_location_field\spatial\forms.py
# Compiled at: 2019-11-08 16:11:11
# Size of source mod 2**32: 1039 bytes
from django.contrib.gis.forms import PointField, ValidationError
from django.contrib.gis.geos import Point
from ..forms import parse_location
from ..widgets import MapInput

class SpatialLocationField(PointField):
    __doc__ = 'custom form field for picking location for spatial databases'

    def __init__(self, *args, **kwargs):
        map_attrs = kwargs.pop('map_attrs', None)
        self.widget = MapInput(map_attrs=map_attrs)
        (super().__init__)(*args, **kwargs)
        self.error_messages = {'required': "Please pick a location, it's required"}

    def clean(self, value):
        try:
            return super().clean(value)
        except (ValueError, ValidationError):
            return

    def to_python(self, value):
        """Transform the value to a Geometry object."""
        if value in self.empty_values:
            return
        else:
            if isinstance(value, Point):
                return value
            return Point(parse_location(value, first_in_order='lat'), srid=4326)