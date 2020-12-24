# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/tests/test_pop3s.py
# Compiled at: 2016-11-12 07:38:04
import gevent.monkey
gevent.monkey.patch_all()
import unittest, os, tempfile, shutil
from gevent.server import StreamServer
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.drones.honeypot.capabilities import pop3s as honeypot_pop3s
from beeswarm.drones.client.baits import pop3s as client_pop3s
from beeswarm.drones.client.models.session import BaitSession

class Pop3sTest(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_login(self):
        """Tests if the POP3s bait can login to the POP3 capability"""
        options = {'enabled': 'True', 'port': 0, 'protocol_specific_data': {'max_attempts': 3}, 'users': {'test': 'test'}}
        cap = honeypot_pop3s.Pop3S(options, self.work_dir)
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
        current_bait = client_pop3s.Pop3s(bee_info)
        current_bait.start()
        srv.stop()


if __name__ == '__main__':
    unittest.main()