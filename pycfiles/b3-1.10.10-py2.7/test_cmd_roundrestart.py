# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_roundrestart.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, call
from mockito import verify, when
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_roundrestart(Bf3TestCase):

    @classmethod
    def setUpClass(cls):
        Bf3TestCase.setUpClass()
        cls.sleep_patcher = patch.object(time, 'sleep')
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nroundrestart: 20\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')

    def test_nominal(self):
        when(self.console).write()
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!roundrestart')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('mapList.restartRound', ))