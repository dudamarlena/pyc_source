# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/gis/serializers/geojson.py
# Compiled at: 2019-02-14 00:35:16
from __future__ import unicode_literals
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.core.serializers.base import SerializerDoesNotExist
from django.core.serializers.json import Serializer as JSONSerializer

class Serializer(JSONSerializer):
    """
    Convert a queryset to GeoJSON, http://geojson.org/
    """

    def _init_options(self):
        super(Serializer, self)._init_options()
        self.geometry_field = self.json_kwargs.pop(b'geometry_field', None)
        self.srid = self.json_kwargs.pop(b'srid', 4326)
        if self.selected_fields is not None and self.geometry_field is not None and self.geometry_field not in self.selected_fields:
            self.selected_fields = list(self.selected_fields) + [self.geometry_field]
        return

    def start_serialization(self):
        self._init_options()
        self._cts = {}
        self.stream.write(b'{"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "EPSG:%d"}}, "features": [' % self.srid)

    def end_serialization(self):
        self.stream.write(b']}')

    def start_object(self, obj):
        super(Serializer, self).start_object(obj)
        self._geometry = None
        if self.geometry_field is None:
            for field in obj._meta.fields:
                if hasattr(field, b'geom_type'):
                    self.geometry_field = field.name
                    break

        return

    def get_dump_object(self, obj):
        data = {b'type': b'Feature', 
           b'properties': self._current}
        if (self.selected_fields is None or b'pk' in self.selected_fields) and b'pk' not in data[b'properties']:
            data[b'properties'][b'pk'] = obj._meta.pk.value_to_string(obj)
        if self._geometry:
            if self._geometry.srid != self.srid:
                if self._geometry.srid not in self._cts:
                    srs = SpatialReference(self.srid)
                    self._cts[self._geometry.srid] = CoordTransform(self._geometry.srs, srs)
                self._geometry.transform(self._cts[self._geometry.srid])
            data[b'geometry'] = eval(self._geometry.geojson)
        else:
            data[b'geometry'] = None
        return data

    def handle_field(self, obj, field):
        if field.name == self.geometry_field:
            self._geometry = field.value_from_object(obj)
        else:
            super(Serializer, self).handle_field(obj, field)


class Deserializer(object):

    def __init__(self, *args, **kwargs):
        raise SerializerDoesNotExist(b'geojson is a serialization-only serializer')