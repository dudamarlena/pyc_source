# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_telnet.py
# Compiled at: 2016-11-12 07:38:04
import gevent, gevent.monkey
from beeswarm.drones.honeypot.capabilities import telnet
gevent.monkey.patch_all()
from gevent.server import StreamServer
import unittest, telnetlib, tempfile, sys, os, shutil
from beeswarm.drones.honeypot.honeypot import Honeypot

class TelnetTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_invalid_login(self):
        """Tests if telnet server responds correctly to a invalid login attempt."""
        sys.stdout = tempfile.TemporaryFile()
        options = {'enabled': 'True', 'port': 2503, 'protocol_specific_data': {'max_attempts': 3}, 'users': {'test': 'test'}}
        cap = telnet.Telnet(options, self.work_dir)
        server = StreamServer(('0.0.0.0', 2503), cap.handle_session)
        server.start()
        client = telnetlib.Telnet('localhost', 2503)
        client.set_debuglevel(0)
        client.set_option_negotiation_callback(self.cb)
        reply = client.read_until('Username: ', 1)
        self.assertEquals('Username: ', reply)
        client.write('someuser\r\n')
        reply = client.read_until('Password: ', 5)
        self.assertTrue(reply.endswith('Password: '))
        client.write('somepass\r\n')
        reply = client.read_until('Invalid username/password\r\nUsername: ')
        self.assertTrue(reply.endswith('Invalid username/password\r\nUsername: '))
        server.stop()

    def test_valid_login(self):
        """Tests if telnet server responds correctly to a VALID login attempt."""
        sys.stdout = tempfile.TemporaryFile()
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3}, 'users': {'test': 'test'}}
        cap = telnet.Telnet(options, self.work_dir)
        server = StreamServer(('0.0.0.0', 0), cap.handle_session)
        server.start()
        client = telnetlib.Telnet('localhost', server.server_port)
        client.set_debuglevel(0)
        client.set_option_negotiation_callback(self.cb)
        reply = client.read_until('Username: ', 1)
        self.assertEquals('Username: ', reply)
        client.write('test\r\n')
        reply = client.read_until('Password: ', 5)
        self.assertTrue(reply.endswith('Password: '))
        client.write('test\r\n')
        reply = client.read_until('$ ')
        self.assertTrue(reply.endswith('$ '))
        server.stop()

    def test_commands(self):
        """Tests the telnet commands"""
        sys.stdout = tempfile.TemporaryFile()
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'banner': 'Test', 'max_attempts': 3}, 'users': {'test': 'test'}}
        cap = telnet.Telnet(options, self.work_dir)
        server = StreamServer(('0.0.0.0', 0), cap.handle_session)
        server.start()
        client = telnetlib.Telnet('localhost', server.server_port)
        client.set_debuglevel(0)
        client.set_option_negotiation_callback(self.cb)
        reply = client.read_until('Username: ', 1)
        self.assertEquals('Username: ', reply)
        client.write('test\r\n')
        reply = client.read_until('Password: ', 5)
        self.assertTrue(reply.endswith('Password: '))
        client.write('test\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.endswith('$ '))
        client.write('ls -l\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('ls -l\r\n'))
        self.assertTrue(reply.endswith('$ '))
        client.write('echo this test is so cool' + '\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('echo '))
        self.assertTrue('this test is so cool' in reply)
        self.assertTrue(reply.endswith('$ '))
        client.write('cd var\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('cd '))
        self.assertTrue(reply.endswith('$ '))
        client.write('pwd\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('pwd'))
        self.assertTrue('/var' in reply)
        self.assertTrue(reply.endswith('$ '))
        client.write('uname -a\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('uname '))
        self.assertTrue(reply.endswith('$ '))
        client.write('cat /var/www/index.html' + '\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('cat '))
        self.assertTrue('</html>' in reply)
        self.assertTrue(reply.endswith('$ '))
        client.write('uptime\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('uptime'))
        self.assertTrue(reply.endswith('$ '))
        client.write('sudo service network restart' + '\r\n')
        reply = client.read_until('$ ', 5)
        self.assertTrue(reply.startswith('sudo'))
        self.assertTrue('Sorry' in reply)
        self.assertTrue(reply.endswith('$ '))
        server.stop()

    def cb(self, socket, command, option):
        pass