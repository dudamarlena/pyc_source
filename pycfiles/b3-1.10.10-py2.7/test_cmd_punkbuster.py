# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_punkbuster.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, call
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_punkbuster(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\npunkbuster-punk: 20\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')

    def test_pb_inactive(self):
        when(self.console).write(('punkBuster.isActive', )).thenReturn(['false'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual(['Punkbuster is not active'], self.superadmin.message_history)

    def test_pb_active(self):
        when(self.console).write(('punkBuster.isActive', )).thenReturn(['true'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('punkBuster.pb_sv_command', 'test'))

    def test_pb_active(self):
        when(self.console).write(('punkBuster.isActive', )).thenReturn(['true'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punk test')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('punkBuster.pb_sv_command', 'test'))