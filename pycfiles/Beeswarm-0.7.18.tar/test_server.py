# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/server/tests/test_server.py
# Compiled at: 2016-11-12 07:38:04
import unittest, tempfile, shutil, os, gevent
from gevent import Greenlet
from beeswarm.server.server import Server

class ServerTests(unittest.TestCase):

    def setUp(self):
        self.greenlet_exception = None
        self.greenlet_name = None
        self.tmpdir = tempfile.mkdtemp()
        return

    def tearDown(self):
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def test_server_startup(self):
        server = Server(self.tmpdir, None, clear_db=True, server_hostname='127.0.0.1', customize=False, reset_password=False, max_sessions=999, start_webui=True)
        server_greenlet = Greenlet.spawn(server.start)
        gevent.sleep(2)
        server.stop()
        gevent.sleep(2)
        server_greenlet.kill()
        return