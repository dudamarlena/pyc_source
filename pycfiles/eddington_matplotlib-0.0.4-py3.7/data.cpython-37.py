# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_matplotlib/data.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 523 bytes
from eddington_core import FitData
from eddington_matplotlib.plot_configuration import PlotConfiguration
from eddington_matplotlib.util import label_axes, errorbar, show_or_export, grid

def plot_data(data: FitData, plot_configuration: PlotConfiguration, output_path=None):
    label_axes(xlabel=(plot_configuration.xlabel), ylabel=(plot_configuration.ylabel))
    grid(plot_configuration.grid)
    errorbar(x=(data.x), y=(data.y), xerr=(data.xerr), yerr=(data.yerr))
    show_or_export(output_path=output_path)