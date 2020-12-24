# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\iourt42\test_cmd_funstuff.py
# Compiled at: 2016-03-08 18:42:10
from mock import call, Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class Test_cmd_funstuff(Iourt42TestCase):

    def setUp(self):
        super(Test_cmd_funstuff, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npafunstuff-funstuff: 20 ; set the use of funstuff <on/off>\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.write = Mock()
        self.moderator.connects('2')

    def test_missing_parameter(self):
        self.moderator.message_history = []
        self.moderator.says('!funstuff')
        self.assertListEqual(['invalid or missing data, try !help pafunstuff'], self.moderator.message_history)

    def test_junk(self):
        self.moderator.message_history = []
        self.moderator.says('!funstuff qsdf')
        self.assertListEqual(['invalid or missing data, try !help pafunstuff'], self.moderator.message_history)

    def test_on(self):
        self.moderator.says('!funstuff on')
        self.console.write.assert_has_calls([call('set g_funstuff "1"')])

    def test_off(self):
        self.moderator.says('!funstuff off')
        self.console.write.assert_has_calls([call('set g_funstuff "0"')])