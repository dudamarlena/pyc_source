# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_endround.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase, logging_disabled

class Test_cmd_endround(Bf3TestCase):

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
        self.conf.loadFromString('[commands]\nendround: 20\n        ')
        with logging_disabled():
            self.p = Poweradminbf3Plugin(self.console, self.conf)
            self.p.onLoadConfig()
            self.p.onStartup()
            self.superadmin.connects('superadmin')

    def test_frostbite_error(self):
        when(self.console).write(('serverInfo', )).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
         '2', '300', '300', '0', '', 'false', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.superadmin.message_history = []
        self.superadmin.says('!endround')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('mapList.endRound', '1'))

    def test_no_argument_team1_winning(self):
        when(self.console).write(('serverInfo', )).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
         '2', '800', '90', '0', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.superadmin.message_history = []
        self.superadmin.says('!endround')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('mapList.endRound', '1'))

    def test_no_argument_team2_winning(self):
        when(self.console).write(('serverInfo', )).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
         '2', '400', '1300', '0', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.superadmin.message_history = []
        self.superadmin.says('!endround')
        verify(self.console).write(('mapList.endRound', '2'))
        self.assertEqual([], self.superadmin.message_history)

    def test_no_argument_team4_winning(self):
        when(self.console).write(('serverInfo', )).thenReturn(['i3D.net - BigBrotherBot #3 (DE)', '0', '16', 'ConquestLarge0', 'MP_007', '0', '2',
         '4', '400', '1300', '45', '16510', '', 'true', 'true', 'false', '105473', '105450', '', '', '', 'EU', 'AMS', 'DE'])
        self.superadmin.message_history = []
        self.superadmin.says('!endround')
        verify(self.console).write(('mapList.endRound', '4'))
        self.assertEqual([], self.superadmin.message_history)

    def test_0(self):
        when(self.console).write().thenReturn()
        self.superadmin.message_history = []
        self.superadmin.says('!endround 0')
        verify(self.console).write(('mapList.endRound', '0'))
        self.assertEqual([], self.superadmin.message_history)

    def test_1(self):
        when(self.console).write().thenReturn()
        self.superadmin.message_history = []
        self.superadmin.says('!endround 1')
        verify(self.console).write(('mapList.endRound', '1'))
        self.assertEqual([], self.superadmin.message_history)