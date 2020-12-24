# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/tests/base/test_resources.py
# Compiled at: 2016-07-19 10:55:32
import re
from unittest import TestCase
from ycyc.base import resources

class TestRegex(TestCase):

    def pattern_equal_rex(self, pattern):
        return re.compile(pattern.rstrip('$') + '$')

    def test_num_less_than(self):
        with self.assertRaises(ValueError):
            rex = re.compile(resources.Regex.num_less_than(0))

        def test_num(num):
            rex = self.pattern_equal_rex(resources.Regex.num_less_than(num))
            for i in range(num + num / 2):
                if i < num:
                    self.assertIsNotNone(rex.match(str(i)))
                else:
                    self.assertIsNone(rex.match(str(i)))

        test_num(1)
        test_num(2)
        test_num(9)
        test_num(10)
        test_num(11)
        test_num(12)
        test_num(99)
        test_num(100)
        test_num(101)
        test_num(102)
        test_num(200)
        test_num(201)
        test_num(255)
        test_num(256)
        test_num(999)
        test_num(1000)
        test_num(1001)
        test_num(1010)
        test_num(1100)
        test_num(1991)
        test_num(1999)
        test_num(2000)
        test_num(2001)
        test_num(2002)