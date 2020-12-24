# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/tests/test_https.py
# Compiled at: 2016-11-12 07:38:04
import gevent.monkey
from beeswarm.drones.client.baits import https as bee_https
gevent.monkey.patch_all()
from gevent.server import StreamServer
import unittest, os, shutil, tempfile
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.client.models.session import BaitSession
from beeswarm.drones.honeypot.capabilities import https as honeypot_https

class HttpsTest(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_login(self):
        """ Tests if HTTPs bait can login to the http capability.
        """
        options = {'enabled': 'True', 'port': 0, 'users': {'test': 'test'}}
        cap = honeypot_https.https(options, self.work_dir)
        srv = StreamServer(('0.0.0.0', 0), cap.handle_session)
        srv.start()
        bee_info = {'timing': 'regular', 
           'username': 'test', 
           'password': 'test', 
           'port': srv.server_port, 
           'server': '127.0.0.1', 
           'honeypot_id': '1234'}
        beesessions = {}
        BaitSession.client_id = 'f51171df-c8f6-4af4-86c0-f4e163cf69e8'
        current_bait = bee_https.Https(bee_info)
        current_bait.start()
        srv.stop()


if __name__ == '__main__':
    unittest.main()