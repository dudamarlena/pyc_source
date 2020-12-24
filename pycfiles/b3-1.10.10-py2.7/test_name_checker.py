# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\common\test_name_checker.py
# Compiled at: 2016-03-08 18:42:10
import time
from mock import patch, call, Mock, ANY
from b3.config import CfgConfigParser
from b3.fake import FakeClient
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt41 import Iourt41TestCase
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class mixin_name_checker(object):

    def setUp(self):
        super(mixin_name_checker, self).setUp()
        self.conf = CfgConfigParser()
        self.conf.loadFromString('\n[namechecker]\ncheckdupes: True\ncheckunknown: True\ncheckbadnames: True\n        ')
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()
        self.p.onLoadConfig()
        self.p.onStartup()
        self.sleep_patcher = patch.object(time, 'sleep')
        self.sleep_patcher.start()
        self.console.say = Mock()
        self.console.write = Mock()
        self.p._ignoreTill = 0

    def tearDown(self):
        super(mixin_name_checker, self).tearDown()
        self.sleep_patcher.stop()

    def test_checkdupes_no_dup(self):
        p1 = FakeClient(self.console, name='theName', guid='p1guid')
        p1.warn = Mock()
        p1.connects('1')
        p2 = FakeClient(self.console, name='anotherName', guid='p2guid')
        p2.warn = Mock()
        p2.connects('2')
        self.assertFalse(p1.name == p2.name)
        self.p.namecheck()
        self.assertFalse(p1.warn.called)
        self.assertFalse(p2.warn.called)

    def test_checkdupes_with_dup(self):
        p1 = FakeClient(self.console, name='sameName', guid='p1guid')
        p1.warn = Mock()
        p1.connects('1')
        p2 = FakeClient(self.console, name='sameName', guid='p2guid')
        p2.warn = Mock()
        p2.connects('2')
        self.assertTrue(p1.name == p2.name)
        self.p.namecheck()
        p1.warn.assert_has_calls([call(ANY, ANY, 'badname', None, '')])
        p2.warn.assert_has_calls([call(ANY, ANY, 'badname', None, '')])
        return

    def test_checkdupes_with_player_reconnecting(self):
        p1 = FakeClient(self.console, name='sameName', guid='p1guid')
        p1.warn = Mock()
        p1.connects('1')
        p1.disconnects()
        p1.connects('2')
        self.p.namecheck()
        self.assertFalse(p1.warn.called)

    def test_checkunknown(self):
        p1 = FakeClient(self.console, name='New UrT Player', guid='p1guid')
        p1.warn = Mock()
        p1.connects('1')
        self.p.namecheck()
        p1.warn.assert_has_calls([call(ANY, ANY, 'badname', None, '')])
        return

    def test_checkbadnames(self):
        p1 = FakeClient(self.console, name='all', guid='p1guid')
        p1.warn = Mock()
        p1.connects('1')
        self.p.namecheck()
        p1.warn.assert_has_calls([call(ANY, ANY, 'badname', None, '')])
        return


class Test_cmd_nuke_41(mixin_name_checker, Iourt41TestCase):
    """
    call the mixin test using the Iourt41TestCase parent class
    """
    pass


class Test_cmd_nuke_42(mixin_name_checker, Iourt42TestCase):
    """
    call the mixin test using the Iourt42TestCase parent class
    """
    pass