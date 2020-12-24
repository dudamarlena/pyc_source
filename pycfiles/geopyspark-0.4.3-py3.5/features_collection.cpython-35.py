# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/vector_pipe/features_collection.py
# Compiled at: 2018-12-10 10:02:50
# Size of source mod 2**32: 3731 bytes
from json import loads
from geopyspark import create_python_rdd
from geopyspark.geotrellis.protobufserializer import ProtoBufSerializer
from geopyspark.vector_pipe.vector_pipe_protobufcodecs import feature_decoder, feature_encoder

class FeaturesCollection(object):
    __doc__ = "Represents a collection of features from OSM data. A ``feature`` is\n    a geometry that is derived from an OSM Element with that Element's associated metadata.\n    These ``feature``\\s are grouped together by their geometry type.\n\n    There are 4 different types of geometries that a ``feature`` can contain:\n        - ``Point``\\s\n        - ``Line``\\s\n        - ``Polygon``\\s\n        - ``MultiPolygon``\\s\n\n    Args:\n        scala_features (py4j.JavaObject): The Scala representation of ``FeaturesCollection``.\n\n    Attributes:\n        scala_features (py4j.JavaObject): The Scala representation of ``FeaturesCollection``.\n    "

    def __init__(self, scala_features):
        self.scala_features = scala_features

    def get_point_features_rdd(self):
        """Returns each ``Point`` ``feature`` in the ``FeaturesCollection``
        as a :class:`~geopyspark.vector_pipe.Feature` in a Python RDD.

        Returns:
            ``RDD[Feature]``
        """
        return self._get_rdd(self.scala_features.toProtoPoints())

    def get_line_features_rdd(self):
        """Returns each ``Line`` ``feature`` in the ``FeaturesCollection``
        as a :class:`~geopyspark.vector_pipe.Feature` in a Python RDD.

        Returns:
            ``RDD[Feature]``
        """
        return self._get_rdd(self.scala_features.toProtoLines())

    def get_polygon_features_rdd(self):
        """Returns each ``Polygon`` ``feature`` in the ``FeaturesCollection``
        as a :class:`~geopyspark.vector_pipe.Feature` in a Python RDD.

        Returns:
            ``RDD[Feature]``
        """
        return self._get_rdd(self.scala_features.toProtoPolygons())

    def get_multipolygon_features_rdd(self):
        """Returns each ``MultiPolygon`` ``feature`` in the ``FeaturesCollection``
        as a :class:`~geopyspark.vector_pipe.Feature` in a Python RDD.

        Returns:
            ``RDD[Feature]``
        """
        return self._get_rdd(self.scala_features.toProtoMultiPolygons())

    def _get_rdd(self, jrdd):
        ser = ProtoBufSerializer(feature_decoder, feature_encoder)
        return create_python_rdd(jrdd, ser)

    def get_point_tags(self):
        r"""Returns all of the unique tags for all of the ``Point``\s in the
        ``FeaturesCollection`` as a ``dict``. Both the keys and values of the
        ``dict`` will be ``str``\s.

        Returns:
            dict
        """
        return loads(self.scala_features.getPointTags())

    def get_line_tags(self):
        r"""Returns all of the unique tags for all of the ``Line``\s in the
        ``FeaturesCollection`` as a ``dict``. Both the keys and values of the
        ``dict`` will be ``str``\s.

        Returns:
            dict
        """
        return loads(self.scala_features.getLineTags())

    def get_polygon_tags(self):
        r"""Returns all of the unique tags for all of the ``Polygon``\s in the
        ``FeaturesCollection`` as a ``dict``. Both the keys and values of the
        ``dict`` will be ``str``\s.

        Returns:
            dict
        """
        return loads(self.scala_features.getPolygonTags())

    def get_multipolygon_tags(self):
        r"""Returns all of the unique tags for all of the ``MultiPolygon``\s in the
        ``FeaturesCollection`` as a ``dict``. Both the keys and values of the
        ``dict`` will be ``str``\s.

        Returns:
            dict
        """
        return loads(self.scala_features.getMultiPolygonTags())