# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc_tests/test_server_socket.py
# Compiled at: 2018-07-31 10:42:31
import unittest, socket
from summerrpc.helper import ServerSocketBuilder

class TestServerSocket(unittest.TestCase):

    def setUp(self):
        self._server_socket = ServerSocketBuilder().with_host('127.0.0.1').with_port(0).with_timeout(1).with_blocking().build()

    def tearDown(self):
        self._server_socket.close()

    def testAccept(self):
        host, port = self._server_socket.getsockname()
        print ("host='{0}', port='{1}'").format(host, port)
        try:
            conn, addr = self._server_socket.accept()
        except socket.timeout:
            pass