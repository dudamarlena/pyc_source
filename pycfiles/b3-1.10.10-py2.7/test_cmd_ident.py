# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\iourt42\test_cmd_ident.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock, patch
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class Test_cmd_ident(Iourt42TestCase):

    def setUp(self):
        super(Test_cmd_ident, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npaident-id: 20\n\n[special]\npaident_full_level: 40\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.parser_conf._settings.update({'b3': {'time_zone': 'GMT', 'time_format': '%I:%M%p %Z %m/%d/%y'}})
        self.p.onLoadConfig()
        self.p.onStartup()
        self.console.say = Mock()
        self.console.write = Mock()
        self.moderator.connects('2')
        self.moderator.message_history = []

    def test_no_parameter(self):
        self.moderator.says('!id')
        self.assertListEqual(['Your id is @2'], self.moderator.message_history)

    def test_junk(self):
        self.moderator.says('!id qsdfsqdq sqfd qf')
        self.assertListEqual(['No players found matching qsdfsqdq'], self.moderator.message_history)

    def test_nominal_under_full_level(self):
        self.joe.pbid = 'joe_pbid'
        self.joe.connects('3')
        with patch('time.time', return_value=0.0) as (time_mock):
            self.moderator.says('!id joe')
        self.assertListEqual(['12:00AM GMT 01/01/70 @3 Joe'], self.moderator.message_history)

    def test_nominal_above_full_level(self):
        self.joe.pbid = 'joe_pbid'
        self.joe.connects('3')
        self.joe.timeAdd = 5400.0
        self.superadmin.connects('1')
        with patch('time.time', return_value=10800.0):
            self.superadmin.says('!id joe')
        self.assertListEqual(['03:00AM GMT 01/01/70 @3 Joe  [joe_pbid] since 01:30AM GMT 01/01/70'], self.superadmin.message_history)