# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/client/tests/test_feeder.py
# Compiled at: 2016-11-12 07:38:04
import shutil, time, tempfile, os
from gevent.greenlet import Greenlet
from mock import Mock
import gevent, gevent.monkey
from beeswarm.drones.client.models.dispatcher import BaitDispatcher
gevent.monkey.patch_all()
import unittest

class DispatcherTests(unittest.TestCase):

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        self.test_config_file = os.path.join(os.path.dirname(__file__), 'clientcfg.json.test')

    def tearDown(self):
        if os.path.isdir(self.work_dir):
            shutil.rmtree(self.work_dir)

    def test_dispatcher(self):
        options = {'enabled': True, 
           'server': '127.0.0.1', 
           'active_range': '00:00 - 23:59', 
           'sleep_interval': '1', 
           'activation_probability': '1', 
           'username': 'test', 
           'password': 'test', 
           'port': 8080}
        dispatcher = BaitDispatcher(Mock(), options)
        dispatcher_greenlet = Greenlet(dispatcher.start)
        dispatcher_greenlet.start()
        gevent.sleep(2)
        dispatcher_greenlet.kill()