# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_blank_filter.py
# Compiled at: 2018-08-07 00:31:11
# Size of source mod 2**32: 410 bytes
"""Blank filter testcase"""
from unittest import TestCase
from purewords.filters import blank_filter

class TestBlankFilterClass(TestCase):

    def setUp(self):
        self.filter = blank_filter

    def test_blank_filter(self):
        sentence = 'Hello I am ______ blank!!'
        answer = 'Hello I am _ blank!!'
        self.assertEqual(answer, self.filter(sentence))