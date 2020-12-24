# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_plot_residuals.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1962 bytes
from pathlib import Path
from unittest import TestCase
from eddington_matplotlib import plot_residuals
from test.base_test_cases import PlotBaseTestCase

class PlotResidualsBaseTestCase(PlotBaseTestCase):

    def setUp(self):
        PlotBaseTestCase.setUp(self)
        plot_residuals(func=(self.func),
          data=(self.data),
          plot_configuration=(self.plot_configuration),
          a=(self.a),
          output_path=(self.output_path))

    def test_error_bar(self):
        self.check_error_bar(y=(self.y - self.func(self.a, self.x)))

    def test_horizontal_line(self):
        self.plt.hlines(0, xmin=(self.xmin), xmax=(self.xmax), linestyles='dashed')


class TestPlotResidualsWithoutLabelsAndTitle(TestCase, PlotResidualsBaseTestCase):

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotResidualsWithXlabel(TestCase, PlotResidualsBaseTestCase):
    xlabel = 'xlabel'

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotResidualsWithYlabel(TestCase, PlotResidualsBaseTestCase):
    ylabel = 'ylabel'

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotResidualsWithTitle(TestCase, PlotResidualsBaseTestCase):
    residuals_title = 'Title - Residuals'

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotResidualsWithLabelsAndTitle(TestCase, PlotResidualsBaseTestCase):
    xlabel = 'xlabel'
    ylabel = 'ylabel'
    residuals_title = 'Title - Residuals'

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotResidualsExportToFile(TestCase, PlotResidualsBaseTestCase):
    output_path = Path('/dir/to/output/linear_fitting_residuals.png')

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)


class TestPlotFittingWithGrid(TestCase, PlotResidualsBaseTestCase):
    grid = True

    def setUp(self):
        PlotResidualsBaseTestCase.setUp(self)