# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_matplotlib/plot_configuration.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1813 bytes
from typing import Union
from dataclasses import dataclass
import numpy as np
from numbers import Number

@dataclass
class PlotConfiguration:
    xmin: float
    xmax: float
    xlabel = None
    xlabel: Union[(str, None)]
    ylabel = None
    ylabel: Union[(str, None)]
    title = None
    title: Union[(str, None)]
    residuals_title = None
    residuals_title: Union[(str, None)]
    grid = False
    grid: bool
    plot_fitting = True
    plot_fitting: bool
    plot_residuals = True
    plot_residuals: bool
    plot_data = False
    plot_data: bool

    @classmethod
    def build(cls, func_name, title=None, residuals_title=None, xcolumn=None, ycolumn=None, xlabel=None, ylabel=None, **kwargs):
        title = cls._PlotConfiguration__get_title(func_name=func_name, title=title)
        residuals_title = cls._PlotConfiguration__get_residuals_title(title=title,
          residuals_title=residuals_title)
        return PlotConfiguration(xlabel=cls._PlotConfiguration__get_label(xcolumn, xlabel), 
         ylabel=cls._PlotConfiguration__get_label(ycolumn, ylabel), 
         title=title, 
         residuals_title=residuals_title, **kwargs)

    @classmethod
    def get_plot_borders(cls, x):
        xmin = np.min(x)
        xmax = np.max(x)
        gap = (xmax - xmin) * 0.1
        return (xmin - gap, xmax + gap)

    @classmethod
    def __get_label(cls, header, label):
        if label is not None:
            return label
        if isinstance(header, Number):
            return
        return header

    @classmethod
    def __get_title(cls, func_name, title):
        if title is not None:
            return title
        return f"{func_name} Fitting"

    @classmethod
    def __get_residuals_title(cls, residuals_title, title):
        if residuals_title is not None:
            return residuals_title
        return f"{title} - Residuals"