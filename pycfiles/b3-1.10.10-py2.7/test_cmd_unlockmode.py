# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_unlockmode.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from mockito import when, verify
import b3
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_unlockmode(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_unlockmode, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nunlockmode: 40\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        when(self.console).write()

    def test_get_current_unlockmode(self):
        self.superadmin.connects('superadmin')
        when(self.console).write(('vars.unlockMode', )).thenReturn(['f00'])
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode')
        self.assertEqual(['Current unlock mode is [f00]'], self.superadmin.message_history)

    def test_bad_argument(self):
        self.superadmin.connects('superadmin')
        when(self.console).write(('vars.unlockMode', )).thenReturn(['foobar'])
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode junk')
        self.assertEqual([
         "unexpected value 'junk'. Available modes : all, common, stats, none", 'Current unlock mode is [foobar]'], self.superadmin.message_history)

    def test_all(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode all')
        verify(self.console).write(('vars.unlockMode', 'all'))
        self.assertEqual(['Unlock mode set to all'], self.superadmin.message_history)

    def test_common(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode common')
        verify(self.console).write(('vars.unlockMode', 'common'))
        self.assertEqual(['Unlock mode set to common'], self.superadmin.message_history)

    def test_stats(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode stats')
        verify(self.console).write(('vars.unlockMode', 'stats'))
        self.assertEqual(['Unlock mode set to stats'], self.superadmin.message_history)

    def test_none(self):
        self.superadmin.connects('superadmin')
        self.superadmin.message_history = []
        self.superadmin.says('!unlockmode none')
        verify(self.console).write(('vars.unlockMode', 'none'))
        self.assertEqual(['Unlock mode set to none'], self.superadmin.message_history)