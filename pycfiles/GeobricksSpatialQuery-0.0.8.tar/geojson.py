# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vortex/repos/FENIX-MAPS/geobricks/geobricks_spatial_query/geobricks_spatial_query/utils/geojson.py
# Compiled at: 2015-03-05 09:12:05
import simplejson
from geobricks_spatial_query.utils.encode_postgis import _encode_geometry

def encode_geojson(rows, encode_geometry=True):
    output = {}
    output['type'] = 'FeatureCollection'
    output['features'] = []
    for v in rows:
        j = simplejson.loads(v[0])
        f = {}
        f['type'] = 'Feature'
        f['geometry'] = {}
        f['geometry']['type'] = j['type']
        if encode_geometry:
            f['geometry']['coordinates'] = _encode_geometry(j)
        f['properties'] = {}
        for p in range(1, len(v)):
            f['properties']['prop' + str(p - 1)] = v[p]

        output['features'].append(f)

    return output