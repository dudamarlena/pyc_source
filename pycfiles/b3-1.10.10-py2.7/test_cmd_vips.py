# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_vips.py
# Compiled at: 2016-03-08 18:42:10
from mock import call, Mock
from mockito import when
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_vips(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\nvips: mod\n')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.saybig = Mock()
        self.moderator.connects('moderator')
        self.joe.connects('joe')
        self.joe.teamId = 2

    def test_empty_vip_list(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn([])
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vips')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])

    def test_4_vips(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'name2'])
        when(self.console).write(('reservedSlotsList.list', 4)).thenReturn(['name4'])
        when(self.console).write(('reservedSlotsList.list', 5)).thenReturn([])
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vips')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])

    def test_4_vips_one_is_connected(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'Joe'])
        when(self.console).write(('reservedSlotsList.list', 4)).thenReturn([])
        self.joe.connects('Joe')
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vips')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Connected VIPs: Joe', self.moderator.message_history[0])