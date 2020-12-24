# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/evaluators/Evaluator.py
# Compiled at: 2020-05-07 09:46:08
# Size of source mod 2**32: 3392 bytes
import numpy as np, pandas as pd, xarray as xr
from pyplan_core import cubepy
import pyplan_core.classes.evaluators.BaseEvaluator as BaseEvaluator
import pyplan_core.classes.evaluators.CubepyEvaluator as CubepyEvaluator
import pyplan_core.classes.evaluators.NumpyEvaluator as NumpyEvaluator
import pyplan_core.classes.evaluators.PandasEvaluator as PandasEvaluator
import pyplan_core.classes.evaluators.XArrayEvaluator as XArrayEvaluator
import inspect

class Evaluator(object):
    ipytonMethods = [
     '_repr_html_', '_repr_json_',
     '_repr_jpeg_', '_repr_png_', '_repr_pretty_']

    @staticmethod
    def createInstance(result):
        if result is None:
            return BaseEvaluator()
        if Evaluator.isPandas(result):
            return PandasEvaluator()
        if Evaluator.isXArray(result):
            return XArrayEvaluator()
        if Evaluator.isMatplotlib(result):
            import pyplan_core.classes.evaluators.MatplotlibEvaluator as MatplotlibEvaluator
            return MatplotlibEvaluator()
        if Evaluator.isNumpy(result):
            return NumpyEvaluator()
        if Evaluator.isBokeh(result):
            import pyplan_core.classes.evaluators.BokehEvaluator as BokehEvaluator
            return BokehEvaluator()
        if Evaluator.isPlotly(result):
            import pyplan_core.classes.evaluators.PlotlyEvaluator as PlotlyEvaluator
            return PlotlyEvaluator()
        if Evaluator.isCubepy(result):
            return CubepyEvaluator()
        if Evaluator.isIPython(result):
            import pyplan_core.classes.evaluators.IPythonEvaluator as IPythonEvaluator
            return IPythonEvaluator()
        return BaseEvaluator()

    @staticmethod
    def isPandas(result):
        return isinstance(result, pd.DataFrame) or isinstance(result, pd.Series) or isinstance(result, pd.Index)

    @staticmethod
    def isXArray(result):
        return isinstance(result, xr.DataArray)

    @staticmethod
    def isMatplotlib(result):
        try:
            import matplotlib.artist as MatplotlibArtist
            return isinstance(result, MatplotlibArtist) or inspect.ismodule(result) and 'matplotlib.pyplot' in str(result) or isinstance(result, np.ndarray) and result.ndim > 0 and len(result) > 0 and isinstance(result.item(0), MatplotlibArtist)
        except:
            return False

    @staticmethod
    def isNumpy(result):
        return isinstance(result, np.ndarray)

    @staticmethod
    def isBokeh(result):
        try:
            from bokeh.plotting import Figure
            from bokeh.layouts import LayoutDOM
            return isinstance(result, Figure) or isinstance(result, LayoutDOM)
        except:
            return False

    @staticmethod
    def isPlotly(result):
        try:
            import plotly.graph_objs._figure as PlotlyFigue
            return isinstance(result, PlotlyFigue)
        except:
            return False

    @staticmethod
    def isCubepy(result):
        return isinstance(result, cubepy.Cube) or isinstance(result, cubepy.Index)

    @staticmethod
    def isIPython(result):
        _dir = dir(result)
        return len(list(set(_dir) & set(Evaluator.ipytonMethods))) > 0