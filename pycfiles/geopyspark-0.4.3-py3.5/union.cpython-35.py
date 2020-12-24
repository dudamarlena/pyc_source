# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/union.py
# Compiled at: 2018-11-28 11:44:02
# Size of source mod 2**32: 2566 bytes
from geopyspark import get_spark_context
from geopyspark.geotrellis import LayerType, check_layers
from geopyspark.geotrellis.layer import RasterLayer, TiledRasterLayer
__all__ = [
 'union']

def union(layers):
    r"""Unions togther two or more ``RasterLayer``\s or ``TiledRasterLayer``\s.

    All layers must have the same ``layer_type``. If the layers are ``TiledRasterLayer``\s,
    then all of the layers must also have the same :class:`~geopyspark.geotrellis.TileLayout`
    and ``CRS``.

    Note:
        If the layers to be unioned share one or more keys, then the resulting layer will contain
        duplicates of that key. One copy for each instance of the key.

    Args:
        layers ([:class:`~geopyspark.RasterLayer`] or [:class:`~geopyspark.TiledRasterLayer`] or (:class:`~geopyspark.RasterLayer`) or (:class:`~geopyspark.TiledRasterLayer`)): A
            colection of two or more ``RasterLayer``\s or ``TiledRasterLayer``\s layers to be unioned together.

    Returns:
        :class:`~geopyspark.RasterLayer` or :class:`~geopyspark.TiledRasterLayer`
    """
    if len(layers) == 1:
        raise ValueError('union can only be performed on 2 or more layers')
    base_layer = layers[0]
    base_layer_type = base_layer.layer_type
    check_layers(base_layer, base_layer_type, layers)
    pysc = get_spark_context()
    if isinstance(base_layer, RasterLayer):
        if base_layer_type == LayerType.SPATIAL:
            result = pysc._gateway.jvm.geopyspark.geotrellis.ProjectedRasterLayer.unionLayers(pysc._jsc.sc(), [x.srdd for x in layers])
        else:
            result = pysc._gateway.jvm.geopyspark.geotrellis.TemporalRasterLayer.unionLayers(pysc._jsc.sc(), [x.srdd for x in layers])
        return RasterLayer(base_layer_type, result)
    else:
        if base_layer_type == LayerType.SPATIAL:
            result = pysc._gateway.jvm.geopyspark.geotrellis.SpatialTiledRasterLayer.unionLayers(pysc._jsc.sc(), [x.srdd for x in layers])
        else:
            result = pysc._gateway.jvm.geopyspark.geotrellis.TemporalTiledRasterLayer.unionLayers(pysc._jsc.sc(), [x.srdd for x in layers])
        return TiledRasterLayer(base_layer_type, result)