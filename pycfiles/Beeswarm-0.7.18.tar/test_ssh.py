# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_ssh.py
# Compiled at: 2016-11-12 07:38:04
import gevent, gevent.monkey
gevent.monkey.patch_all()
from gevent.server import StreamServer
import unittest, os, shutil, tempfile
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import ssh
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException

class SshTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        self.key = os.path.join(os.path.dirname(__file__), 'dummy_key.key')
        self.cert = os.path.join(os.path.dirname(__file__), 'dummy_cert.crt')
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_basic_login(self):
        options = {'port': 0, 'users': {'test': 'test'}}
        sut = ssh.SSH(options, self.work_dir, self.key)
        server = StreamServer(('127.0.0.1', 0), sut.handle_session)
        server.start()
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        with self.assertRaises(AuthenticationException):
            client.connect('127.0.0.1', server.server_port, 'someuser', 'somepassword')
        server.stop()