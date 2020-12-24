# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/tests/test_honeypot.py
# Compiled at: 2016-11-12 07:38:04
import tempfile, shutil, json, os, gevent, gevent.monkey
gevent.monkey.patch_all()
import unittest, beeswarm, beeswarm.shared, zmq.green
from beeswarm.drones.honeypot.honeypot import Honeypot
from beeswarm.shared.asciify import asciify
from beeswarm.shared.socket_enum import SocketNames

class HoneypotTests(unittest.TestCase):

    def setUp(self):
        beeswarm.shared.zmq_context = zmq.Context()
        self.work_dir = tempfile.mkdtemp()
        Honeypot.prepare_environment(self.work_dir)
        test_config_file = os.path.join(os.path.dirname(__file__), 'honeypotcfg.json.test')
        with open(test_config_file, 'r') as (config_file):
            self.config_dict = json.load(config_file, object_hook=asciify)
        self.key = os.path.join(os.path.dirname(__file__), 'dummy_key.key')
        self.cert = os.path.join(os.path.dirname(__file__), 'dummy_cert.crt')
        self.inbox = gevent.queue.Queue()
        self.mock_relay = gevent.spawn(self.mock_server_relay)

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)
        self.mock_relay.kill()
        self.inbox = gevent.queue.Queue()

    def mock_server_relay(self):
        context = beeswarm.shared.zmq_context
        internal_server_relay = context.socket(zmq.PULL)
        internal_server_relay.bind(SocketNames.SERVER_RELAY.value)
        while True:
            self.inbox.put(internal_server_relay.recv())

    def test_init(self):
        """Tests if the Honeypot class can be instantiated successfully"""
        sut = Honeypot(self.work_dir, self.config_dict, key=self.key, cert=self.cert)

    def test_start_serving(self):
        sut = Honeypot(self.work_dir, self.config_dict, key=self.key, cert=self.cert)
        gevent.spawn(sut.start)
        gevent.sleep(1)
        self.assertEquals(9, len(sut._servers))