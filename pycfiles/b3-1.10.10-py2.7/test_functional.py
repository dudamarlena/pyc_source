# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\censor\test_functional.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from tests.plugins.censor import CensorTestCase

class Test_functional(CensorTestCase):
    """
    Test simulated in-game scenarios.
    """

    def test_joe_says_badword(self):
        self.init_plugin('\n            <configuration plugin="censor">\n                <settings name="settings">\n                    <set name="max_level">40</set>\n                    <!-- ignore bad words that have equal or less characters: -->\n                    <set name="ignore_length">3</set>\n                </settings>\n                <badwords>\n                    <penalty type="warning" reasonkeyword="default_reason"/>\n                    <badword name="foo" lang="en">\n                        <regexp>\\bf[o0]{2}\\b</regexp>\n                    </badword>\n                </badwords>\n                <badnames>\n                    <penalty type="warning" reasonkeyword="badname"/>\n                    <badname name="cunt">\n                        <word>cunt</word>\n                    </badname>\n                </badnames>\n            </configuration>\n        ')
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.joe.says('qsfdl f0o!')
        self.assertEqual(1, self.joe.warn.call_count)

    def test_cunt_connects(self):
        self.init_plugin('\n            <configuration plugin="censor">\n                <settings name="settings">\n                    <set name="max_level">40</set>\n                    <!-- ignore bad words that have equal or less characters: -->\n                    <set name="ignore_length">3</set>\n                </settings>\n                <badwords>\n                    <penalty type="warning" reasonkeyword="default_reason"/>\n                    <badword name="foo" lang="en">\n                        <regexp>\\bf[o0]{2}\\b</regexp>\n                    </badword>\n                </badwords>\n                <badnames>\n                    <penalty type="warning" reasonkeyword="badname"/>\n                    <badname name="cunt">\n                        <word>cunt</word>\n                    </badname>\n                </badnames>\n            </configuration>\n        ')
        self.joe.name = self.joe.exactName = 'cunt'
        self.joe.warn = Mock()
        self.joe.connects(0)
        self.assertEqual(1, self.joe.warn.call_count)

    def test_2_letters_badword_when_ignore_length_is_2(self):
        self.init_plugin('\n            <configuration plugin="censor">\n                <settings name="settings">\n                    <set name="max_level">40</set>\n                    <!-- ignore bad words that have equal or less characters: -->\n                    <set name="ignore_length">2</set>\n                </settings>\n                <badwords>\n                    <penalty type="warning" reasonkeyword="default_reason"/>\n                    <badword name="TG" lang="fr">\n                        <regexp>\\bTG\\b</regexp>\n                    </badword>\n                </badwords>\n                <badnames>\n                    <penalty type="warning" reasonkeyword="badname"/>\n                </badnames>\n            </configuration>\n        ')
        self.joe.warn = Mock()
        self.joe.warn.reset_mock()
        self.joe.connects(0)
        self.joe.says('tg')
        self.assertEqual(0, self.joe.warn.call_count)

    def test_2_letters_badword_when_ignore_length_is_1(self):
        self.init_plugin('\n            <configuration plugin="censor">\n                <settings name="settings">\n                    <set name="max_level">40</set>\n                    <!-- ignore bad words that have equal or less characters: -->\n                    <set name="ignore_length">1</set>\n                </settings>\n                <badwords>\n                    <penalty type="warning" reasonkeyword="default_reason"/>\n                    <badword name="TG" lang="fr">\n                        <regexp>\\bTG\\b</regexp>\n                    </badword>\n                </badwords>\n                <badnames>\n                    <penalty type="warning" reasonkeyword="badname"/>\n                </badnames>\n            </configuration>\n        ')
        self.joe.warn = Mock()
        self.joe.warn.reset_mock()
        self.joe.connects(0)
        self.joe.says('tg')
        self.assertEqual(1, self.joe.warn.call_count)

    def test_tempban_penalty_is_applied(self):
        self.init_plugin('\n            <configuration plugin="censor">\n                <settings name="settings">\n                    <set name="max_level">40</set>\n                    <!-- ignore bad words that have equal or less characters: -->\n                    <set name="ignore_length">3</set>\n                </settings>\n                <badwords>\n                    <penalty type="warning" reasonkeyword="default_reason"/>\n                    <badword name="anani" lang="en">\n                        <penalty type="tempban" reasonkeyword="cuss" duration="7d" />\n                        <regexp>\\s[a@]n[a@]n[iy!1]</regexp>\n                    </badword>\n                </badwords>\n                <badnames>\n                    <penalty type="warning" reasonkeyword="badname"/>\n                </badnames>\n            </configuration>\n        ')
        self.joe.warn = Mock(wraps=lambda *args: sys.stdout.write('warning joe %s' % repr(args)))
        self.joe.tempban = Mock(wraps=lambda *args: sys.stdout.write('tempbanning joe %s' % repr(args)))
        self.joe.warn.reset_mock()
        self.joe.tempban.reset_mock()
        self.joe.connects(0)
        self.joe.says('anani')
        self.assertEqual(0, self.joe.warn.call_count)
        self.assertEqual(1, self.joe.tempban.call_count)