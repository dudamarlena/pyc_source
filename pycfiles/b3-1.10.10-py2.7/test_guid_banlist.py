# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\banlist\test_guid_banlist.py
# Compiled at: 2016-03-08 18:42:10
import sys, xml.etree.ElementTree as ET
from mock import Mock
from b3.plugins.banlist import GuidBanlist
from tests.plugins.banlist import BanlistTestCase

class Test_GuidBanlist(BanlistTestCase):

    def setUp(self):
        BanlistTestCase.setUp(self)
        console = Mock()
        self.banlist = GuidBanlist(console, ET.fromstring('\n            <guid_banlist>\n                <name>Banlist_name</name>\n                <file>F:\\temp\\banlist.txt</file>\n                <force_ip_range>no</force_ip_range>\n                <message>$name is BANNED</message>\n            </guid_banlist>\n        '))
        self.banlist.plugin.info = Mock(wraps=lambda x: sys.stdout.write(x + '\n'))

    def isBanned(self, guid):
        client = Mock()
        client.guid = guid
        return self.banlist.isBanned(client)

    def assertBanned(self, guid, expected_debug=None):
        self.banlist.plugin.info.reset_mock()
        self.assertTrue(self.isBanned(guid))
        self.assertTrue(self.banlist.plugin.info.called)
        if expected_debug:
            self.banlist.plugin.info.assert_called_with("guid '%s' matches banlist entry %r (Banlist_name 2000-01-01 00:00:00)" % (guid, expected_debug))
        else:
            args = self.banlist.plugin.info.call_args[0][0]
            self.assertTrue(args.startswith("guid '%s' matches banlist entry " % guid), args)

    def assertNotBanned(self, guid):
        self.banlist.plugin.info.reset_mock()
        self.assertFalse(self.isBanned(guid))
        self.banlist.plugin.verbose.assert_called_with("guid '%s' not found in banlist (Banlist_name 2000-01-01 00:00:00)" % guid)

    def test_empty_banlist(self):
        self.file_content = ''
        self.assertNotBanned('STEAM:0:1:123456')

    def test_match(self):
        self.file_content = 'STEAM:0:1:111111\nSTEAM:0:1:222222\n  STEAM:0:1:333333\nSTEAM:0:1:444444\n64A8FC41E14548C2B8A0C50637FAF16E\n690CD3D4975A4D4B83C1960A9CA0C060\n'
        self.assertBanned('STEAM:0:1:111111')
        self.assertNotBanned('STEAM:0:1:11111')
        self.assertBanned('STEAM:0:1:222222')
        self.assertNotBanned('STEAM:0:1:22222')
        self.assertBanned('STEAM:0:1:333333')
        self.assertNotBanned('STEAM:0:1:33333')
        self.assertBanned('STEAM:0:1:444444')
        self.assertNotBanned('STEAM:0:1:44444')
        self.assertBanned('64A8FC41E14548C2B8A0C50637FAF16E')
        self.assertNotBanned('64A8FC41E14548C2B8A0C50637FAF16')
        self.assertBanned('690CD3D4975A4D4B83C1960A9CA0C060')
        self.assertNotBanned('690CD3D4975A4D4B83C1960A9CA0C06')

    def test_commented_entries(self):
        self.file_content = '//STEAM:0:1:111111\nSTEAM:0:1:222222 // comment after guid\n// STEAM:0:1:333333\n#STEAM:0:1:444444\n# 64A8FC41E14548C2B8A0C50637FAF16E\n## 690CD3D4975A4D4B83C1960A9CA0C060\n'
        self.assertNotBanned('STEAM:0:1:111111')
        self.assertBanned('STEAM:0:1:222222', 'STEAM:0:1:222222 // comment after guid')
        self.assertNotBanned('STEAM:0:1:333333')
        self.assertNotBanned('STEAM:0:1:444444')
        self.assertNotBanned('64A8FC41E14548C2B8A0C50637FAF16E')
        self.assertNotBanned('690CD3D4975A4D4B83C1960A9CA0C060')

    def test_case(self):
        self.file_content = 'steam:0:1:111111\nSTEAM:0:1:222222\nSTeam:0:1:333333\n64A8FC41e14548c2b8a0c50637FAF16E\n690cd3d4975a4d4b83c1960a9ca0c060\n'
        self.assertNotBanned('F00')
        self.assertBanned('STEAM:0:1:111111')
        self.assertBanned('STEAM:0:1:222222')
        self.assertBanned('STEAM:0:1:333333')
        self.assertBanned('64A8FC41E14548C2B8A0C50637FAF16E')
        self.assertBanned('690CD3D4975A4D4B83C1960A9CA0C060')