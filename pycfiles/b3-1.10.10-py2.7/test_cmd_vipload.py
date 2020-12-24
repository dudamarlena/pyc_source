# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_vipload.py
# Compiled at: 2016-03-08 18:42:10
from mockito import when
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase, logging_disabled

class Test_cmd_vipload(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nvipload: 20\n        ')
        with logging_disabled():
            self.p = Poweradminbf3Plugin(self.console, self.conf)
            self.p.onLoadConfig()
            self.p.onStartup()
            self.moderator.connects('moderator')

    def test_nominal(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn([])
        when(self.console).write(('reservedSlotsList.load', )).thenReturn([])
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vipload')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (0 name loaded)', self.moderator.message_history[0])

    def test_nominal_2(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['foo', 'bar'])
        when(self.console).write(('reservedSlotsList.list', 2)).thenReturn([])
        when(self.console).write(('reservedSlotsList.load', )).thenReturn([])
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vipload')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (2 names loaded)', self.moderator.message_history[0])

    def test_frostbite_error(self):
        when(self.console).write(('reservedSlotsList.load', )).thenRaise(CommandFailedError(['f00']))
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vipload')
        self.assertEqual(['Error: f00'], self.moderator.message_history)