# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_matplotlib/all.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1203 bytes
from eddington_core import FitData
from eddington_matplotlib.fitting import plot_fitting
from eddington_matplotlib.residuals import plot_residuals
from eddington_matplotlib.output_configuration import OutputConfiguration
from eddington_matplotlib.plot_configuration import PlotConfiguration
from eddington_matplotlib.data import plot_data

def plot_all(func, data: FitData, plot_configuration: PlotConfiguration, output_configuration: OutputConfiguration, a=None):
    if plot_configuration.plot_data:
        plot_data(data=data,
          plot_configuration=plot_configuration,
          output_path=(output_configuration.data_output_path))
    if plot_configuration.plot_fitting:
        plot_fitting(func=func,
          data=data,
          plot_configuration=plot_configuration,
          a=a,
          output_path=(output_configuration.fitting_output_path))
    if plot_configuration.plot_residuals:
        plot_residuals(func=func,
          data=data,
          plot_configuration=plot_configuration,
          a=a,
          output_path=(output_configuration.residuals_output_path))