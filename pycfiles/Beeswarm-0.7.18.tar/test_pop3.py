# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_pop3.py
# Compiled at: 2016-11-12 07:38:04
import unittest, shutil, tempfile, os
from gevent.server import StreamServer
import gevent
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities.pop3 import Pop3

class Pop3Tests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_initial_session(self):
        """Tests if the basic parts of the session is filled correctly"""
        options = {'port': 110, 'protocol_specific_data': {'max_attempts': 3}, 'users': {'test': 'test'}}
        sut = Pop3(options, self.work_dir)
        try:
            sut.handle_session(None, ['192.168.1.200', 12000])
        except AttributeError:
            pass

        return

    def test_login(self):
        """Testing different login combinations"""
        login_sequences = [
         (
          ('USER james', '+OK User accepted'), ('PASS bond', '+OK Pass accepted')),
         (
          ('USER james', '+OK User accepted'), ('PASS wakkawakka', '-ERR Authentication failed.'),
          ('RETR', '-ERR Unknown command')),
         (
          ('USER wakkwakk', '+OK User accepted'), ('PASS wakkwakk', '-ERR Authentication failed.')),
         (('PASS bond', '-ERR No username given.'), ),
         (('RETR', '-ERR Unknown command'), )]
        options = {'port': 110, 'protocol_specific_data': {'max_attempts': 3}, 'users': {'james': 'bond'}}
        sut = Pop3(options, self.work_dir)
        server = StreamServer(('127.0.0.1', 0), sut.handle_session)
        server.start()
        for sequence in login_sequences:
            client = gevent.socket.create_connection(('127.0.0.1', server.server_port))
            fileobj = client.makefile()
            fileobj.readline()
            for pair in sequence:
                client.sendall(pair[0] + '\r\n')
                response = fileobj.readline().rstrip()
                self.assertEqual(response, pair[1])

        server.stop()