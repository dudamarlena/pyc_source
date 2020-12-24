# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nweir/code/cosmiq_repos/solaris/solaris/data/__init__.py
# Compiled at: 2019-12-17 17:07:38
# Size of source mod 2**32: 924 bytes
import os, pandas as pd, geopandas as gpd, gdal, rasterio
from . import coco
data_dir = os.path.abspath(os.path.dirname(__file__))

def load_geojson(gj_fname):
    """Load a geojson into a gdf using GeoPandas."""
    return gpd.read_file(os.path.join(data_dir, gj_fname))


def gt_gdf():
    """Load in a ground truth GDF example."""
    return load_geojson('gt.geojson')


def pred_gdf():
    """Load in an example prediction GDF."""
    return load_geojson('pred.geojson')


def sample_load_rasterio():
    return rasterio.open(os.path.join(data_dir, 'sample_geotiff.tif'))


def sample_load_gdal():
    return gdal.Open(os.path.join(data_dir, 'sample_geotiff.tif'))


def sample_load_geojson():
    return gpd.read_file(os.path.join(data_dir, 'sample.geojson'))


def sample_load_csv():
    return pd.read_file(os.path.join(data_dir, 'sample.csv'))