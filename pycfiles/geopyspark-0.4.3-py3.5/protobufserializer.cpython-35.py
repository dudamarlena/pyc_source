# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/geopyspark/geotrellis/protobufserializer.py
# Compiled at: 2018-11-28 11:44:02
# Size of source mod 2**32: 2889 bytes
"""The class which serializes/deserializes values in a RDD to/from Python."""
from geopyspark.geopyspark_utils import ensure_pyspark
ensure_pyspark()
from geopyspark.geotrellis.protobufcodecs import create_partial_tuple_decoder, create_partial_tuple_encoder, create_partial_image_rdd_decoder, _get_encoder, _get_decoder
from pyspark.serializers import FramedSerializer
from pyspark.serializers import AutoBatchedSerializer

class ProtoBufSerializer(FramedSerializer):
    __doc__ = 'The serializer used by a RDD to encode/decode values to/from Python.\n\n    Args:\n        decoding_method (func): The decocding function for the values within the RDD.\n        encoding_method (func): The encocding function for the values within the RDD.\n\n    Attributes:\n        decoding_method (func): The decocding function for the values within the RDD.\n        encoding_method (func): The encocding function for the values within the RDD.\n    '
    __slots__ = [
     'decoding_method', 'encoding_method']

    def __init__(self, decoding_method, encoding_method):
        FramedSerializer.__init__(self)
        self.decoding_method = decoding_method
        self.encoding_method = encoding_method

    @classmethod
    def create_tuple_serializer(cls, key_type):
        decoder = create_partial_tuple_decoder(key_type=key_type)
        encoder = create_partial_tuple_encoder(key_type=key_type)
        return cls(decoder, encoder)

    @classmethod
    def create_value_serializer(cls, value_type):
        decoder = _get_decoder(value_type)
        encoder = _get_encoder(value_type)
        return cls(decoder, encoder)

    @classmethod
    def create_image_rdd_serializer(cls, key_type):
        decoder = create_partial_image_rdd_decoder(key_type=key_type)
        encoder = None
        return cls(decoder, encoder)

    def _dumps(self, obj):
        return self.encoding_method(obj)

    def dumps(self, obj):
        """Serialize an object into a byte array.

        Note:
            When batching is used, this will be called with a list of objects.

        Args:
            obj: The object to serialized into a byte array.

        Returns:
            The byte array representation of the ``obj``.
        """
        if isinstance(obj, list):
            for x in obj:
                return self._dumps(x)

        else:
            return self._dumps(obj)

    def loads(self, obj):
        """Deserializes a byte array into a collection of Python objects.

        Args:
            obj: The byte array representation of an object to be deserialized into the object.

        Returns:
            A list of deserialized objects.
        """
        return [
         self.decoding_method(obj)]