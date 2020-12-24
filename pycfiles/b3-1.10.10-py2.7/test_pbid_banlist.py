# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\banlist\test_pbid_banlist.py
# Compiled at: 2016-03-08 18:42:10
import sys, xml.etree.ElementTree as ET
from mock import Mock
from b3.plugins.banlist import PbidBanlist
from tests.plugins.banlist import BanlistTestCase

class Test_PbidBanlist(BanlistTestCase):

    def setUp(self):
        BanlistTestCase.setUp(self)
        console = Mock()
        self.banlist = PbidBanlist(console, ET.fromstring('\n            <pbid_banlist>\n                <name>Banlist_name</name>\n                <file>F:\\temp\\banlist.txt</file>\n                <force_ip_range>no</force_ip_range>\n                <message>$name is BANNED $pbid</message>\n            </pbid_banlist>\n        '))
        self.banlist.plugin.info = Mock(wraps=lambda x: sys.stdout.write(x + '\n'))

    def isBanned(self, pbid):
        client = Mock()
        client.pbid = pbid
        return self.banlist.isBanned(client)

    def assertBanned(self, pbid, expected_debug=None):
        self.banlist.plugin.info.reset_mock()
        self.assertTrue(self.isBanned(pbid))
        self.assertTrue(self.banlist.plugin.info.called)
        if expected_debug:
            self.banlist.plugin.info.assert_called_with("PBid '%s' matches banlist entry %r (Banlist_name 2000-01-01 00:00:00)" % (pbid, expected_debug))
        else:
            args = self.banlist.plugin.info.call_args[0][0]
            self.assertTrue(args.startswith("PBid '%s' matches banlist entry " % pbid), args)

    def assertNotBanned(self, pbid):
        self.banlist.plugin.info.reset_mock()
        self.assertFalse(self.isBanned(pbid))
        self.banlist.plugin.verbose.assert_called_with("PBid '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % pbid)

    def test_empty_banlist(self):
        self.file_content = ''
        self.assertNotBanned('1234567890abcdef1234567890abcdef')

    def test_match(self):
        self.file_content = '1234567890abcdef1234567890abc000\n1234567890abcdef1234567890abc111\n1234567890abcdef1234567890abc222\n1234567890abcdef1234567890abc333\n1234567890abcdef1234567890abc444\n1234567890abcdef1234567890abc555\n'
        self.assertBanned('1234567890abcdef1234567890abc000')
        self.assertBanned('1234567890ABCDEF1234567890ABC000')
        self.assertBanned('1234567890abcdef1234567890abc111')
        self.assertBanned('1234567890ABCDEF1234567890ABC111')
        self.assertBanned('1234567890abcdef1234567890abc222')
        self.assertBanned('1234567890ABCDEF1234567890ABC222')
        self.assertBanned('1234567890abcdef1234567890abc333')
        self.assertBanned('1234567890ABCDEF1234567890ABC333')
        self.assertBanned('1234567890abcdef1234567890abc444')
        self.assertBanned('1234567890ABCDEF1234567890ABC444')
        self.assertBanned('1234567890abcdef1234567890abc555')
        self.assertBanned('1234567890ABCDEF1234567890ABC555')
        self.assertNotBanned('1234567890abcdef1234567890abc00')

    def test_commented_entries(self):
        self.file_content = '//1234567890abcdef1234567890abc000\n// 1234567890abcdef1234567890abc111\n# 1234567890abcdef1234567890abc222\n## 1234567890abcdef1234567890abc333\n'
        self.assertNotBanned('1234567890abcdef1234567890abc000')
        self.assertNotBanned('1234567890abcdef1234567890abc111')
        self.assertNotBanned('1234567890abcdef1234567890abc222')
        self.assertNotBanned('1234567890abcdef1234567890abc333')