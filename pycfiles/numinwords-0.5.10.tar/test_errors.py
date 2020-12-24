# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_errors.py
# Compiled at: 2020-04-17 01:12:35
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsErrorsTest(TestCase):

    def test_NotImplementedError(self):
        with self.assertRaises(NotImplementedError):
            numinwords(100, lang=b'lalala')