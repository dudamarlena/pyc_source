# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminurt\iourt42\test_radio_spam_protection.py
# Compiled at: 2016-03-08 18:42:10
import sys
from mock import Mock, call
from mockito import when
from b3.config import CfgConfigParser
from b3.plugins.poweradminurt import PoweradminurtPlugin
from tests.plugins.poweradminurt.iourt42 import Iourt42TestCase

class Test_radio_spam_protection(Iourt42TestCase):

    def setUp(self):
        super(Test_radio_spam_protection, self).setUp()
        self.conf = CfgConfigParser()
        self.p = PoweradminurtPlugin(self.console, self.conf)
        self.init_default_cvar()

    def init(self, config_content=None):
        if config_content:
            self.conf.loadFromString(config_content)
        else:
            self.conf.loadFromString('\n[radio_spam_protection]\nenable: True\nmute_duration: 2\n        ')
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_conf_nominal(self):
        self.init('\n[radio_spam_protection]\nenable: True\nmute_duration: 2\n        ')
        self.assertTrue(self.p._rsp_enable)
        self.assertEqual(2, self.p._rsp_mute_duration)

    def test_conf_nominal_2(self):
        self.init('\n[radio_spam_protection]\nenable: no\nmute_duration: 1\n        ')
        self.assertFalse(self.p._rsp_enable)
        self.assertEqual(1, self.p._rsp_mute_duration)

    def test_conf_broken(self):
        self.init('\n[radio_spam_protection]\nenable: f00\nmute_duration: 0\n        ')
        self.assertFalse(self.p._rsp_enable)
        self.assertEqual(1, self.p._rsp_mute_duration)

    def test_spam(self):
        self.init('\n[radio_spam_protection]\nenable: True\nmute_duration: 2\n')
        self.joe.connects('0')
        self.console.write = Mock(wraps=lambda x: sys.stderr.write('%s\n' % x))
        self.joe.warn = Mock()

        def joe_radio(msg_group, msg_id, location, text):
            self.console.parseLine('Radio: 0 - %s - %s - "%s" - "%s"' % (msg_group, msg_id, location, text))

        def assertSpampoints(points):
            self.assertEqual(points, self.joe.var(self.p, 'radio_spamins', 0).value)

        assertSpampoints(0)
        when(self.p).getTime().thenReturn(0)
        joe_radio(3, 3, 'Patio Courtyard', 'Requesting medic. Status: healthy')
        assertSpampoints(0)
        self.assertEqual(0, self.joe.warn.call_count)
        self.assertEqual(0, self.console.write.call_count)
        when(self.p).getTime().thenReturn(0)
        joe_radio(3, 3, 'Patio Courtyard', 'Requesting medic. Status: healthy')
        assertSpampoints(8)
        self.assertEqual(0, self.joe.warn.call_count)
        self.assertEqual(0, self.console.write.call_count)
        when(self.p).getTime().thenReturn(1)
        joe_radio(3, 1, 'Patio Courtyard', 'f00')
        assertSpampoints(5)
        self.assertEqual(0, self.joe.warn.call_count)
        self.console.write.assert_has_calls([call('mute 0 2')])