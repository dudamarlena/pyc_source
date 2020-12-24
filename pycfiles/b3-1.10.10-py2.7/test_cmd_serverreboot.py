# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_serverreboot.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

@patch.object(time, 'sleep')
class Test_cmd_serverreboot(Bf3TestCase):

    def setUp(self):
        super(Test_cmd_serverreboot, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nserverreboot: 100\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_nominal(self, sleep_mock):
        when(self.console).write()
        self.superadmin.connects('god')
        self.superadmin.says('!serverreboot')
        verify(self.console).write(('admin.shutDown', ))

    def test_frostbite_error(self, sleep_mock):
        when(self.console).write(('admin.shutDown', )).thenRaise(CommandFailedError(['fOO']))
        self.superadmin.connects('god')
        self.superadmin.message_history = []
        self.superadmin.says('!serverreboot')
        self.assertEqual(['Error: fOO'], self.superadmin.message_history)