# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_phone_filter.py
# Compiled at: 2018-08-07 00:31:19
# Size of source mod 2**32: 514 bytes
__doc__ = 'Phone filter testcases'
from unittest import TestCase
from purewords.filters import phone_filter

class TestPhoneFilterClass(TestCase):

    def setUp(self):
        self.filter = phone_filter

    def test_phone_filter(self):
        sentence = '薄餡手機是:0912345678, ' + '家電請打:02-2266-2266或08-449-5978'
        answer = '薄餡手機是:_phone_, 家電請打:_phone_或_phone_'
        self.assertEqual(answer, self.filter(sentence))