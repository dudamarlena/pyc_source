# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_plot_fitting.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 2862 bytes
from pathlib import Path
from unittest import TestCase
import numpy as np
from eddington_matplotlib import plot_fitting
from test.base_test_cases import PlotBaseTestCase

class PlotFittingBaseTestCase(PlotBaseTestCase):
    xrange = np.arange((PlotBaseTestCase.xmin), (PlotBaseTestCase.xmax), step=0.002)
    yrange = PlotBaseTestCase.a[0] + PlotBaseTestCase.a[1] * xrange

    def setUp(self):
        PlotBaseTestCase.setUp(self)
        plot_fitting(func=(self.func),
          data=(self.data),
          plot_configuration=(self.plot_configuration),
          a=(self.a),
          output_path=(self.output_path))

    def test_error_bar(self):
        self.check_error_bar(y=(self.data.y))

    def test_plot(self):
        self.assertEqual(1,
          (self.plt.plot.call_count),
          msg='Plot call count is different than expected')
        self.assertEqual(2,
          (len(self.plt.plot.call_args_list[0].args)),
          msg='Plot arguments count is different than expected')
        self.assertEqual(0,
          (len(self.plt.plot.call_args_list[0].kwargs)),
          msg='Plot keyword arguments count is different than expected')
        np.testing.assert_almost_equal((self.plt.plot.call_args_list[0].args[0]),
          (self.xrange),
          decimal=(self.decimal),
          err_msg='Plot x is different than expected')
        np.testing.assert_almost_equal((self.plt.plot.call_args_list[0].args[1]),
          (self.yrange),
          decimal=(self.decimal),
          err_msg='Plot y is different than expected')


class TestPlotFittingWithoutLabelsAndTitle(TestCase, PlotFittingBaseTestCase):

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingWithXlabel(TestCase, PlotFittingBaseTestCase):
    xlabel = 'xlabel'

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingWithYlabel(TestCase, PlotFittingBaseTestCase):
    ylabel = 'ylabel'

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingWithTitle(TestCase, PlotFittingBaseTestCase):
    title = 'title'

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingWithLabelsAndTitle(TestCase, PlotFittingBaseTestCase):
    xlabel = 'xlabel'
    ylabel = 'ylabel'
    title = 'title'

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingExportToFile(TestCase, PlotFittingBaseTestCase):
    output_path = Path('/dir/to/output/linear_fitting.png')

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)


class TestPlotFittingWithGrid(TestCase, PlotFittingBaseTestCase):
    grid = True

    def setUp(self):
        PlotFittingBaseTestCase.setUp(self)