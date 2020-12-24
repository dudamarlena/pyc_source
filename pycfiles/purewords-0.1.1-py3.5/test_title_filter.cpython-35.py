# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_title_filter.py
# Compiled at: 2018-08-07 00:31:28
# Size of source mod 2**32: 598 bytes
"""Title filter testcases"""
from unittest import TestCase
from purewords.filters import title_filter

class TestTitleFilterClass(TestCase):

    def setUp(self):
        self.filter = title_filter

    def test_title_filter(self):
        sentence = "I'm Mr. Qoo. She's Mrs. M. " + "Hello ma'am. I'd and I'll " + 'like to show you something'
        answer = "I'm Mr Qoo. She's Mrs M. Hello madam. " + "I'd and I'll like to show you something"
        self.assertEqual(answer, self.filter(sentence))