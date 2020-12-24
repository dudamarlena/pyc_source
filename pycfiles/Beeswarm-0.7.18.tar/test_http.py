# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_http.py
# Compiled at: 2016-11-12 07:38:04
import gevent.monkey
gevent.monkey.patch_all()
from gevent.server import StreamServer
from beeswarm.drones.honeypot.capabilities import http
import unittest, httplib, base64, tempfile, shutil, os
from beeswarm.drones.honeypot.honeypot import Honeypot

class HttpTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_connection(self):
        """ Tests if the capability is up, and sending
            HTTP 401 (Unauthorized) headers.
        """
        options = {'enabled': 'True', 'port': 0, 'users': {'test': 'test'}}
        cap = http.Http(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        client = httplib.HTTPConnection('127.0.0.1', srv.server_port)
        client.request('GET', '/')
        response = client.getresponse()
        self.assertEqual(response.status, 401)
        srv.stop()

    def test_login(self):
        """ Tries to login using the username/password as test/test.
        """
        options = {'enabled': 'True', 'port': 0, 'users': {'test': 'test'}}
        cap = http.Http(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        client = httplib.HTTPConnection('127.0.0.1', srv.server_port)
        client.putrequest('GET', '/')
        client.putheader('Authorization', 'Basic ' + base64.b64encode('test:test'))
        client.endheaders()
        response = client.getresponse()
        self.assertEqual(response.status, 200)
        srv.stop()