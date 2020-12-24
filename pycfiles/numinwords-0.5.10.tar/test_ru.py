# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_ru.py
# Compiled at: 2020-04-17 01:14:20
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsRUTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(numinwords(100, lang=b'ru'), b'сто')
        self.assertEqual(numinwords(101, lang=b'ru'), b'сто один')
        self.assertEqual(numinwords(110, lang=b'ru'), b'сто десять')
        self.assertEqual(numinwords(115, lang=b'ru'), b'сто пятнадцать')
        self.assertEqual(numinwords(123, lang=b'ru'), b'сто двадцать три')
        self.assertEqual(numinwords(1000, lang=b'ru'), b'одна тысяча')
        self.assertEqual(numinwords(1001, lang=b'ru'), b'одна тысяча один')
        self.assertEqual(numinwords(2012, lang=b'ru'), b'две тысячи двенадцать')
        self.assertEqual(numinwords(12519.85, lang=b'ru'), b'двенадцать тысяч пятьсот девятнадцать запятая восемьдесят пять')
        self.assertEqual(numinwords(1234567890, lang=b'ru'), b'один миллиард двести тридцать четыре миллиона пятьсот шестьдесят семь тысяч восемьсот девяносто')
        self.assertEqual(numinwords(215461407892039002157189883901676, lang=b'ru'), b'двести пятнадцать нониллионов четыреста шестьдесят один октиллион четыреста семь септиллионов восемьсот девяносто два секстиллиона тридцать девять квинтиллионов два квадриллиона сто пятьдесят семь триллионов сто восемьдесят девять миллиардов восемьсот восемьдесят три миллиона девятьсот одна тысяча шестьсот семьдесят шесть')
        self.assertEqual(numinwords(719094234693663034822824384220291, lang=b'ru'), b'семьсот девятнадцать нониллионов девяносто четыре октиллиона двести тридцать четыре септиллиона шестьсот девяносто три секстиллиона шестьсот шестьдесят три квинтиллиона тридцать четыре квадриллиона восемьсот двадцать два триллиона восемьсот двадцать четыре миллиарда триста восемьдесят четыре миллиона двести двадцать тысяч двести девяносто один')
        self.assertEqual(numinwords(5, lang=b'ru'), b'пять')
        self.assertEqual(numinwords(15, lang=b'ru'), b'пятнадцать')
        self.assertEqual(numinwords(154, lang=b'ru'), b'сто пятьдесят четыре')
        self.assertEqual(numinwords(1135, lang=b'ru'), b'одна тысяча сто тридцать пять')
        self.assertEqual(numinwords(418531, lang=b'ru'), b'четыреста восемнадцать тысяч пятьсот тридцать один')
        self.assertEqual(numinwords(1000139, lang=b'ru'), b'один миллион сто тридцать девять')
        self.assertEqual(numinwords(-1, lang=b'ru'), b'минус один')
        self.assertEqual(numinwords(-15, lang=b'ru'), b'минус пятнадцать')
        self.assertEqual(numinwords(-100, lang=b'ru'), b'минус сто')

    def test_floating_point(self):
        self.assertEqual(numinwords(5.2, lang=b'ru'), b'пять запятая два')
        self.assertEqual(numinwords(561.42, lang=b'ru'), b'пятьсот шестьдесят один запятая сорок два')

    def test_to_ordinal(self):
        self.assertEqual(numinwords(1, lang=b'ru', to=b'ordinal'), b'первый')
        self.assertEqual(numinwords(5, lang=b'ru', to=b'ordinal'), b'пятый')
        self.assertEqual(numinwords(10, lang=b'ru', to=b'ordinal'), b'десятый')
        self.assertEqual(numinwords(13, lang=b'ru', to=b'ordinal'), b'тринадцатый')
        self.assertEqual(numinwords(20, lang=b'ru', to=b'ordinal'), b'двадцатый')
        self.assertEqual(numinwords(23, lang=b'ru', to=b'ordinal'), b'двадцать третий')
        self.assertEqual(numinwords(40, lang=b'ru', to=b'ordinal'), b'сороковой')
        self.assertEqual(numinwords(70, lang=b'ru', to=b'ordinal'), b'семидесятый')
        self.assertEqual(numinwords(100, lang=b'ru', to=b'ordinal'), b'сотый')
        self.assertEqual(numinwords(136, lang=b'ru', to=b'ordinal'), b'сто тридцать шестой')
        self.assertEqual(numinwords(500, lang=b'ru', to=b'ordinal'), b'пятисотый')
        self.assertEqual(numinwords(1000, lang=b'ru', to=b'ordinal'), b'тысячный')
        self.assertEqual(numinwords(1001, lang=b'ru', to=b'ordinal'), b'тысяча первый')
        self.assertEqual(numinwords(2000, lang=b'ru', to=b'ordinal'), b'двух тысячный')
        self.assertEqual(numinwords(10000, lang=b'ru', to=b'ordinal'), b'десяти тысячный')
        self.assertEqual(numinwords(1000000, lang=b'ru', to=b'ordinal'), b'миллионный')
        self.assertEqual(numinwords(1000000000, lang=b'ru', to=b'ordinal'), b'миллиардный')

    def test_to_currency(self):
        self.assertEqual(numinwords(1.0, lang=b'ru', to=b'currency', currency=b'EUR'), b'один евро, ноль центов')
        self.assertEqual(numinwords(1.0, lang=b'ru', to=b'currency', currency=b'RUB'), b'один рубль, ноль копеек')
        self.assertEqual(numinwords(1234.56, lang=b'ru', to=b'currency', currency=b'EUR'), b'одна тысяча двести тридцать четыре евро, пятьдесят шесть центов')
        self.assertEqual(numinwords(1234.56, lang=b'ru', to=b'currency', currency=b'RUB'), b'одна тысяча двести тридцать четыре рубля, пятьдесят шесть копеек')
        self.assertEqual(numinwords(10111, lang=b'ru', to=b'currency', currency=b'EUR', separator=b' и'), b'сто один евро и одиннадцать центов')
        self.assertEqual(numinwords(10121, lang=b'ru', to=b'currency', currency=b'RUB', separator=b' и'), b'сто один рубль и двадцать одна копейка')
        self.assertEqual(numinwords(10122, lang=b'ru', to=b'currency', currency=b'RUB', separator=b' и'), b'сто один рубль и двадцать две копейки')
        self.assertEqual(numinwords(10121, lang=b'ru', to=b'currency', currency=b'EUR', separator=b' и'), b'сто один евро и двадцать один цент')
        self.assertEqual(numinwords(-1251985, lang=b'ru', to=b'currency', currency=b'EUR', cents=False), b'минус двенадцать тысяч пятьсот девятнадцать евро, 85 центов')
        self.assertEqual(numinwords(b'38.4', lang=b'ru', to=b'currency', separator=b' и', cents=False, currency=b'EUR'), b'тридцать восемь евро и 40 центов')
        self.assertEqual(numinwords(b'1230.56', lang=b'ru', to=b'currency', currency=b'USD'), b'одна тысяча двести тридцать долларов, пятьдесят шесть центов')
        self.assertEqual(numinwords(b'1231.56', lang=b'ru', to=b'currency', currency=b'USD'), b'одна тысяча двести тридцать один доллар, пятьдесят шесть центов')
        self.assertEqual(numinwords(b'1234.56', lang=b'ru', to=b'currency', currency=b'USD'), b'одна тысяча двести тридцать четыре доллара, пятьдесят шесть центов')