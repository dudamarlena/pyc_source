# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/monitor_tests.py
# Compiled at: 2013-06-29 16:07:21
import sys, os, unittest, tempfile
from operator import itemgetter
from functools import partial
from monitor import *

class TestMonitor(unittest.TestCase):

    def setUp(self):
        self.incr = map(LearnMonitor._make, (
         (0, 0, 0, 0, 0, 0, 0, 0),
         (0, 0, 1, 0, 0, 0, 0, 0),
         (0, 0, 2, 0, 0, 0, 0, 0),
         (0, 0, 1, 0, 0, 0, 0, 0),
         (0, 0, 2, 0, 0, 0, 0, 0),
         (0, 0, 3, 0, 0, 0, 0, 0)))

    def test_seqmonotonicity(self):
        self.assertTrue(LearnMonitor.is_min_up('traincost', 2, self.incr))
        self.assertFalse(LearnMonitor.is_min_still('traincost', 2, self.incr[:-1]))
        self.assertTrue(LearnMonitor.is_min_up('traincost', 1, self.incr[:-1]))
        self.assertTrue(LearnMonitor.is_max_still('traincost', 2, self.incr[:-1]))

    def test_reldiff(self):
        self.assertEqual(LearnMonitor.rel_diff(init=90, final=100), 0.1)
        self.assertEqual(LearnMonitor.rel_diff(init=100, final=90), -0.1)