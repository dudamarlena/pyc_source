# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/test_producer_consume_b.py
# Compiled at: 2019-09-19 15:18:10
# Size of source mod 2**32: 1664 bytes
import uuid, pytest
from kafkian import Producer, Consumer
from tests.unit.conftest import producer_produce_mock, producer_flush_mock
KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
SCHEMA_REGISTRY_URL = 'https://localhost:28081'
TEST_TOPIC = 'test.test.' + str(uuid.uuid4())
CONSUMER_CONFIG = {'bootstrap.servers':KAFKA_BOOTSTRAP_SERVERS, 
 'auto.offset.reset':'earliest', 
 'group.id':str(uuid.uuid4())}
PRODUCER_CONFIG = {'bootstrap.servers':KAFKA_BOOTSTRAP_SERVERS, 
 'schema.registry.url':SCHEMA_REGISTRY_URL}

@pytest.fixture
def producer():
    return Producer(PRODUCER_CONFIG)


@pytest.fixture
def consumer():
    return Consumer(CONSUMER_CONFIG, [TEST_TOPIC])


def test_produce_consume_one(producer, consumer):
    producer_produce_mock.reset_mock()
    producer_flush_mock.reset_mock()
    key = bytes((str(uuid.uuid4())), encoding='utf8')
    value = bytes((str(uuid.uuid4())), encoding='utf8')
    producer.produce(TEST_TOPIC, key, value, sync=True)
    producer_produce_mock.assert_called_once_with(TEST_TOPIC, key, value)
    producer_flush_mock.assert_called_once_with()


def test_produce_consume_one_tombstone(producer, consumer):
    producer_produce_mock.reset_mock()
    producer_flush_mock.reset_mock()
    key = bytes((str(uuid.uuid4())), encoding='utf8')
    value = None
    producer.produce(TEST_TOPIC, key, value, sync=True)
    producer_produce_mock.assert_called_once_with(TEST_TOPIC, key, value)
    producer_flush_mock.assert_called_once_with()