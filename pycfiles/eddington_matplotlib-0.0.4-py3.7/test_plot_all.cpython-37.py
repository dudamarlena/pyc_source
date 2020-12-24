# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_plot_all.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 3731 bytes
from pathlib import Path
from unittest import TestCase
from mock import patch
from eddington_core import linear
import numpy as np
from eddington_matplotlib import PlotConfiguration, OutputConfiguration
from eddington_matplotlib import plot_all

class PlotAllBaseTestCase:
    data = 'data'
    xmin = 0.2
    xmax = 9.8
    func = linear
    a = np.array([1, 2])
    output_dir = Path('dir/to/output')

    def setUp(self):
        plot_data_patcher = patch('eddington_matplotlib.all.plot_data')
        plot_fitting_patcher = patch('eddington_matplotlib.all.plot_fitting')
        plot_residuals_patcher = patch('eddington_matplotlib.all.plot_residuals')
        self.plot_data = plot_data_patcher.start()
        self.plot_fitting = plot_fitting_patcher.start()
        self.plot_residuals = plot_residuals_patcher.start()
        self.addCleanup(plot_data_patcher.stop)
        self.addCleanup(plot_fitting_patcher.stop)
        self.addCleanup(plot_residuals_patcher.stop)
        self.plot_configuration = (PlotConfiguration.build)(func_name=self.func.name, 
         xmin=self.xmin, xmax=self.xmax, **self.kwargs)
        self.output_configuration = OutputConfiguration.build(func_name=(self.func.name),
          output_dir=(self.output_dir))
        plot_all(func=(self.func),
          data=(self.data),
          plot_configuration=(self.plot_configuration),
          output_configuration=(self.output_configuration),
          a=(self.a))

    def test_plot_data(self):
        if self.should_plot_data:
            self.plot_data.assert_called_once_with(data=(self.data),
              plot_configuration=(self.plot_configuration),
              output_path=(self.output_configuration.data_output_path))
        else:
            self.plot_data.assert_not_called()

    def test_plot_fitting(self):
        if self.should_plot_fitting:
            self.plot_fitting.assert_called_once_with(func=(self.func),
              data=(self.data),
              a=(self.a),
              plot_configuration=(self.plot_configuration),
              output_path=(self.output_configuration.fitting_output_path))
        else:
            self.plot_fitting.assert_not_called()

    def test_plot_residuals(self):
        if self.should_plot_residuals:
            self.plot_residuals.assert_called_once_with(func=(self.func),
              data=(self.data),
              a=(self.a),
              plot_configuration=(self.plot_configuration),
              output_path=(self.output_configuration.residuals_output_path))
        else:
            self.plot_residuals.assert_not_called()


class TestPlotAllDefault(TestCase, PlotAllBaseTestCase):
    kwargs = dict()
    should_plot_fitting = True
    should_plot_residuals = True
    should_plot_data = False

    def setUp(self):
        PlotAllBaseTestCase.setUp(self)


class TestPlotWithPlotData(TestCase, PlotAllBaseTestCase):
    kwargs = dict(plot_data=True)
    should_plot_fitting = True
    should_plot_residuals = True
    should_plot_data = True

    def setUp(self):
        PlotAllBaseTestCase.setUp(self)


class TestPlotWithoutPlotFitting(TestCase, PlotAllBaseTestCase):
    kwargs = dict(plot_fitting=False)
    should_plot_fitting = False
    should_plot_residuals = True
    should_plot_data = False

    def setUp(self):
        PlotAllBaseTestCase.setUp(self)


class TestPlotWithoutPlotResiduals(TestCase, PlotAllBaseTestCase):
    kwargs = dict(plot_residuals=False)
    should_plot_fitting = True
    should_plot_residuals = False
    should_plot_data = False

    def setUp(self):
        PlotAllBaseTestCase.setUp(self)