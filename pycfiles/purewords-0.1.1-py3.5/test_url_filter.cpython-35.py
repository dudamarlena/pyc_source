# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_url_filter.py
# Compiled at: 2018-08-07 00:31:31
# Size of source mod 2**32: 598 bytes
"""Url filter testcases"""
from unittest import TestCase
from purewords.filters import url_filter

class TestUrlFilterClass(TestCase):

    def setUp(self):
        self.filter = url_filter

    def test_url_filter(self):
        sentence = '我們的官網是http://www.yoctol.com.tw' + '，有問題可以寄信至service@yoctol.com' + '或寄信到email@yoctol.edu.tw'
        answer = '我們的官網是_url_，有問題可以寄信至_url_或寄信到_url_'
        self.assertEqual(answer, self.filter(sentence))