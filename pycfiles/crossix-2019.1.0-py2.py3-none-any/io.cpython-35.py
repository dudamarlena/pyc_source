# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/io.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 2653 bytes
import os, shutil
from tempfile import mkdtemp
import geopandas as gpd, osmnx as ox, overpass
from shapely.geometry import shape
from . import validators

def read_sidewalks(path):
    sidewalks = gpd.read_file(path)
    sidewalks = validators.validate_sidewalks(sidewalks)
    sidewalks_wgs84 = sidewalks.to_crs({'init': 'epsg:4326'})
    return sidewalks_wgs84


def fetch_sidewalks(west, south, east, north):
    api = overpass.API()
    footpaths_filter = '[highway=footway][footway=sidewalk]'
    response = api.Get('way{}({},{},{},{})'.format(footpaths_filter, south, west, north, east))
    rows = []
    for feature in response['features']:
        data = feature['properties']
        data['geometry'] = shape(feature['geometry'])
        rows.append(data)

    gdf = gpd.GeoDataFrame(rows)
    gdf.crs = {'init': 'epsg:4326'}
    return gdf


def fetch_street_graph(sidewalks):
    sidewalks = sidewalks.to_crs({'init': 'epsg:4326'})
    west, south, east, north = sidewalks.total_bounds
    G_streets = ox.graph_from_bbox(north, south, east, west, network_type='drive')
    return G_streets


def write_crossings(crossings, path):
    crossings = crossings.to_crs({'init': 'epsg:4326'})
    tempdir = mkdtemp()
    tempfile = os.path.join(tempdir, 'crossings.geojson')
    try:
        crossings.to_file(tempfile, driver='GeoJSON')
    except Exception as e:
        shutil.rmtree(tempdir)
        raise e

    shutil.move(tempfile, path)


def write_sidewalk_links(links, path):
    links = links.to_crs({'init': 'epsg:4326'})
    tempdir = mkdtemp()
    tempfile = os.path.join(tempdir, 'links.geojson')
    try:
        links.to_file(tempfile, driver='GeoJSON')
    except Exception as e:
        shutil.rmtree(tempdir)
        raise e

    shutil.move(tempfile, path)