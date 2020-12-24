# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\banlist\test_ip_banlist.py
# Compiled at: 2016-03-08 18:42:10
import sys, xml.etree.ElementTree as ET
from mock import Mock
from b3.plugins.banlist import IpBanlist
from tests.plugins.banlist import BanlistTestCase

class Test_IpBanlist(BanlistTestCase):

    def setUp(self):
        BanlistTestCase.setUp(self)
        console = Mock()
        self.ip_banlist = IpBanlist(console, ET.fromstring('\n            <ip_banlist>\n                <name>Banlist_name</name>\n                <file>F:\\temp\\banlist.txt</file>\n                <force_ip_range>no</force_ip_range>\n                <message>$name is BANNED</message>\n            </ip_banlist>\n        '))
        self.assertFalse(self.ip_banlist._forceRange)
        self.ip_banlist.plugin.info = Mock(wraps=lambda x: sys.stdout.write(x + '\n'))

    def tearDown(self):
        self.patcher_isfile.stop()
        self.patcher_open.stop()
        self.patcher_getModifiedTime.stop()

    def isBanned(self, ip):
        client = Mock()
        client.ip = ip
        return self.ip_banlist.isBanned(client)

    def test_empty_banlist(self):
        self.file_content = ''
        self.assertFalse(self.isBanned('11.22.33.44'))
        self.ip_banlist.plugin.verbose.assert_called_with("ip '11.22.33.44' not found in banlist (Banlist_name 2000-01-01 00:00:00)")

    def test_match_strict(self):
        self.file_content = '11.22.33.44:-1\n22.33.44.11foo\n33.44.55.66\n'

        def assertBanned(ip, expected_matched_line):
            self.ip_banlist.plugin.info.reset_mock()
            self.assertTrue(self.isBanned(ip))
            self.ip_banlist.plugin.info.assert_called_with("ip '%s' matches banlist entry '%s' (Banlist_name 2000-01-01 00:00:00)" % (ip, expected_matched_line))

        def assertNotBanned(ip):
            self.ip_banlist.plugin.verbose.reset_mock()
            self.assertFalse(self.isBanned(ip))
            self.ip_banlist.plugin.verbose.assert_called_with("ip '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % ip)

        assertBanned('11.22.33.44', '11.22.33.44:-1')
        assertNotBanned('11.22.33.4')
        assertBanned('22.33.44.11', '22.33.44.11foo')
        assertNotBanned('22.33.44.1')
        assertBanned('33.44.55.66', '33.44.55.66')
        assertNotBanned('33.44.55.6')

    def test_commented_entries(self):
        self.file_content = '//11.22.33.44:-1\n# 22.33.44.11foo\n//   33.44.55.66\n12.12.12.12\n'

        def assertNotBanned(ip):
            self.ip_banlist.plugin.verbose.reset_mock()
            self.assertFalse(self.isBanned(ip))
            self.ip_banlist.plugin.verbose.assert_called_with("ip '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % ip)

        assertNotBanned('11.22.33.44')
        assertNotBanned('22.33.44.11')
        assertNotBanned('33.44.55.66')

    def test_match_range(self):
        self.file_content = '11.22.33.0:-1\n22.33.44.0foo\n33.44.55.0\n44.55.0.0\n55.0.0.0\n'

        def assertBanned(ip, expected_matched_line):
            self.ip_banlist.plugin.info.reset_mock()
            self.assertTrue(self.isBanned(ip))
            self.ip_banlist.plugin.info.assert_called_with("ip '%s' matches (by range) banlist entry '%s' (Banlist_name 2000-01-01 00:00:00)" % (ip, expected_matched_line))

        def assertNotBanned(ip):
            self.ip_banlist.plugin.info.reset_mock()
            self.assertFalse(self.isBanned(ip))
            self.ip_banlist.plugin.info.assert_called_with("ip '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % ip)

        assertBanned('11.22.33.44', '11.22.33.0:-1')
        assertBanned('11.22.33.4', '11.22.33.0:-1')
        assertBanned('22.33.44.11', '22.33.44.0foo')
        assertBanned('22.33.44.1', '22.33.44.0foo')
        assertBanned('33.44.55.66', '33.44.55.0')
        assertBanned('33.44.55.6', '33.44.55.0')
        assertBanned('44.55.0.1', '44.55.0.0')
        assertBanned('44.55.1.255', '44.55.0.0')
        assertBanned('44.55.255.255', '44.55.0.0')
        assertBanned('55.0.0.1', '55.0.0.0')
        assertBanned('55.41.25.15', '55.0.0.0')
        assertBanned('55.255.255.255', '55.0.0.0')

    def test_match_force_range(self):
        self.ip_banlist._forceRange = True
        self.file_content = '11.22.33.44:-1\n22.33.44.33foo\n33.44.55.66\n'

        def assertBanned(ip, expected_matched_line):
            self.ip_banlist.plugin.info.reset_mock()
            self.assertTrue(self.isBanned(ip))
            self.ip_banlist.plugin.info.assert_called_with("ip '%s' matches (by forced range) banlist entry '%s' (Banlist_name 2000-01-01 00:00:00)" % (ip, expected_matched_line))

        def assertNotBanned(ip):
            self.ip_banlist.plugin.verbose.reset_mock()
            self.assertFalse(self.isBanned(ip))
            self.ip_banlist.plugin.verbose.assert_called_with("ip '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % ip)

        assertBanned('11.22.33.77', '11.22.33.44:-1')
        assertBanned('11.22.33.4', '11.22.33.44:-1')
        assertNotBanned('11.22.66.66')
        assertBanned('22.33.44.77', '22.33.44.33foo')
        assertBanned('22.33.44.1', '22.33.44.33foo')
        assertBanned('33.44.55.77', '33.44.55.66')
        assertBanned('33.44.55.6', '33.44.55.66')