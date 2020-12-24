# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_spatial_query/geobricks_spatial_query/utils/geojson_encoder.py
# Compiled at: 2015-02-05 08:41:58
from geobricks_dbms.core.dbms_postgresql import DBMSPostgreSQL
from sys import stdin, stdout
from json import loads, dumps, JSONEncoder
from optparse import OptionParser
from re import compile
import encode_postgis, simplejson
float_pat = compile('^-?\\d+\\.\\d+(e-?\\d+)?$')
charfloat_pat = compile('^[\\[,\\,]-?\\d+\\.\\d+(e-?\\d+)?$')
input = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [102.0, 0.5]}, 'properties': {'prop0': 'value0'}}, {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]]}, 'properties': {'prop0': 'value0', 'prop1': 0.0}}, {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]}, 'properties': {'prop0': 'value0', 'prop1': {'this': 'that'}}}]}
data = dumps(input)
encoder = JSONEncoder(separators=(',', ':'))
encoded = encoder.iterencode(input)
prev_lat = 0
prev_lng = 0
out = ''
char_lat = True

def encode_geojson(r):
    output = {}
    output['type'] = 'FeatureCollection'
    output['features'] = []
    for v in r:
        j = loads(v[0])
        f = {}
        f['type'] = 'Feature'
        f['geometry'] = {}
        f['geometry']['type'] = j['type']
        f['geometry']['coordinates'] = encode_postgis._encode_geometry(j)
        f['properties'] = {}
        for p in range(1, len(v)):
            f['properties']['prop' + str(p)] = v[p]

        output['features'].append(f)

    print output
    return output


def encode_geojson_to_file(r):
    out_file = open('/home/vortex/Desktop/encode_geojson.geojson', 'wb')
    out_file.write('{"type":"FeatureCollection","features":[')
    index = 0
    for v in r:
        j = loads(v[0])
        f = {}
        f['type'] = 'Feature'
        f['geometry'] = {}
        f['geometry']['type'] = j['type']
        f['geometry']['coordinates'] = encode_postgis._encode_geometry(j)
        f['properties'] = {'gaul0': v[1], 'name': v[2]}
        out_file.write(dumps(f))
        if index < len(r) - 1:
            out_file.write(',')
        index += 1

    out_file.write(']}')
    out_file.close()


def query_geojson():
    db_settings = {}
    db_settings['dbname'] = 'fenix'
    db_settings['password'] = 'Qwaszx'
    db_settings['username'] = 'fenix'
    db = DBMSPostgreSQL(db_settings)
    r = db.query("select ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.04)), adm0_code, adm0_name from spatial.gaul0_2015_4326 where adm0_name IN ('Italy')")
    print 'doing geojson'
    out_file = open('html/data/Italy.geojson', 'wb')
    out_file.write('{"type":"FeatureCollection","features":[')
    index = 0
    for v in r:
        j = loads(v[0])
        f = {}
        f['type'] = 'Feature'
        f['geometry'] = {}
        f['geometry']['type'] = j['type']
        f['geometry']['coordinates'] = encode_postgis._encode_geometry(j)
        f['properties'] = {'gaul0': v[1], 'name': v[2]}
        out_file.write(dumps(f))
        if index < len(r) - 1:
            out_file.write(',')
        index += 1

    out_file.write(']}')
    out_file.close()


print out