# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/system/test_produce_consume_avro.py
# Compiled at: 2019-09-19 15:18:10
# Size of source mod 2**32: 2059 bytes
import uuid, pytest
from confluent_kafka import avro
from kafkian import Producer, Consumer
from kafkian.serde.avroserdebase import AvroRecord
from kafkian.serde.deserialization import AvroDeserializer
from kafkian.serde.serialization import AvroStringKeySerializer, AvroSerializer
KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
SCHEMA_REGISTRY_URL = 'http://localhost:28081'
TEST_TOPIC = 'test.test.' + str(uuid.uuid4())
CONSUMER_CONFIG = {'bootstrap.servers':KAFKA_BOOTSTRAP_SERVERS, 
 'auto.offset.reset':'earliest', 
 'group.id':str(uuid.uuid4())}
PRODUCER_CONFIG = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}
value_schema_str = '\n{\n   "namespace": "my.test",\n   "name": "value",\n   "type": "record",\n   "fields" : [\n     {\n       "name" : "name",\n       "type" : "string"\n     }\n   ]\n}\n'

class Message(AvroRecord):
    _schema = avro.loads(value_schema_str)


@pytest.fixture
def producer():
    return Producer(PRODUCER_CONFIG,
      key_serializer=AvroStringKeySerializer(schema_registry_url=SCHEMA_REGISTRY_URL),
      value_serializer=AvroSerializer(schema_registry_url=SCHEMA_REGISTRY_URL))


@pytest.fixture
def consumer():
    return Consumer(CONSUMER_CONFIG,
      [
     TEST_TOPIC],
      key_deserializer=AvroDeserializer(schema_registry_url=SCHEMA_REGISTRY_URL),
      value_deserializer=AvroDeserializer(schema_registry_url=SCHEMA_REGISTRY_URL))


def test_produce_consume_one(producer, consumer):
    key = str(uuid.uuid4())
    value = Message({'name': 'some name'})
    producer.produce(TEST_TOPIC, key, value, sync=True)
    with consumer:
        m = next(consumer)
        consumer.commit(sync=True)
    assert m.key == key
    assert m.value == value


def test_produce_consume_one_tombstone(producer, consumer):
    key = str(uuid.uuid4())
    value = None
    producer.produce(TEST_TOPIC, key, value, sync=True)
    with consumer:
        m = next(consumer)
        consumer.commit(sync=True)
    assert m.key == key
    assert m.value == value