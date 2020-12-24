# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\language\nl\number_nl.py
# Compiled at: 2009-01-22 11:42:48
"""
This file implements Integer and Digits classes for the Dutch language.

"""
from integer_base import MapIntBuilder, CollectionIntBuilder, MagnitudeIntBuilder, IntegerBase
from digits_base import DigitsBase
int_0 = MapIntBuilder({'0': 0})
int_1_9 = MapIntBuilder(dict(zip('123456789', range(1, 10))))
int_10_19 = MapIntBuilder(dict(zip(('10 11 12 13 14 15 16 17 18 19').split(), range(10, 20))))
int_20_90_10 = MapIntBuilder(dict(zip(('20 30 40 50 60 70 80 90').split(), range(2, 10))))
int_20_99 = MagnitudeIntBuilder(10, '[<remainder> en] <multiplier>', [
 int_20_90_10], [int_1_9])
int_en_1_99 = CollectionIntBuilder('[en] <element>', [
 int_1_9, int_10_19, int_20_99])
int_100s = MagnitudeIntBuilder(100, '[<multiplier>] honderd [<remainder>]', [
 int_1_9], [int_en_1_99])
int_100big = MagnitudeIntBuilder(100, '[<multiplier>] honderd [<remainder>]', [
 int_10_19, int_20_99], [int_en_1_99])
int_1000s = MagnitudeIntBuilder(1000, '[<multiplier>] duizend [<remainder>]', [
 int_1_9, int_10_19, int_20_99, int_100s], [
 int_en_1_99, int_100s])
int_1000000s = MagnitudeIntBuilder(1000000, '[<multiplier>] millioen [<remainder>]', [
 int_1_9, int_10_19, int_20_99, int_100s, int_1000s], [
 int_en_1_99, int_100s, int_1000s])

class Integer(IntegerBase):
    _builders = [
     int_0, int_1_9, int_10_19, int_20_99,
     int_100s, int_100big, int_1000s, int_1000000s]


class Digits(DigitsBase):
    _digits = [
     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']