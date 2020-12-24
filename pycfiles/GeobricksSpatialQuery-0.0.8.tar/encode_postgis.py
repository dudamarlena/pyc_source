# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_spatial_query/geobricks_spatial_query/utils/encode_postgis.py
# Compiled at: 2014-12-25 17:43:18
import os, sys, json, argparse
from pyproj import Proj, transform

def _encode_coords(coords):
    """Encodes a polyline using Google's polyline algorithm

    See http://code.google.com/apis/maps/documentation/polylinealgorithm.html
    for more information.

    :param coords: Coordinates to transform (list of tuples in order: latitude,
    longitude).
    :type coords: list
    :returns: Google-encoded polyline string.
    :rtype: string
    """
    result = []
    prev_lat = 0
    prev_lng = 0
    for coord in coords:
        lat, lng = int(coord[1] * 100000.0), int(coord[0] * 100000.0)
        d_lat = _encode_value(lat - prev_lat)
        d_lng = _encode_value(lng - prev_lng)
        prev_lat, prev_lng = lat, lng
        result.append(d_lat)
        result.append(d_lng)

    return ('').join(c for r in result for c in r)


def _split_into_chunks(value):
    while value >= 32:
        yield value & 31 | 32
        value >>= 5

    yield value


def _encode_value(value):
    value = ~(value << 1) if value < 0 else value << 1
    chunks = _split_into_chunks(value)
    return (chr(chunk + 63) for chunk in chunks)


def _encode_geometry(geom):
    geom_type = geom['type']
    encoded_geom = None
    if geom_type == 'Point':
        return geom['coordinates']
    else:
        if geom_type == 'LineString':
            return _encode_coords(geom['coordinates'])
        if geom_type == 'Polygon':
            return [ _encode_coords(ring) for ring in geom['coordinates'] ]
        if geom_type == 'MultiLinePoint':
            return _encode_coords(geom['coordinates'])
        if geom_type == 'MultiLineString':
            return [ _encode_coords(ls) for ls in geom['coordinates'] ]
        if geom_type == 'MultiPolygon':
            out = []
            for pg in geom['coordinates']:
                out.append([ _encode_coords(ring) for ring in pg ])

            return out
        raise Exception('%s is not a supported geometry type.' % geom_type)
        return


def _shp2json(shp, output, encode=False):
    features = []
    with fiona.collection(shp, 'r') as (source):
        src_srs = Proj(source.crs)
        if src_srs is None:
            print 'Not able to determine spatial reference assuming WGS84.'
        records = []
        for rec in source:
            if rec['geometry'] is None:
                print 'Skipping feature with empty geometry.'
                continue
            geom_type = rec['geometry']['type']
            if src_srs:
                geom = to_wgs84(rec['geometry'], src_srs)
            else:
                geom = rec['geometry']
            if encode:
                rec['geometry']['coordinates'] = _encode_geometry(geom)
            else:
                rec['geometry'] = geom
            records.append(rec)

        layer = {'type': 'FeatureCollection', 
           'features': records}
        geojson = json.dumps(layer)
        output.write(geojson)
        output.close()
    return


def to_wgs84(geom, src_srs):
    """

    Function: to_wgs84

    Transform Fiona geometry to WGS84

    Parameters:

      geom    - (dict) Geometry to be transformed.
      src_srs - (pyproj.Proj) Source spatial reference.

    Returns:

      return Transformed (Fiona) geometry.
    """
    if not src_srs:
        return geom
    out_srs = Proj(init='epsg:4326')
    new_coords = []
    if geom['type'] == 'Point':
        x, y = transform(src_srs, out_srs, *geom['coordinates'])
        new_coords = [x, y]
    elif geom['type'] == 'LineString':
        x, y = transform(src_srs, out_srs, *zip(*geom['coordinates']))
        new_coords = zip(x, y)
    elif geom['type'] in ('MultiLineString', 'Polygon'):
        for ring in geom['coordinates']:
            x, y = transform(src_srs, out_srs, *zip(*ring))
            new_coords.append(zip(x, y))

    elif geom['type'] == 'MultiPolygon':
        for polygon in geom['coordinates']:
            new_polygons = []
            for ring in polygon:
                x, y = transform(src_srs, out_srs, *zip(*ring))
                new_polygons.append(zip(x, y))

            new_coords.append(new_polygons)

    geom['coordinates'] = new_coords
    return geom