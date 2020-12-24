# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/validators.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 1475 bytes
__doc__ = 'Functions for validating and sprucing-up inputs.'
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