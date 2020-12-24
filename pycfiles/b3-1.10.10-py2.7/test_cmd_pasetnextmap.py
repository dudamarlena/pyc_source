# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\common\test_cmd_pasetnextmap.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, Mock
from mockito import when, verify
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt41 import Iourt41TestCase
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class mixin_cmd_pasetnextmap(object):

    def setUp(self):
        super(mixin_cmd_pasetnextmap, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[commands]\npasetnextmap-snmap: 20\n        ')
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
        super(mixin_cmd_pasetnextmap, self).tearDown()
        self.sleep_patcher.stop()

    def test_missing_parameter(self):
        self.moderator.clearMessageHistory()
        self.moderator.says('!snmap')
        self.assertEqual(['Invalid or missing data, try !help pasetnextmap'], self.moderator.message_history)

    def test_existing_map(self):
        when(self.console).getMapsSoundingLike('f00').thenReturn('f00')
        self.moderator.clearMessageHistory()
        self.moderator.says('!snmap f00')
        verify(self.console).getMapsSoundingLike('f00')
        self.assertEqual(['nextmap set to f00'], self.moderator.message_history)

    def test_suggestions(self):
        when(self.console).getMapsSoundingLike('f00').thenReturn(['f001', 'foo2'])
        self.moderator.clearMessageHistory()
        self.moderator.says('!snmap f00')
        verify(self.console).getMapsSoundingLike('f00')
        self.assertEqual(['do you mean : f001, foo2 ?'], self.moderator.message_history)


class Test_cmd_nuke_41(mixin_cmd_pasetnextmap, Iourt41TestCase):
    """
    call the mixin test using the Iourt41TestCase parent class
    """
    pass


class Test_cmd_nuke_42(mixin_cmd_pasetnextmap, Iourt42TestCase):
    """
    call the mixin test using the Iourt42TestCase parent class
    """
    pass