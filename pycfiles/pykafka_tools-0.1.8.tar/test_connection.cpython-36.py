# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pykafka/test_connection.py
# Compiled at: 2018-05-29 17:13:25
# Size of source mod 2**32: 2402 bytes
import unittest, threading, time, pytest
from uuid import uuid4
from testinstances.managed_instance import ManagedInstance
from pykafka import KafkaClient, Broker
from pykafka.connection import BrokerConnection
from pykafka.exceptions import SocketDisconnectedError
from pykafka.handlers import ThreadingHandler
from pykafka.utils.compat import itervalues
from pykafka.test.utils import get_cluster, stop_cluster

class TestBrokerConnection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kafka = get_cluster()
        if not isinstance(cls.kafka, ManagedInstance):
            pytest.skip('Only test on ManagedInstance (run locally)')
        cls.client = KafkaClient(cls.kafka.brokers)
        ports = cls.kafka._port_generator(9092)
        cls.dest_port = next(ports)
        cls.src_port = next(ports)
        cls.conn = BrokerConnection('localhost', (cls.dest_port),
          (cls.client._handler),
          buffer_size=1048576,
          source_host='localhost',
          source_port=(cls.src_port),
          ssl_config=None)

    @classmethod
    def tearDownClass(cls):
        stop_cluster(cls.kafka)

    def test_connection_fails_no_broker(self):
        """Fail connection when no broker proc exists"""
        assert self.conn is not None
        with self.assertRaises(SocketDisconnectedError):
            self.conn.connect(3000)

    def test_retry_connect(self):
        """Should retry until the connection succeeds."""

        def delayed_make_broker():
            time.sleep(2)
            self.kafka._start_broker_proc(self.dest_port)

        def retry_connect_broker():
            self.conn.connect(3000, attempts=20)

        delay_make_broker_thread = threading.Thread(target=delayed_make_broker)
        delay_make_broker_thread.start()
        connect_broker_thread = threading.Thread(target=retry_connect_broker)
        connect_broker_thread.start()
        delay_make_broker_thread.join(5)
        connect_broker_thread.join(6)
        assert self.conn.connected is True