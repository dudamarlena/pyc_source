# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_get_plot_borders.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1692 bytes
from unittest import TestCase
import numpy as np
from eddington_matplotlib import PlotConfiguration

class TestGotPlotBorders(TestCase):
    decimal = 5
    size = 20

    def check(self):
        x = np.random.uniform((self.min), (self.max), size=(self.size))
        x = np.concatenate((x, np.array([self.min, self.max])), axis=None)
        np.random.shuffle(x)
        actual_min, actual_max = PlotConfiguration.get_plot_borders(x)
        self.assertAlmostEqual((self.expected_min),
          actual_min,
          places=(self.decimal),
          msg=f"Expected minimum of {x} is different than expected.")
        self.assertAlmostEqual((self.expected_max),
          actual_max,
          places=(self.decimal),
          msg=f"Expected maximum of {x} is different than expected.")

    def test_positive_borders(self):
        self.min = 1
        self.max = 6
        self.expected_min = 0.5
        self.expected_max = 6.5
        self.check()

    def test_min_border_zero(self):
        self.min = 0
        self.max = 5
        self.expected_min = -0.5
        self.expected_max = 5.5
        self.check()

    def test_min_border_negative_max_border_positive(self):
        self.min = -4
        self.max = 6
        self.expected_min = -5
        self.expected_max = 7
        self.check()

    def test_max_border_zero(self):
        self.min = -5
        self.max = 0
        self.expected_min = -5.5
        self.expected_max = 0.5
        self.check()

    def test_negative_borders(self):
        self.min = -6
        self.max = -1
        self.expected_min = -6.5
        self.expected_max = -0.5
        self.check()