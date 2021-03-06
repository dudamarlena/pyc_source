# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/nnet_tests.py
# Compiled at: 2013-07-10 19:56:04
import unittest, numpy as np
rng = np.random.RandomState()
import pandas as pd
from . import adjust_lr, shift_data, scale_data, fit_data

class TestLr(unittest.TestCase):

    def setUp(self):
        rng = np.random.RandomState(10)
        self.rx = np.array(rng.rand(15, 2, 10))
        self.xpn = pd.Panel(self.rx, items=map(lambda i: 'anchor_%d' % i, range(self.rx.shape[0])), major_axis=map(lambda i: 'track_%d' % i, range(self.rx.shape[1])), minor_axis=map(lambda i: 'position_%d' % i, range(self.rx.shape[2])))
        self.trials = range(rng.randint(0, self.rx.shape[1] * self.rx.shape[2]))

    def test_seqmonotonicity(self):
        self.assertEqual(adjust_lr([4], 0.1), 0.1)
        self.assertLess(adjust_lr([4, 5], 0.1), 0.1)
        self.assertEqual(adjust_lr([5, 3], 0.1), 0.1)
        self.assertEqual(adjust_lr([5, 5], 0.1), 0.1)

    def test_shift(self):
        oxpn = self.xpn.copy()
        xpn, meandf = shift_data(self.xpn)
        for trial in self.trials:
            track = rng.choice(xrange(self.rx.shape[1]))
            position = rng.choice(xrange(self.rx.shape[2]))
            self.assertAlmostEqual(xpn.values[:, track, position].mean(), 0)
            self.assertAlmostEqual(oxpn.values[:, track, position].mean(), meandf[(track, position)])

    def test_scale(self):
        oxpn = self.xpn.copy()
        xpn, sddf = scale_data(self.xpn)
        for trial in self.trials:
            track = rng.choice(xrange(self.rx.shape[1]))
            position = rng.choice(xrange(self.rx.shape[2]))
            self.assertAlmostEqual(xpn.values[:, track, position].std(), 1)
            self.assertAlmostEqual(oxpn.values[:, track, position].std(), sddf[(track, position)])

    def test_fit(self):
        xpn = fit_data(self.xpn)
        for trial in self.trials:
            track = rng.choice(xrange(self.rx.shape[1]))
            position = rng.choice(xrange(self.rx.shape[2]))
            self.assertLessEqual(np.max(np.abs(xpn.values[:, track, position])), 1)