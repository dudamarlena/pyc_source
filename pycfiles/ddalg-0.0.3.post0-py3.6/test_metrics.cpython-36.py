# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddalg/test_metrics.py
# Compiled at: 2020-03-30 11:18:59
# Size of source mod 2**32: 1657 bytes
import unittest
from ddalg.itree.test__tree import SimpleInterval
from ddalg.metrics.interval import jaccard_coefficient, get_boundary_margin, reciprocal_overlap
DELTA = 1e-05

class TestInterval(unittest.TestCase):

    def setUp(self):
        self.one = SimpleInterval.of(0, 100)
        self.two = SimpleInterval.of(50, 150)
        self.three = SimpleInterval.of(100, 200)
        self.four = SimpleInterval.of(0, 10)

    def test_jaccard_coefficient(self):
        self.assertAlmostEqual(0.3333333333333333, (jaccard_coefficient(self.one, self.two)), delta=DELTA)
        self.assertAlmostEqual(0.0, (jaccard_coefficient(self.one, self.three)), delta=DELTA)
        self.assertAlmostEqual(1.0, (jaccard_coefficient(self.one, self.one)), delta=DELTA)

    def test_get_boundary_margin(self):
        self.assertAlmostEqual(5.0, (get_boundary_margin(0, 100, 0.9)), delta=DELTA)
        self.assertAlmostEqual(5.0, (get_boundary_margin(-50, 50, 0.9)), delta=DELTA)
        self.assertAlmostEqual(2.5, (get_boundary_margin(0, 50, 0.9)), delta=DELTA)
        self.assertAlmostEqual(0.0, (get_boundary_margin(0, 100)), delta=DELTA)
        self.assertRaises(ValueError, get_boundary_margin, 0, 100, 10)

    def test_reciprocal_overlap(self):
        self.assertAlmostEqual(0.5, (reciprocal_overlap(self.one, self.two)), delta=DELTA)
        self.assertAlmostEqual(0.1, (reciprocal_overlap(self.one, self.four)), delta=DELTA)
        self.assertAlmostEqual(1.0, (reciprocal_overlap(self.one, self.one)), delta=DELTA)
        self.assertAlmostEqual(0.0, (reciprocal_overlap(self.one, self.three)), delta=DELTA)