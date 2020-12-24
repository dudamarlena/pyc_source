# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_angle_brackets_filter.py
# Compiled at: 2018-08-07 00:31:09
# Size of source mod 2**32: 460 bytes
"""Angle brackets filter testcases"""
from unittest import TestCase
from purewords.filters import angle_brackets_filter

class TestAngleBracketsFilterClass(TestCase):

    def setUp(self):
        self.filter = angle_brackets_filter

    def test_angle_brackets_filter(self):
        sentence = "<br>CPH<<阿阿>GG啦,要被清掉啦<>ob'_'ov>"
        answer = 'CPH'
        self.assertEqual(answer, self.filter(sentence))