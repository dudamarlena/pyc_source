# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_th.py
# Compiled at: 2020-04-17 01:14:36
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
from numinwords.lang_TH import Num2Word_TH

class TestNumWord(TestCase):

    def test_0(self):
        self.assertEqual(numinwords(0, lang=b'th'), b'ศูนย์')

    def test_end_with_1(self):
        self.assertEqual(numinwords(21, lang=b'th'), b'ยี่สิบเอ็ด')
        self.assertEqual(numinwords(11, lang=b'th'), b'สิบเอ็ด')
        self.assertEqual(numinwords(101, lang=b'th'), b'หนึ่งร้อยเอ็ด')
        self.assertEqual(numinwords(1201, lang=b'th'), b'หนึ่งพันสองร้อยเอ็ด')

    def test_start_20(self):
        self.assertEqual(numinwords(22, lang=b'th'), b'ยี่สิบสอง')
        self.assertEqual(numinwords(27, lang=b'th'), b'ยี่สิบเจ็ด')

    def test_start_10(self):
        self.assertEqual(numinwords(10, lang=b'th'), b'สิบ')
        self.assertEqual(numinwords(18, lang=b'th'), b'สิบแปด')

    def test_1_to_9(self):
        self.assertEqual(numinwords(1, lang=b'th'), b'หนึ่ง')
        self.assertEqual(numinwords(5, lang=b'th'), b'ห้า')
        self.assertEqual(numinwords(9, lang=b'th'), b'เก้า')

    def test_31_to_99(self):
        self.assertEqual(numinwords(31, lang=b'th'), b'สามสิบเอ็ด')
        self.assertEqual(numinwords(48, lang=b'th'), b'สี่สิบแปด')
        self.assertEqual(numinwords(76, lang=b'th'), b'เจ็ดสิบหก')

    def test_100_to_999(self):
        self.assertEqual(numinwords(100, lang=b'th'), b'หนึ่งร้อย')
        self.assertEqual(numinwords(123, lang=b'th'), b'หนึ่งร้อยยี่สิบสาม')
        self.assertEqual(numinwords(456, lang=b'th'), b'สี่ร้อยห้าสิบหก')
        self.assertEqual(numinwords(721, lang=b'th'), b'เจ็ดร้อยยี่สิบเอ็ด')

    def test_1000_to_9999(self):
        self.assertEqual(numinwords(1000, lang=b'th'), b'หนึ่งพัน')
        self.assertEqual(numinwords(2175, lang=b'th'), b'สองพันหนึ่งร้อยเจ็ดสิบห้า')
        self.assertEqual(numinwords(4582, lang=b'th'), b'สี่พันห้าร้อยแปดสิบสอง')
        self.assertEqual(numinwords(9346, lang=b'th'), b'เก้าพันสามร้อยสี่สิบหก')

    def test_10000_to_99999(self):
        self.assertEqual(numinwords(11111, lang=b'th'), b'หนึ่งหมื่นหนึ่งพันหนึ่งร้อยสิบเอ็ด')
        self.assertEqual(numinwords(22222, lang=b'th'), b'สองหมื่นสองพันสองร้อยยี่สิบสอง')
        self.assertEqual(numinwords(84573, lang=b'th'), b'แปดหมื่นสี่พันห้าร้อยเจ็ดสิบสาม')

    def test_100000_to_999999(self):
        self.assertEqual(numinwords(153247, lang=b'th'), b'หนึ่งแสนห้าหมื่นสามพันสองร้อยสี่สิบเจ็ด')
        self.assertEqual(numinwords(562442, lang=b'th'), b'ห้าแสนหกหมื่นสองพันสี่ร้อยสี่สิบสอง')
        self.assertEqual(numinwords(999999, lang=b'th'), b'เก้าแสนเก้าหมื่นเก้าพันเก้าร้อยเก้าสิบเก้า')

    def test_more_than_million(self):
        self.assertEqual(numinwords(1000000, lang=b'th'), b'หนึ่งล้าน')
        self.assertEqual(numinwords(1000001, lang=b'th'), b'หนึ่งล้านเอ็ด')
        self.assertEqual(numinwords(42478941, lang=b'th'), b'สี่สิบสองล้านสี่แสนเจ็ดหมื่นแปดพันเก้าร้อยสี่สิบเอ็ด')
        self.assertEqual(numinwords(712696969, lang=b'th'), b'เจ็ดร้อยสิบสองล้านหกแสนเก้าหมื่นหกพันเก้าร้อยหกสิบเก้า')
        self.assertEqual(numinwords(1000000000000000001, lang=b'th'), b'หนึ่งล้านล้านล้านเอ็ด')

    def test_decimal(self):
        self.assertEqual(numinwords(0.0, lang=b'th'), b'ศูนย์')
        self.assertEqual(numinwords(0.0038, lang=b'th'), b'ศูนย์จุดศูนย์ศูนย์สามแปด')
        self.assertEqual(numinwords(0.01, lang=b'th'), b'ศูนย์จุดศูนย์หนึ่ง')
        self.assertEqual(numinwords(1.123, lang=b'th'), b'หนึ่งจุดหนึ่งสองสาม')
        self.assertEqual(numinwords(35.37, lang=b'th'), b'สามสิบห้าจุดสามเจ็ด')
        self.assertEqual(numinwords(1000000.01, lang=b'th'), b'หนึ่งล้านจุดศูนย์หนึ่ง')

    def test_currency(self):
        self.assertEqual(numinwords(100, lang=b'th', to=b'currency', currency=b'THB'), b'หนึ่งร้อยบาทถ้วน')
        self.assertEqual(numinwords(100, lang=b'th', to=b'currency', currency=b'USD'), b'หนึ่งร้อยดอลลาร์')
        self.assertEqual(numinwords(100, lang=b'th', to=b'currency', currency=b'EUR'), b'หนึ่งร้อยยูโร')

    def test_currency_decimal(self):
        self.assertEqual(numinwords(0.0, lang=b'th', to=b'currency'), b'ศูนย์บาทถ้วน')
        self.assertEqual(numinwords(0.05, lang=b'th', to=b'currency'), b'ห้าสตางค์')
        self.assertEqual(numinwords(0.5, lang=b'th', to=b'currency'), b'ห้าสิบสตางค์')
        self.assertEqual(numinwords(0.99, lang=b'th', to=b'currency'), b'เก้าสิบเก้าสตางค์')
        self.assertEqual(numinwords(100.0, lang=b'th', to=b'currency'), b'หนึ่งร้อยบาทถ้วน')
        self.assertEqual(numinwords(100.23, lang=b'th', to=b'currency', currency=b'USD'), b'หนึ่งร้อยดอลลาร์ยี่สิบสามเซนต์')
        self.assertEqual(numinwords(100.24, lang=b'th', to=b'currency', currency=b'EUR'), b'หนึ่งร้อยยูโรยี่สิบสี่เซนต์')

    def test_negative(self):
        self.assertEqual(numinwords(-10, lang=b'th'), b'ติดลบสิบ')
        self.assertEqual(numinwords(-10.5, lang=b'th'), b'ติดลบสิบจุดห้า')
        self.assertEqual(numinwords(-100.0, lang=b'th', to=b'currency'), b'ติดลบหนึ่งร้อยบาทถ้วน')

    def test_round_2_decimal(self):
        n2wTH = Num2Word_TH()
        self.assertEqual(n2wTH.round_2_decimal(0.004), (b'0.00', False))
        self.assertEqual(n2wTH.round_2_decimal(0.005), (b'0.01', False))
        self.assertEqual(n2wTH.round_2_decimal(0.006), (b'0.01', False))
        self.assertEqual(n2wTH.round_2_decimal(0.0005), (
         b'0.00', False))
        self.assertEqual(n2wTH.round_2_decimal(0.984), (b'0.98', False))
        self.assertEqual(n2wTH.round_2_decimal(0.989), (b'0.99', False))
        self.assertEqual(n2wTH.round_2_decimal(0.994), (b'0.99', False))
        self.assertEqual(n2wTH.round_2_decimal(0.999), (b'1.00', False))
        self.assertEqual(n2wTH.round_2_decimal(-0.994), (b'0.99', True))
        self.assertEqual(n2wTH.round_2_decimal(-0.999), (b'1.00', True))

    def test_split_six(self):
        n2wTH = Num2Word_TH()
        self.assertEqual(n2wTH.split_six(str(123456789)), [
         b'987654', b'321'])
        self.assertEqual(n2wTH.split_six(str(12345)), [
         b'54321'])
        self.assertEqual(n2wTH.split_six(str(1234567)), [
         b'765432', b'1'])