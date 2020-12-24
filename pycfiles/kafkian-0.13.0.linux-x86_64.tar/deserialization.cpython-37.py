# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/kafkian/serde/deserialization.py
# Compiled at: 2018-11-21 15:57:52
# Size of source mod 2**32: 757 bytes
from confluent_kafka.avro import CachedSchemaRegistryClient
from .avroserdebase import AvroSerDeBase

class Deserializer:
    __doc__ = '\n    Base class for all key and value deserializers.\n    This default implementation returns the value intact.\n    '

    def __init__(self, **kwargs):
        pass

    def deserialize(self, value, **kwargs):
        return value


class AvroDeserializer(Deserializer):

    def __init__(self, schema_registry_url, **kwargs):
        (super().__init__)(**kwargs)
        self.schema_registry = CachedSchemaRegistryClient(schema_registry_url)
        self._serializer_impl = AvroSerDeBase(self.schema_registry)

    def deserialize(self, value, **kwargs):
        return self._serializer_impl.decode_message(value)