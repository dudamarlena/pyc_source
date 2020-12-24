# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/validators.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 1475 bytes
"""Functions for validating and sprucing-up inputs."""
import numpy as np

def validate_sidewalks(sidewalks):
    sidewalks_ls = sidewalks[(sidewalks.type == 'LineString')]
    n = sidewalks_ls.shape[0]
    if n:
        if n < sidewalks.shape[0]:
            m = sidewalks.shape[0] - n
            print('Warning: Removed {} non-LineString sidewalks'.format(m))
        return sidewalks_ls
    raise Exception('No LineStrings in sidewalks dataset: are they' + ' MultiLineStrings?')


def validate_streets(streets):
    streets_ls = streets[(streets.type == 'LineString')]
    n = streets_ls.shape[0]
    if n:
        if n < streets.shape[0]:
            m = streets.shape[0] - n
            print('Warning: Removed {} non-LineString streets'.format(m))
        return streets_ls
    raise Exception('No LineStrings in streets dataset: are they' + ' MultiLineStrings?')


def transform_layer(layer):
    if layer is np.nan:
        return 0
        try:
            return int(layer)
        except ValueError:
            return 0
        except TypeError:
            return int(layer[0])


def standardize_layer(gdf):
    if 'layer' in gdf.columns:
        gdf['layer'] = gdf['layer'].apply(transform_layer)
    else:
        gdf['layer'] = 0