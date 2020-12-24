# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_plot_configuration.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 4597 bytes
from unittest import TestCase
from eddington_matplotlib import PlotConfiguration

class PlotConfigurationBaseTestCase:
    decimal = 5
    xmin = 0.2
    xmax = 9.8
    func_name = 'Func Name'
    grid = False
    xcolumn = xlabel = 'x_column_example'
    ycolumn = ylabel = 'y_column_example'
    title = 'Func Name Fitting'
    residuals_title = 'Func Name Fitting - Residuals'

    @classmethod
    def build_kwargs(cls, xlabel=None, ylabel=None, title=None, residuals_title=None, grid=False):
        kwargs = dict(xlabel=xlabel,
          ylabel=ylabel,
          title=title,
          residuals_title=residuals_title,
          grid=grid)
        return kwargs

    def setUp(self):
        self.plot_configuration = (PlotConfiguration.build)(func_name=self.func_name, 
         xmin=self.xmin, 
         xmax=self.xmax, 
         xcolumn=self.xcolumn, 
         ycolumn=self.ycolumn, **self.kwargs)

    def test_xmin(self):
        self.assertAlmostEqual((self.xmin),
          (self.plot_configuration.xmin),
          places=(self.decimal),
          msg='X min value is different than expected')

    def test_xmax(self):
        self.assertAlmostEqual((self.xmax),
          (self.plot_configuration.xmax),
          places=(self.decimal),
          msg='X max value is different than expected')

    def test_xlabel(self):
        self.assertEqual((self.xlabel),
          (self.plot_configuration.xlabel),
          msg='X label is different than expected')

    def test_ylabel(self):
        self.assertEqual((self.ylabel),
          (self.plot_configuration.ylabel),
          msg='Y label is different than expected')

    def test_title(self):
        self.assertEqual((self.title),
          (self.plot_configuration.title),
          msg='Title is different than expected')

    def test_residuals_title(self):
        self.assertEqual((self.residuals_title),
          (self.plot_configuration.residuals_title),
          msg='Residuals title is different than expected')

    def test_grid(self):
        if self.grid:
            self.assertTrue((self.plot_configuration.grid), msg='Grid should be true')
        else:
            self.assertFalse((self.plot_configuration.grid), msg='Grid should be false')


class TestPlotConfigurationWithStringHeaders(TestCase, PlotConfigurationBaseTestCase):
    kwargs = PlotConfigurationBaseTestCase.build_kwargs()

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithXLabelOverride(TestCase, PlotConfigurationBaseTestCase):
    xlabel = 'some x label'
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(xlabel=xlabel)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithYLabel(TestCase, PlotConfigurationBaseTestCase):
    ylabel = 'some y label'
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(ylabel=ylabel)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithXAndYLabel(TestCase, PlotConfigurationBaseTestCase):
    xlabel = 'xlabel'
    ylabel = 'ylabel'
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(xlabel=xlabel, ylabel=ylabel)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithNumberHeaders(TestCase, PlotConfigurationBaseTestCase):
    xcolumn, ycolumn = (5.2, 2)
    kwargs = PlotConfigurationBaseTestCase.build_kwargs()
    xlabel = ylabel = None

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithTitle(TestCase, PlotConfigurationBaseTestCase):
    title = 'An Awesome Title'
    residuals_title = 'An Awesome Title - Residuals'
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(title=title)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithResidualsTitle(TestCase, PlotConfigurationBaseTestCase):
    residuals_title = 'An Awesome Residuals Title'
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(residuals_title=residuals_title)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)


class TestPlotConfigurationWithGrid(TestCase, PlotConfigurationBaseTestCase):
    grid = True
    kwargs = PlotConfigurationBaseTestCase.build_kwargs(grid=True)

    def setUp(self):
        PlotConfigurationBaseTestCase.setUp(self)