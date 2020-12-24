# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/test_producer_avro.py
# Compiled at: 2018-12-06 15:32:52
# Size of source mod 2**32: 2722 bytes
import uuid
from unittest.mock import MagicMock, patch
import pytest
from confluent_kafka import avro
from kafkian import producer
from kafkian.serde.avroserdebase import AvroRecord
from kafkian.serde.serialization import AvroSerializer, Serializer
from tests.unit.conftest import producer_produce_mock
KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
SCHEMA_REGISTRY_URL = 'https://localhost:28081'
TEST_TOPIC = 'test.test.' + str(uuid.uuid4())
PRODUCER_CONFIG = {'bootstrap.servers':KAFKA_BOOTSTRAP_SERVERS, 
 'schema.registry.url':SCHEMA_REGISTRY_URL}
value_schema_str = '\n{\n   "namespace": "my.test",\n   "name": "value",\n   "type": "record",\n   "fields" : [\n     {\n       "name" : "name",\n       "type" : "string"\n     }\n   ]\n}\n'

class Message(AvroRecord):
    _schema = avro.loads(value_schema_str)


message = Message({'name': 'some name'})

def teardown_function(function):
    producer_produce_mock.reset_mock()


@pytest.fixture(scope='module')
def avro_producer():
    return producer.Producer(PRODUCER_CONFIG,
      value_serializer=AvroSerializer(schema_registry_url=SCHEMA_REGISTRY_URL))


def test_producer_init(avro_producer):
    assert isinstance(avro_producer.key_serializer, Serializer)
    assert isinstance(avro_producer.value_serializer, AvroSerializer)


@patch('confluent_kafka.avro.CachedSchemaRegistryClient.register', MagicMock(return_value=1))
@patch('confluent_kafka.avro.CachedSchemaRegistryClient.get_latest_schema', MagicMock(return_value=(1, message._schema, 1)))
@patch('confluent_kafka.avro.CachedSchemaRegistryClient.get_by_id', MagicMock(return_value=(message._schema)))
def test_avro_producer_produce(avro_producer):
    key = 'a'
    value = message
    topic = 'z'
    avro_producer.produce(key=key, value=value, topic=topic)
    producer_produce_mock.assert_called_once_with(topic, key, avro_producer.value_serializer.serialize(value, topic))