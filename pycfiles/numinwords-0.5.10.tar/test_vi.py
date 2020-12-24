# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_vi.py
# Compiled at: 2020-04-17 01:14:48
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsVITest(TestCase):

    def test_0(self):
        self.assertEqual(numinwords(0, lang=b'vi'), b'không')

    def test_1_to_10(self):
        self.assertEqual(numinwords(1, lang=b'vi'), b'một')
        self.assertEqual(numinwords(2, lang=b'vi'), b'hai')
        self.assertEqual(numinwords(7, lang=b'vi'), b'bảy')
        self.assertEqual(numinwords(10, lang=b'vi'), b'mười')

    def test_11_to_19(self):
        self.assertEqual(numinwords(11, lang=b'vi'), b'mười một')
        self.assertEqual(numinwords(13, lang=b'vi'), b'mười ba')
        self.assertEqual(numinwords(14, lang=b'vi'), b'mười bốn')
        self.assertEqual(numinwords(15, lang=b'vi'), b'mười lăm')
        self.assertEqual(numinwords(16, lang=b'vi'), b'mười sáu')
        self.assertEqual(numinwords(19, lang=b'vi'), b'mười chín')

    def test_20_to_99(self):
        self.assertEqual(numinwords(20, lang=b'vi'), b'hai mươi')
        self.assertEqual(numinwords(23, lang=b'vi'), b'hai mươi ba')
        self.assertEqual(numinwords(28, lang=b'vi'), b'hai mươi tám')
        self.assertEqual(numinwords(31, lang=b'vi'), b'ba mươi mốt')
        self.assertEqual(numinwords(40, lang=b'vi'), b'bốn mươi')
        self.assertEqual(numinwords(66, lang=b'vi'), b'sáu mươi sáu')
        self.assertEqual(numinwords(92, lang=b'vi'), b'chín mươi hai')

    def test_100_to_999(self):
        self.assertEqual(numinwords(100, lang=b'vi'), b'một trăm')
        self.assertEqual(numinwords(150, lang=b'vi'), b'một trăm năm mươi')
        self.assertEqual(numinwords(196, lang=b'vi'), b'một trăm chín mươi sáu')
        self.assertEqual(numinwords(200, lang=b'vi'), b'hai trăm')
        self.assertEqual(numinwords(210, lang=b'vi'), b'hai trăm mười')

    def test_1000_to_9999(self):
        self.assertEqual(numinwords(1000, lang=b'vi'), b'một nghìn')
        self.assertEqual(numinwords(1500, lang=b'vi'), b'một nghìn năm trăm')
        self.assertEqual(numinwords(7378, lang=b'vi'), b'bảy nghìn ba trăm bảy mươi tám')
        self.assertEqual(numinwords(2000, lang=b'vi'), b'hai nghìn')
        self.assertEqual(numinwords(2100, lang=b'vi'), b'hai nghìn một trăm')
        self.assertEqual(numinwords(6870, lang=b'vi'), b'sáu nghìn tám trăm bảy mươi')
        self.assertEqual(numinwords(10000, lang=b'vi'), b'mười nghìn')
        self.assertEqual(numinwords(100000, lang=b'vi'), b'một trăm nghìn')
        self.assertEqual(numinwords(523456, lang=b'vi'), b'năm trăm hai mươi ba nghìn bốn trăm năm mươi sáu')

    def test_big(self):
        self.assertEqual(numinwords(1000000, lang=b'vi'), b'một triệu')
        self.assertEqual(numinwords(1200000, lang=b'vi'), b'một triệu hai trăm nghìn')
        self.assertEqual(numinwords(3000000, lang=b'vi'), b'ba triệu')
        self.assertEqual(numinwords(3800000, lang=b'vi'), b'ba triệu tám trăm nghìn')
        self.assertEqual(numinwords(1000000000, lang=b'vi'), b'một tỷ')
        self.assertEqual(numinwords(2000000000, lang=b'vi'), b'hai tỷ')
        self.assertEqual(numinwords(2000001000, lang=b'vi'), b'hai tỷ một nghìn')
        self.assertEqual(numinwords(1234567890, lang=b'vi'), b'một tỷ hai trăm ba mươi bốn triệu năm trăm sáu mươi bảy nghìn tám trăm chín mươi')

    def test_decimal_number(self):
        self.assertEqual(numinwords(1000.11, lang=b'vi'), b'một nghìn phẩy mười một')
        self.assertEqual(numinwords(1000.21, lang=b'vi'), b'một nghìn phẩy hai mươi mốt')

    def test_special_number(self):
        """
        Some number will have some specail rule
        """
        self.assertEqual(numinwords(21, lang=b'vi'), b'hai mươi mốt')
        self.assertEqual(numinwords(25, lang=b'vi'), b'hai mươi lăm')
        self.assertEqual(numinwords(101, lang=b'vi'), b'một trăm lẻ một')
        self.assertEqual(numinwords(105, lang=b'vi'), b'một trăm lẻ năm')
        self.assertEqual(numinwords(701, lang=b'vi'), b'bảy trăm lẻ một')
        self.assertEqual(numinwords(705, lang=b'vi'), b'bảy trăm lẻ năm')
        self.assertEqual(numinwords(1001, lang=b'vi'), b'một nghìn lẻ một')
        self.assertEqual(numinwords(1005, lang=b'vi'), b'một nghìn lẻ năm')
        self.assertEqual(numinwords(98765, lang=b'vi'), b'chín mươi tám nghìn bảy trăm sáu mươi lăm')
        self.assertEqual(numinwords(3000005, lang=b'vi'), b'ba triệu lẻ năm')
        self.assertEqual(numinwords(1000007, lang=b'vi'), b'một triệu lẻ bảy')
        self.assertEqual(numinwords(1000000017, lang=b'vi'), b'một tỷ lẻ mười bảy')
        self.assertEqual(numinwords(1000101017, lang=b'vi'), b'một tỷ một trăm lẻ một nghìn lẻ mười bảy')