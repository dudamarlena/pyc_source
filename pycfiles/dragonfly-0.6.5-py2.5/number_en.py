# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\number_en.py
# Compiled at: 2009-01-22 11:35:32
"""
This file implements Integer and Digits classes for the English language.

"""
from integer_base import MapIntBuilder, CollectionIntBuilder, MagnitudeIntBuilder, IntegerBase
from digits_base import DigitsBase
int_0 = MapIntBuilder({'zero': 0})
int_1_9 = MapIntBuilder(dict(zip(('one two three four five six seven eight nine').split(), range(1, 10))))
int_10_19 = MapIntBuilder(dict(zip(('ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen').split(), range(10, 20))))
int_20_90_10 = MapIntBuilder(dict(zip(('twenty thirty forty fifty sixty seventy eighty ninety').split(), range(2, 10))))
int_20_99 = MagnitudeIntBuilder(10, '<multiplier> [<remainder>]', [
 int_20_90_10], [int_1_9])
int_and_1_99 = CollectionIntBuilder('[and] <element>', [
 int_1_9, int_10_19, int_20_99])
int_100s = MagnitudeIntBuilder(100, '[<multiplier>] hundred [<remainder>]', [
 int_1_9], [int_and_1_99])
int_100big = MagnitudeIntBuilder(100, '[<multiplier>] hundred [<remainder>]', [
 int_10_19, int_20_99], [int_and_1_99])
int_1000s = MagnitudeIntBuilder(1000, '[<multiplier>] thousand [<remainder>]', [
 int_1_9, int_10_19, int_20_99, int_100s], [
 int_and_1_99, int_100s])
int_1000000s = MagnitudeIntBuilder(1000000, '[<multiplier>] million [<remainder>]', [
 int_1_9, int_10_19, int_20_99, int_100s, int_1000s], [
 int_and_1_99, int_100s, int_1000s])

class Integer(IntegerBase):
    _builders = [
     int_0, int_1_9, int_10_19, int_20_99,
     int_100s, int_100big, int_1000s, int_1000000s]


class Digits(DigitsBase):
    _digits = [
     ('zero', 'oh'), 'one', 'two', 'three', 'four',
     'five', 'six', 'seven', 'eight', 'nine']