# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/commons/clip.py
# Compiled at: 2019-10-18 08:46:26
# Size of source mod 2**32: 2224 bytes
"""Clip array using vector data."""
import numpy as np, numpy.ma as ma
from shapely.ops import unary_union
from rasterio.features import geometry_mask
from mapchete.io.vector import to_shape

def clip_array_with_vector(array, array_affine, geometries, inverted=False, clip_buffer=0):
    """
    Clip input array with a vector list.

    Parameters
    ----------
    array : array
        input raster data
    array_affine : Affine
        Affine object describing the raster's geolocation
    geometries : iterable
        iterable of dictionaries, where every entry has a 'geometry' and
        'properties' key.
    inverted : bool
        invert clip (default: False)
    clip_buffer : integer
        buffer (in pixels) geometries before clipping

    Returns
    -------
    clipped array : array
    """
    buffered_geometries = []
    for feature in geometries:
        feature_geom = to_shape(feature['geometry'])
        if feature_geom.is_empty:
            pass
        else:
            if feature_geom.geom_type == 'GeometryCollection':
                buffered_geom = unary_union([g.buffer(clip_buffer) for g in feature_geom])
            else:
                buffered_geom = feature_geom.buffer(clip_buffer)
            if not buffered_geom.is_empty:
                buffered_geometries.append(buffered_geom)

    if buffered_geometries:
        if array.ndim == 2:
            return ma.masked_array(array, geometry_mask(buffered_geometries, array.shape, array_affine, invert=inverted))
        if array.ndim == 3:
            mask = geometry_mask(buffered_geometries, (
             array.shape[1], array.shape[2]), array_affine, invert=inverted)
            return ma.masked_array(array, mask=np.stack([mask for band in array]))
    else:
        fill = False if inverted else True
        return ma.masked_array(array, mask=np.full(array.shape, fill, dtype=bool))