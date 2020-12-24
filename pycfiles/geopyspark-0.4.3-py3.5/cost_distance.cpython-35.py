# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/cost_distance.py
# Compiled at: 2018-11-28 11:44:02
# Size of source mod 2**32: 1056 bytes
import shapely.wkb
from geopyspark.geotrellis.layer import TiledRasterLayer
__all__ = [
 'cost_distance']

def cost_distance(friction_layer, geometries, max_distance):
    """Performs cost distance of a TileLayer.

    Args:
        friction_layer(:class:`~geopyspark.geotrellis.layer.TiledRasterLayer`):
            ``TiledRasterLayer`` of a friction surface to traverse.
        geometries (list):
            A list of shapely geometries to be used as a starting point.

            Note:
                All geometries must be in the same CRS as the TileLayer.

        max_distance (int or float): The maximum cost that a path may reach before the operation.
            stops. This value can be an ``int`` or ``float``.

    Returns:
        :class:`~geopyspark.geotrellis.layer.TiledRasterLayer`
    """
    wkbs = [shapely.wkb.dumps(g) for g in geometries]
    srdd = friction_layer.srdd.costDistance(friction_layer.pysc._jsc.sc(), wkbs, float(max_distance))
    return TiledRasterLayer(friction_layer.layer_type, srdd)