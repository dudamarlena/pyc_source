# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\common\test_cmd_paset.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, Mock, call
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt41 import Iourt41TestCase
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class mixin_cmd_paset(object):

    def setUp(self):
        super(mixin_cmd_paset, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npaset: 20\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()
        self.setCvar_patcher = patch.object(self.console, 'setCvar')
        self.setCvar_mock = self.setCvar_patcher.start()
        self.moderator.connects('2')

    def assert_setCvar_calls(self, expected_calls):
        self.assertListEqual(expected_calls, self.setCvar_mock.mock_calls)

    def tearDown(self):
        super(mixin_cmd_paset, self).tearDown()
        self.sleep_patcher.stop()
        self.setCvar_patcher.stop()

    def test_nominal(self):
        self.moderator.says('!paset sv_foo bar')
        self.assert_setCvar_calls([call('sv_foo', 'bar')])
        self.assertListEqual([], self.moderator.message_history)

    def test_no_parameter(self):
        self.moderator.says('!paset')
        self.assert_setCvar_calls([])
        self.assertListEqual(['Invalid or missing data, try !help paset'], self.moderator.message_history)

    def test_no_value(self):
        self.moderator.says('!paset sv_foo')
        self.assert_setCvar_calls([call('sv_foo', '')])
        self.assertListEqual([], self.moderator.message_history)


class Test_cmd_nuke_41(mixin_cmd_paset, Iourt41TestCase):
    """
    call the mixin test using the Iourt41TestCase parent class
    """
    pass


class Test_cmd_nuke_42(mixin_cmd_paset, Iourt42TestCase):
    """
    call the mixin test using the Iourt42TestCase parent class
    """
    pass