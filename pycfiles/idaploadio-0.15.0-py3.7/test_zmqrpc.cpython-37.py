# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/test/test_zmqrpc.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 1749 bytes
import unittest
from time import sleep
import zmq
from locust.rpc import zmqrpc, Message
from locust.test.testcases import LocustTestCase

class ZMQRPC_tests(LocustTestCase):

    def setUp(self):
        super(ZMQRPC_tests, self).setUp()
        self.server = zmqrpc.Server('127.0.0.1', 0)
        self.client = zmqrpc.Client('localhost', self.server.port, 'identity')

    def tearDown(self):
        self.server.socket.close()
        self.client.socket.close()
        super(ZMQRPC_tests, self).tearDown()

    def test_constructor(self):
        self.assertEqual(self.server.socket.getsockopt(zmq.TCP_KEEPALIVE), 1)
        self.assertEqual(self.server.socket.getsockopt(zmq.TCP_KEEPALIVE_IDLE), 30)
        self.assertEqual(self.client.socket.getsockopt(zmq.TCP_KEEPALIVE), 1)
        self.assertEqual(self.client.socket.getsockopt(zmq.TCP_KEEPALIVE_IDLE), 30)

    def test_client_send(self):
        self.client.send(Message('test', 'message', 'identity'))
        addr, msg = self.server.recv_from_client()
        self.assertEqual(addr, 'identity')
        self.assertEqual(msg.type, 'test')
        self.assertEqual(msg.data, 'message')

    def test_client_recv(self):
        sleep(0.1)
        self.server.send_to_client(Message('test', 'message', 'identity'))
        msg = self.client.recv()
        self.assertEqual(msg.type, 'test')
        self.assertEqual(msg.data, 'message')
        self.assertEqual(msg.node_id, 'identity')

    def test_client_retry(self):
        server = zmqrpc.Server('127.0.0.1', 0)
        server.socket.close()
        with self.assertRaises(zmq.error.ZMQError):
            server.recv_from_client()