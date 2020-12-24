# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_number_filter.py
# Compiled at: 2018-08-07 00:31:14
# Size of source mod 2**32: 437 bytes
"""Number filter testcase"""
from unittest import TestCase
from purewords.filters import number_filter

class TestNumberFilterClass(TestCase):

    def setUp(self):
        self.filter = number_filter

    def test_number_filter(self):
        sentence = '我要喝八冰綠，一共25元'
        answer = '我要喝八冰綠，一共_num_元'
        self.assertEqual(answer, self.filter(sentence))