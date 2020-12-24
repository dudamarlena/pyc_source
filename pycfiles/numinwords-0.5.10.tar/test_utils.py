# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_utils.py
# Compiled at: 2020-04-17 01:14:44
from unittest import TestCase
from numinwords.utils import splitbyx

class TestUtils(TestCase):

    def test_splitbyx(self):
        self.assertEqual(list(splitbyx(str(12), 3)), [12])
        self.assertEqual(list(splitbyx(str(1234), 3)), [1, 234])
        self.assertEqual(list(splitbyx(str(12345678900), 3)), [
         12, 345, 678, 900])
        self.assertEqual(list(splitbyx(str(1000000), 6)), [1, 0])
        self.assertEqual(list(splitbyx(str(12), 3, format_int=False)), ['12'])
        self.assertEqual(list(splitbyx(str(1234), 3, format_int=False)), [
         '1', '234'])
        self.assertEqual(list(splitbyx(str(12345678900), 3, format_int=False)), [
         '12', '345', '678', '900'])
        self.assertEqual(list(splitbyx(str(1000000), 6, format_int=False)), [
         '1', '000000'])