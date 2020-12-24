# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/geo.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 7097 bytes
"""GeoJSON support for Marrow Mongo."""
from __future__ import unicode_literals
from collections import MutableSequence
from numbers import Number as NumberABC
from . import Document, Field
from .field import Alias, Array, Number, String

class GeoJSON(Document):
    __type_store__ = 'type'
    kind = String('type', required=True)


class GeoJSONCoord(GeoJSON):
    coordinates = Array((Field()), default=(lambda : []), assign=True)

    def __init__(self, *coords, **kw):
        kw['coordinates'] = list(self.to_foreign(i) for i in (coords if coords else kw.get('coordinates', [])))
        (super(GeoJSONCoord, self).__init__)(**kw)

    def to_native(self, value):
        return value

    def to_foreign(self, value):
        return list(getattr(value, 'coordinates', value))

    def insert(self, index, item):
        self.coordinates.insert(index, self.to_foreign(item))

    def append(self, item):
        self.coordinates.append(self.to_foreign(item))

    def extend(self, other):
        if isinstance(other, self.__class__):
            self.coordinates.extend(other.coordinates)
        else:
            self.coordinates.extend(self.to_foreign(i) for i in other)

    def __getitem__(self, item):
        if isinstance(item, NumberABC) or item.lstrip('-').isnumeric():
            return self.to_native(self.coordinates[int(item)])
        else:
            return super(GeoJSONCoord, self).__getitem__(item)

    def __setitem__(self, item, value):
        if isinstance(item, NumberABC) or item.lstrip('-').isnumeric():
            self.coordinates[int(item)] = self.to_foreign(value)
            return
        super(GeoJSONCoord, self).__setitem__(item, value)

    def __delitem__(self, item):
        if isinstance(item, NumberABC) or item.lstrip('-').isnumeric():
            del self.coordinates[int(item)]
            return
        super(GeoJSONCoord, self).__delitem__(item)

    def __len__(self):
        try:
            return len(self.coordinates)
        except:
            return 0


MutableSequence.register(GeoJSONCoord)

class Point(GeoJSONCoord):
    __doc__ = 'A GeoJSON Point.\n\t\n\tExample:\n\t\n\t\tPoint(40, 5)\n\t\t\n\t\t{ type: "Point", coordinates: [ 40, 5 ] }\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#point\n\t\thttp://geojson.org/geojson-spec.html#point\n\t'
    kind = String('type', default='Point', assign=True)
    coordinates = Array(Number())
    lat = latitude = Alias('coordinates.1')
    long = longitude = Alias('coordinates.0')

    def __init__(self, longitude=0, latitude=0, **kw):
        (super(Point, self).__init__)(coordinates=kw.pop('coordinates', [longitude, latitude]), **kw)

    def to_foreign(self, value):
        return float(value)


class LineString(GeoJSONCoord):
    __doc__ = 'A GeoJSON LineString.\n\t\n\tExample:\n\t\n\t\tLineString((40, 5), (41, 6))\n\t\t\n\t\t{ type: "LineString", coordinates: [ [ 40, 5 ], [ 41, 6 ] ] }\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#linestring\n\t\thttp://geojson.org/geojson-spec.html#linestring\n\t'
    kind = String('type', default='LineString', assign=True)
    coordinates = Array(Array(Number()))

    def to_native(self, value):
        return Point(*getattr(value, 'coordinates', value))


class Polygon(GeoJSONCoord):
    __doc__ = 'A GeoJSON Polygon.\n\t\n\tExample:\n\t\n\t\tPolygon([(0, 0), (3, 6), (6, 1), (0, 0)])\n\t\t\n\t\t{\n\t\t\ttype: "Polygon",\n\t\t\tcoordinates: [ [ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0  ] ] ]\n\t\t}\n\t\n\t\t{\n\t\t\ttype : "Polygon",\n\t\t\tcoordinates : [\n\t\t\t\t[ [ 0 , 0 ] , [ 3 , 6 ] , [ 6 , 1 ] , [ 0 , 0 ] ],\n\t\t\t\t[ [ 2 , 2 ] , [ 3 , 3 ] , [ 4 , 2 ] , [ 2 , 2 ] ]\n\t\t\t]\n\t\t}\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#polygon\n\t\thttp://geojson.org/geojson-spec.html#polygon\n\t'
    kind = String('type', default='Polygon', assign=True)
    coordinates = Array(Array(Array(Number())))
    exterior = Alias('coordinates.0')

    def to_native(self, value):
        return LineString(*getattr(value, 'coordinates', value))


class MultiPoint(GeoJSONCoord):
    __doc__ = 'A GeoJSON MultiPoint.\n\t\n\tExample:\n\t\n\t\tMultiPoint((-73.9580, 40.8003), (-73.9498, 40.7968), (-73.9737, 40.7648), (-73.9814, 40.7681))\n\t\t\n\t\t{\n\t\t\ttype: "MultiPoint",\n\t\t\tcoordinates: [\n\t\t\t\t[ -73.9580, 40.8003 ],\n\t\t\t\t[ -73.9498, 40.7968 ],\n\t\t\t\t[ -73.9737, 40.7648 ],\n\t\t\t\t[ -73.9814, 40.7681 ]\n\t\t\t]\n\t\t}\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#multipoint\n\t\thttp://geojson.org/geojson-spec.html#multipoint\n\t'
    kind = String('type', default='MultiPoint', assign=True)
    coordinates = Array(Array(Number()))

    def to_native(self, value):
        return Point(*getattr(value, 'coordinates', value))


class MultiLineString(GeoJSONCoord):
    __doc__ = 'A GeoJSON MultiLineString.\n\t\n\tExample:\n\t\n\t\tMultiLineString([(-73.96943, 40.78519), (-73.96082, 40.78095)], [(-73.96415, 40.79229), (-73.95544, 40.78854)],\n\t\t\t\t[(-73.97162, 40.78205), (-73.96374, 40.77715)], [(-73.97880, 40.77247), (-73.97036, 40.76811)])\n\t\t\n\t\t{\n\t\t\ttype: "MultiLineString",\n\t\t\tcoordinates: [\n\t\t\t\t[ [ -73.96943, 40.78519 ], [ -73.96082, 40.78095 ] ],\n\t\t\t\t[ [ -73.96415, 40.79229 ], [ -73.95544, 40.78854 ] ],\n\t\t\t\t[ [ -73.97162, 40.78205 ], [ -73.96374, 40.77715 ] ],\n\t\t\t\t[ [ -73.97880, 40.77247 ], [ -73.97036, 40.76811 ] ]\n\t\t\t]\n\t\t}\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#multilinestring\n\t\thttp://geojson.org/geojson-spec.html#multilinestring\n\t'
    kind = String('type', default='MultiLineString', assign=True)
    coordinates = Array(Array(Array(Number())))

    def to_native(self, value):
        return LineString(*getattr(value, 'coordinates', value))


class MultiPolygon(GeoJSONCoord):
    __doc__ = 'A GeoJSON MultiPolygon.\n\t\n\tExample:\n\t\n\t\t{\n\t\t\ttype: "MultiPolygon",\n\t\t\tcoordinates: [\n\t\t\t\t[ [ [ -73.958, 40.8003 ], [ -73.9498, 40.7968 ], [ -73.9737, 40.7648 ], [ -73.9814, 40.7681 ],\n\t\t\t\t\t\t[ -73.958, 40.8003 ] ] ],\n\t\t\t\t[ [ [ -73.958, 40.8003 ], [ -73.9498, 40.7968 ], [ -73.9737, 40.7648 ], [ -73.958, 40.8003 ] ] ]\n\t\t\t]\n\t\t}\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#multipolygon\n\t\thttp://geojson.org/geojson-spec.html#multipolygon\n\t'
    kind = String('type', default='MultiPolygon', assign=True)
    coordinates = Array(Array(Array(Array(Number()))))

    def to_native(self, value):
        return Polygon(*getattr(value, 'coordinates', value))


class GeometryCollection(GeoJSON):
    __doc__ = 'A GeoJSON GeometryCollection.\n\t\n\tExample:\n\t\n\t\t{\n\t\t\ttype: "GeometryCollection",\n\t\t\tgeometries: [\n\t\t\t\t{\n\t\t\t\t\ttype: "MultiPoint",\n\t\t\t\t\tcoordinates: [\n\t\t\t\t\t\t[ -73.9580, 40.8003 ],\n\t\t\t\t\t\t[ -73.9498, 40.7968 ],\n\t\t\t\t\t\t[ -73.9737, 40.7648 ],\n\t\t\t\t\t\t[ -73.9814, 40.7681 ]\n\t\t\t\t\t]\n\t\t\t\t},\n\t\t\t\t{\n\t\t\t\t\ttype: "MultiLineString",\n\t\t\t\t\tcoordinates: [\n\t\t\t\t\t\t[ [ -73.96943, 40.78519 ], [ -73.96082, 40.78095 ] ],\n\t\t\t\t\t\t[ [ -73.96415, 40.79229 ], [ -73.95544, 40.78854 ] ],\n\t\t\t\t\t\t[ [ -73.97162, 40.78205 ], [ -73.96374, 40.77715 ] ],\n\t\t\t\t\t\t[ [ -73.97880, 40.77247 ], [ -73.97036, 40.76811 ] ]\n\t\t\t\t\t]\n\t\t\t\t}\n\t\t\t]\n\t\t}\n\t\n\tReferences:\n\t\n\t\thttps://docs.mongodb.com/manual/reference/geojson/#geometrycollection\n\t\thttp://geojson.org/geojson-spec.html#geometrycollection\n\t'
    kind = String('type', default='GeometryCollection', assign=True)
    geometries = Array(GeoJSONCoord, default=(lambda : []), assign=True)

    def __init__(self, *geometries, **kw):
        (super(GeometryCollection, self).__init__)(geometries=list(geometries), **kw)