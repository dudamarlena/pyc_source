# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\common\test_cmd_paversion.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt41 import Iourt41TestCase
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase
from b3.plugins.poweradminurt import __version__ as plugin_version, __author__ as plugin_author

class mixin_cmd_version(object):

    def setUp(self):
        super(mixin_cmd_version, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npaversion-version: 20\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()
        self.console.say = Mock()
        self.console.saybig = Mock()
        self.console.write = Mock()
        self.moderator.connects('2')

    def tearDown(self):
        super(mixin_cmd_version, self).tearDown()
        self.sleep_patcher.stop()

    def test_nominal(self):
        self.moderator.message_history = []
        self.moderator.says('!version')
        self.assertEqual(['I am PowerAdminUrt version %s by %s' % (plugin_version, plugin_author)], self.moderator.message_history)


class Test_cmd_nuke_41(mixin_cmd_version, Iourt41TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt41TestCase parent class
    """
    pass


class Test_cmd_nuke_42(mixin_cmd_version, Iourt42TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt42TestCase parent class
    """
    pass