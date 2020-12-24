# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/test/test_strings.py
# Compiled at: 2018-05-03 13:55:55
import unittest
from bd2k.util.strings import interpolate
from bd2k.util.strings import to_english
foo = 4
bar = 1

class TestStrings(unittest.TestCase):

    def test_interpolate(self):
        bar = 2
        self.assertEquals(interpolate('{foo}{bar}'), '42')