# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_angle_brackets_filter.py
# Compiled at: 2018-08-07 00:31:09
# Size of source mod 2**32: 460 bytes
__doc__ = 'Angle brackets filter testcases'
from unittest import TestCase
from purewords.filters import angle_brackets_filter

class TestAngleBracketsFilterClass(TestCase):

    def setUp(self):
        self.filter = angle_brackets_filter

    def test_angle_brackets_filter(self):
        sentence = "<br>CPH<<阿阿>GG啦,要被清掉啦<>ob'_'ov>"
        answer = 'CPH'
        self.assertEqual(answer, self.filter(sentence))