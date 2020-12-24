# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbeilin/.pyenv/versions/3.7.0/lib/python3.7/site-packages/tests/unit/conftest.py
# Compiled at: 2019-01-05 17:14:30
# Size of source mod 2**32: 678 bytes
from unittest.mock import patch, Mock
producer_produce_mock = Mock()
producer_poll_mock = Mock(return_value=1)
producer_flush_mock = Mock()
consumer_close_mock = Mock()
mocks = [
 patch('kafkian.producer.Producer._init_producer_impl', Mock(return_value=(Mock()))),
 patch('kafkian.Producer._produce', producer_produce_mock),
 patch('kafkian.Producer.poll', producer_poll_mock),
 patch('kafkian.Producer.flush', producer_flush_mock),
 patch('kafkian.consumer.Consumer._init_consumer_impl', Mock(return_value=(Mock()))),
 patch('kafkian.consumer.Consumer._close', consumer_close_mock)]
for mock in mocks:
    mock.start()