# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\common\test_cmd_nuke.py
# Compiled at: 2016-03-08 18:42:10
import time, thread
from mock import patch, call, Mock
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt41 import Iourt41TestCase
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class mixin_cmd_nuke(object):

    def setUp(self):
        super(mixin_cmd_nuke, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npanuke-nuke: 20\n        ')
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
        super(mixin_cmd_nuke, self).tearDown()
        self.sleep_patcher.stop()

    def test_no_argument(self):
        self.moderator.message_history = []
        self.moderator.says('!nuke')
        self.assertEqual(['Invalid data, try !help panuke'], self.moderator.message_history)
        self.console.write.assert_has_calls([])

    def test_unknown_player(self):
        self.moderator.message_history = []
        self.moderator.says('!nuke f00')
        self.assertEqual(['No players found matching f00'], self.moderator.message_history)
        self.console.write.assert_has_calls([])

    def test_joe(self):
        self.joe.connects('3')
        self.moderator.message_history = []
        self.moderator.says('!nuke joe')
        self.assertEqual([], self.moderator.message_history)
        self.assertEqual([], self.joe.message_history)
        self.console.write.assert_has_calls([call('nuke 3')])

    def test_joe_multi(self):

        def _start_new_thread(function, args):
            function(*args)

        with patch.object(thread, 'start_new_thread', wraps=_start_new_thread):
            self.joe.connects('3')
            self.moderator.message_history = []
            self.moderator.says('!nuke joe 3')
            self.assertEqual([], self.moderator.message_history)
            self.assertEqual([], self.joe.message_history)
            self.console.write.assert_has_calls([call('nuke 3'), call('nuke 3'), call('nuke 3')])


class Test_cmd_nuke_41(mixin_cmd_nuke, Iourt41TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt41TestCase parent class
    """
    pass


class Test_cmd_nuke_42(mixin_cmd_nuke, Iourt42TestCase):
    """
    call the mixin_cmd_nuke test using the Iourt42TestCase parent class
    """
    pass