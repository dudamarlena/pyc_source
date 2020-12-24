# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/multicore/tests/test_utils.py
# Compiled at: 2017-08-07 06:18:36
import unittest
from multicore.utils import ranges

class TaskUtilsCase(unittest.TestCase):

    def test_ranges(self):
        li = list(ranges(range(80), number_of_workers=4))
        self.assertEqual(li, [(0, 20), (20, 40), (40, 60), (60, 80)])
        li = list(ranges(range(80), min_range_size=30, number_of_workers=4))
        self.assertEqual(li, [(0, 30), (30, 60), (60, 80)])
        li = list(ranges(range(80), min_range_size=100, number_of_workers=4))
        self.assertEqual(li, [(0, 80)])