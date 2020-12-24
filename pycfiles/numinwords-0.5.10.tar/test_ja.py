# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_ja.py
# Compiled at: 2020-04-17 01:13:20
from __future__ import division, print_function, unicode_literals
from unittest import TestCase
from numinwords import numinwords

def n2j(*args, **kwargs):
    return numinwords(lang=b'ja', *args, **kwargs)


class numinwordsJATest(TestCase):

    def test_low(self):
        self.assertEqual(n2j(0), b'零')
        self.assertEqual(n2j(0, prefer=[b'〇']), b'〇')
        self.assertEqual(n2j(0, reading=True), b'ゼロ')
        self.assertEqual(n2j(0, reading=True, prefer=[b'れい']), b'れい')
        self.assertEqual(n2j(1), b'一')
        self.assertEqual(n2j(1, reading=True), b'いち')
        self.assertEqual(n2j(2), b'二')
        self.assertEqual(n2j(2, reading=True), b'に')
        self.assertEqual(n2j(3), b'三')
        self.assertEqual(n2j(3, reading=True), b'さん')
        self.assertEqual(n2j(4), b'四')
        self.assertEqual(n2j(4, reading=True), b'よん')
        self.assertEqual(n2j(4, reading=True, prefer=[b'し']), b'し')
        self.assertEqual(n2j(5), b'五')
        self.assertEqual(n2j(5, reading=True), b'ご')
        self.assertEqual(n2j(6), b'六')
        self.assertEqual(n2j(6, reading=True), b'ろく')
        self.assertEqual(n2j(7), b'七')
        self.assertEqual(n2j(7, reading=True), b'なな')
        self.assertEqual(n2j(7, reading=True, prefer=[b'しち']), b'しち')
        self.assertEqual(n2j(8), b'八')
        self.assertEqual(n2j(8, reading=True), b'はち')
        self.assertEqual(n2j(9), b'九')
        self.assertEqual(n2j(9, reading=True), b'きゅう')
        self.assertEqual(n2j(10), b'十')
        self.assertEqual(n2j(10, reading=True), b'じゅう')
        self.assertEqual(n2j(11), b'十一')
        self.assertEqual(n2j(11, reading=True), b'じゅういち')
        self.assertEqual(n2j(12), b'十二')
        self.assertEqual(n2j(12, reading=True), b'じゅうに')
        self.assertEqual(n2j(13), b'十三')
        self.assertEqual(n2j(13, reading=True), b'じゅうさん')
        self.assertEqual(n2j(14), b'十四')
        self.assertEqual(n2j(14, reading=True), b'じゅうよん')
        self.assertEqual(n2j(14, reading=True, prefer=[b'し']), b'じゅうし')
        self.assertEqual(n2j(15), b'十五')
        self.assertEqual(n2j(15, reading=True), b'じゅうご')
        self.assertEqual(n2j(16), b'十六')
        self.assertEqual(n2j(16, reading=True), b'じゅうろく')
        self.assertEqual(n2j(17), b'十七')
        self.assertEqual(n2j(17, reading=True), b'じゅうなな')
        self.assertEqual(n2j(17, reading=True, prefer=[b'しち']), b'じゅうしち')
        self.assertEqual(n2j(18), b'十八')
        self.assertEqual(n2j(18, reading=True), b'じゅうはち')
        self.assertEqual(n2j(19), b'十九')
        self.assertEqual(n2j(19, reading=True), b'じゅうきゅう')
        self.assertEqual(n2j(20), b'二十')
        self.assertEqual(n2j(20, reading=True), b'にじゅう')

    def test_mid(self):
        self.assertEqual(n2j(100), b'百')
        self.assertEqual(n2j(100, reading=True), b'ひゃく')
        self.assertEqual(n2j(123), b'百二十三')
        self.assertEqual(n2j(123, reading=True), b'ひゃくにじゅうさん')
        self.assertEqual(n2j(300), b'三百')
        self.assertEqual(n2j(300, reading=True), b'さんびゃく')
        self.assertEqual(n2j(400), b'四百')
        self.assertEqual(n2j(400, reading=True), b'よんひゃく')
        self.assertEqual(n2j(600), b'六百')
        self.assertEqual(n2j(600, reading=True), b'ろっぴゃく')
        self.assertEqual(n2j(700, reading=True, prefer=[b'しち']), b'しちひゃく')
        self.assertEqual(n2j(800, reading=True), b'はっぴゃく')
        self.assertEqual(n2j(1000), b'千')
        self.assertEqual(n2j(1000, reading=True), b'せん')
        self.assertEqual(n2j(3000, reading=True), b'さんぜん')
        self.assertEqual(n2j(8000, reading=True), b'はっせん')

    def test_high(self):
        self.assertEqual(n2j(10000), b'一万')
        self.assertEqual(n2j(10000, reading=True), b'いちまん')
        self.assertEqual(n2j(12345), b'一万二千三百四十五')
        self.assertEqual(n2j(12345, reading=True), b'いちまんにせんさんびゃくよんじゅうご')
        self.assertEqual(n2j(100000000), b'一億')
        self.assertEqual(n2j(100000000, reading=True), b'いちおく')
        self.assertEqual(n2j(123456789), b'一億二千三百四十五万六千七百八十九')
        self.assertEqual(n2j(123456789, reading=True), b'いちおくにせんさんびゃくよんじゅうごまんろくせんななひゃくはちじゅうきゅう')
        self.assertEqual(n2j(1000000000000), b'一兆')
        self.assertEqual(n2j(1000000000000, reading=True), b'いっちょう')
        self.assertEqual(n2j(1234567890123), b'一兆二千三百四十五億六千七百八十九万百二十三')
        self.assertEqual(n2j(1234567890123, reading=True), b'いっちょうにせんさんびゃくよんじゅうごおくろくせんななひゃくはちじゅうきゅうまんひゃくにじゅうさん')

    def test_cardinal_float(self):
        self.assertEqual(n2j(0.0123456789, prefer=[b'〇']), b'〇点〇一二三四五六七八九')
        self.assertEqual(n2j(0.0123456789, reading=True), b'れいてんれいいちにさんよんごろくななはちきゅう')
        self.assertEqual(n2j(100000000.01), b'一億点零一')
        self.assertEqual(n2j(100000000.01, reading=True), b'いちおくてんれいいち')

    def test_ordinal(self):
        self.assertEqual(n2j(0, to=b'ordinal'), b'零番目')
        self.assertEqual(n2j(0, to=b'ordinal', reading=True, prefer=[b'れい']), b'れいばんめ')
        self.assertEqual(n2j(2, to=b'ordinal', counter=b'人'), b'二人目')
        self.assertEqual(n2j(3, to=b'ordinal', counter=b'つ'), b'三つ目')
        with self.assertRaises(NotImplementedError):
            n2j(4, to=b'ordinal', reading=True, counter=b'人')

    def test_ordinal_num(self):
        self.assertEqual(n2j(0, to=b'ordinal_num'), b'0番目')
        self.assertEqual(n2j(0, to=b'ordinal_num', reading=True), b'0ばんめ')
        self.assertEqual(n2j(2, to=b'ordinal_num', counter=b'人'), b'2人目')
        self.assertEqual(n2j(3, to=b'ordinal_num', counter=b'つ'), b'3つ目')

    def test_currency(self):
        self.assertEqual(n2j(123456789, to=b'currency'), b'一億二千三百四十五万六千七百八十九円')
        self.assertEqual(n2j(123456789, to=b'currency', reading=True), b'いちおくにせんさんびゃくよんじゅうごまんろくせんななひゃくはちじゅうきゅうえん')

    def test_year(self):
        self.assertEqual(n2j(2017, to=b'year'), b'平成二十九年')
        self.assertEqual(n2j(2017, to=b'year', reading=True), b'へいせいにじゅうくねん')
        self.assertEqual(n2j(2017, to=b'year', reading=b'arabic'), b'平成29年')
        self.assertEqual(n2j(2009, to=b'year', era=False), b'二千九年')
        self.assertEqual(n2j(2009, to=b'year', reading=True, era=False), b'にせんくねん')
        self.assertEqual(n2j(2000, to=b'year', era=False), b'二千年')
        self.assertEqual(n2j(2000, to=b'year', era=False, reading=True), b'にせんねん')
        self.assertEqual(n2j(645, to=b'year'), b'大化元年')
        self.assertEqual(n2j(645, to=b'year', reading=True), b'たいかがんねん')
        self.assertEqual(n2j(645, to=b'year'), b'大化元年')
        self.assertEqual(n2j(645, to=b'year', reading=True), b'たいかがんねん')
        self.assertEqual(n2j(-99, to=b'year', era=False), b'紀元前九十九年')
        self.assertEqual(n2j(-99, to=b'year', era=False, reading=True), b'きげんぜんきゅうじゅうくねん')
        self.assertEqual(n2j(1375, to=b'year'), b'天授元年')
        self.assertEqual(n2j(1375, to=b'year', prefer=[b'えいわ']), b'永和元年')