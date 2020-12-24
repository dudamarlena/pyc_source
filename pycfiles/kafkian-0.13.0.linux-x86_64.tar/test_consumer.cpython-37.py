# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/test_consumer.py
# Compiled at: 2019-09-19 15:18:10
# Size of source mod 2**32: 1398 bytes
import uuid
from unittest.mock import patch, Mock
import pytest
from kafkian import Consumer
KAFKA_BOOTSTRAP_SERVERS = 'localhost:29092'
TEST_TOPIC = 'test.test.' + str(uuid.uuid4())
CONSUMER_CONFIG = {'bootstrap.servers':KAFKA_BOOTSTRAP_SERVERS, 
 'auto.offset.reset':'earliest', 
 'group.id':str(uuid.uuid4())}

@pytest.fixture
def consumer():
    return Consumer(CONSUMER_CONFIG, [TEST_TOPIC])


class MockMessage(Mock):

    def key(self):
        return self._key

    def value(self):
        return self._value

    def set_key(self, new_key):
        self._key = new_key

    def set_value(self, new_value):
        self._value = new_value

    def error(self):
        pass


def test_consume_one_b(consumer):
    key = bytes((str(uuid.uuid4())), encoding='utf8')
    value = bytes((str(uuid.uuid4())), encoding='utf8')
    m = MockMessage()
    m.set_key(key)
    m.set_value(value)
    with patch('kafkian.consumer.Consumer._poll', Mock(return_value=m)):
        m = next(consumer)
    assert m.key == key
    assert m.value == value


def test_consume_one_tombstone(consumer):
    key = bytes((str(uuid.uuid4())), encoding='utf8')
    value = None
    m = MockMessage()
    m.set_key(key)
    m.set_value(value)
    with patch('kafkian.consumer.Consumer._poll', Mock(return_value=m)):
        m = next(consumer)
    assert m.key == key
    assert m.value == value