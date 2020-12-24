# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_vnc.py
# Compiled at: 2016-11-12 07:38:04
import socket, unittest, os, tempfile, shutil, gevent.monkey
gevent.monkey.patch_all()
from gevent.server import StreamServer
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import vnc
from beeswarm.shared.vnc_constants import *

class VncTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_connection(self):
        """ Tests if the VNC capability is up, and tries login.
        """
        options = {'enabled': 'True', 'port': 0, 'users': {'test': 'test'}}
        cap = vnc.Vnc(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', srv.server_port))
        protocol_version = client_socket.recv(1024)
        self.assertEquals(protocol_version, 'RFB 003.007\n')
        client_socket.send(RFB_VERSION)
        supported_auth_methods = client_socket.recv(1024)
        self.assertEquals(supported_auth_methods, SUPPORTED_AUTH_METHODS)
        client_socket.send(VNC_AUTH)
        challenge = client_socket.recv(1024)
        client_socket.send('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        auth_status = client_socket.recv(1024)
        self.assertEquals(auth_status, AUTH_FAILED)