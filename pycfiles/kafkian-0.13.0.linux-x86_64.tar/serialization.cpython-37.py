# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/kafkian/serde/serialization.py
# Compiled at: 2019-03-06 08:31:32
# Size of source mod 2**32: 2919 bytes
from enum import Enum
from confluent_kafka import avro
from confluent_kafka.avro import CachedSchemaRegistryClient
from .avroserdebase import AvroRecord, AvroSerDeBase

class SubjectNameStrategy(Enum):
    TopicNameStrategy = 0
    RecordNameStrategy = 1
    TopicRecordNameStrategy = 2


class Serializer:
    __doc__ = '\n    Base class for all key and value serializers.\n    This default implementation returns the value intact.\n    '

    def __init__(self, **kwargs):
        pass

    def serialize(self, value, topic, **kwargs):
        return value


class AvroSerializer(Serializer):

    def __init__(self, schema_registry_url, auto_register_schemas=True, subject_name_strategy=SubjectNameStrategy.RecordNameStrategy, **kwargs):
        (super().__init__)(**kwargs)
        schema_registry_url = schema_registry_url
        self.schema_registry = CachedSchemaRegistryClient(schema_registry_url)
        self.auto_register_schemas = auto_register_schemas
        self.subject_name_strategy = subject_name_strategy
        self._serializer_impl = AvroSerDeBase(self.schema_registry)

    def _get_subject(self, topic: str, schema, is_key=False):
        if self.subject_name_strategy == SubjectNameStrategy.TopicNameStrategy:
            subject = topic + ('-key' if is_key else '-value')
        else:
            if self.subject_name_strategy == SubjectNameStrategy.RecordNameStrategy:
                subject = schema.fullname
            else:
                if self.subject_name_strategy == SubjectNameStrategy.TopicRecordNameStrategy:
                    subject = '{}-{}'.format(topic, schema.fullname)
                else:
                    raise ValueError('Unknown SubjectNameStrategy')
        return subject

    def _ensure_schema(self, topic: str, schema, is_key=False):
        subject = self._get_subject(topic, schema, is_key)
        if self.auto_register_schemas:
            schema_id = self.schema_registry.register(subject, schema)
            schema = self.schema_registry.get_by_id(schema_id)
        else:
            schema_id, schema, _ = self.schema_registry.get_latest_schema(subject)
        return (schema_id, schema)

    def serialize(self, value: AvroRecord, topic: str, is_key=False, **kwargs):
        schema_id, _ = self._ensure_schema(topic, value.schema, is_key)
        return self._serializer_impl.encode_record_with_schema_id(schema_id, value, is_key)


class AvroStringKeySerializer(AvroSerializer):
    __doc__ = '\n    A specialized serializer for generic String keys,\n    serialized with a simple value avro schema.\n    '
    KEY_SCHEMA = avro.loads('{"type": "string"}')

    def serialize(self, value: str, topic: str, is_key=False, **kwargs):
        assert is_key
        schema_id, _ = self._ensure_schema(topic, self.KEY_SCHEMA, is_key)
        return self._serializer_impl.encode_record_with_schema_id(schema_id, value, is_key)