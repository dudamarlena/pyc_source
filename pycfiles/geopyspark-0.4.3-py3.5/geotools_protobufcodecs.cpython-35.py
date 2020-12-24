# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotools/geotools_protobufcodecs.py
# Compiled at: 2018-12-10 10:02:50
# Size of source mod 2**32: 1066 bytes
from shapely.wkb import loads, dumps
from geopyspark.geopyspark_utils import ensure_pyspark
ensure_pyspark()
from geopyspark.geotools.protobuf.simpleFeatureMessages_pb2 import ProtoSimpleFeature
from geopyspark.vector_pipe import Feature

def from_pb_feature(pb_feature):
    """Creates a ``Feature`` with ``properties`` of ``Properties``
    from ``ProtoSimpleFeature``.

    Args:
        pb_feature (ProtoSimpleFeature): The ``ProtoSimpleFeature`` instance to be converted.

    Returns:
        :class:`~geopyspark.vector_pipe.Feature`
    """
    metadata = dict(pb_feature.metadata)
    geometry = loads(pb_feature.geom)
    return Feature(geometry=geometry, properties=metadata)


def feature_decoder(proto_bytes):
    """Deserializes the ``ProtoSimpleFeature`` bytes into Python.

    Args:
        proto_bytes (bytes): The ProtoBuf encoded bytes of the ProtoBuf class.

    Returns:
        :class:`~geopyspark.vector_pipe.Feature`
    """
    pb_feature = ProtoSimpleFeature.FromString(proto_bytes)
    return from_pb_feature(pb_feature)