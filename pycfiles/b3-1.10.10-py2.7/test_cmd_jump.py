# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\iourt42\test_cmd_jump.py
# Compiled at: 2016-03-08 18:42:10
from mock import call, Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class Test_cmd_jump(Iourt42TestCase):

    def setUp(self):
        super(Test_cmd_jump, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npajump-jump: 20           ; change game type to Jump\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.write = Mock()
        self.moderator.connects('2')

    def test_nominal(self):
        self.moderator.message_history = []
        self.moderator.says('!jump')
        self.console.write.assert_has_calls([call('set g_gametype "9"')])
        self.assertEqual(['game type changed to Jump'], self.moderator.message_history)