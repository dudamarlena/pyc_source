# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: e:\Remote\chartpy\chartpy\chart.py
# Compiled at: 2018-02-24 12:51:36
# Size of source mod 2**32: 4007 bytes
from __future__ import division
__author__ = 'saeedamen'
from chartpy.twitter import Twitter
from chartpy.chartconstants import ChartConstants
from chartpy.style import Style
from chartpy.engine import EngineMatplotlib, EngineBokeh, EngineBqplot, EnginePlotly, EngineVisPy
import pandas

class Chart(object):

    def __init__(self, df=None, engine=None, chart_type=None, style=None):
        self.df = None
        self.engine = ChartConstants().chartfactory_default_engine
        self.style = Style()
        self.chart_type = 'line'
        self.is_plotted = False
        if df is not None:
            self.df = df
        if engine is not None:
            self.engine = engine
        if chart_type is not None:
            self.chart_type = chart_type
        if style is not None:
            self.style = style

    def plot(self, df=None, engine=None, chart_type=None, style=None, twitter_msg=None, twitter_on=False):
        if style is None:
            style = self.style
        else:
            if df is None:
                df = self.df
            elif engine is None:
                try:
                    engine = style.engine
                except:
                    engine = self.engine

                if chart_type is None:
                    chart_type = self.chart_type
                    try:
                        if style.chart_type is not None:
                            chart_type = style.chart_type
                    except:
                        pass

            else:
                if isinstance(df, list):
                    for i in range(0, len(df)):
                        if isinstance(df[i], pandas.Series):
                            df[i] = pandas.DataFrame(df[i])

                else:
                    if isinstance(df, pandas.Series):
                        df = pandas.DataFrame(df)
                if engine is None:
                    fig = self.get_engine(engine).plot_chart(df, style, chart_type)
                else:
                    if isinstance(engine, str):
                        fig = self.get_engine(engine).plot_chart(df, style, chart_type)
                    else:
                        fig = self.engine.plot_chart(df, style, chart_type)
            if twitter_on:
                twitter = Twitter()
                twitter.auto_set_key()
                twitter.update_status(twitter_msg, picture=(style.file_output))
        self.is_plotted = True
        return fig

    def get_engine(self, engine):
        if engine is None:
            return self.get_engine(self.engine)
        else:
            if engine == 'matplotlib':
                return EngineMatplotlib()
            else:
                if engine == 'bokeh':
                    return EngineBokeh()
                if engine == 'bqplot':
                    return EngineBqplot()
                if engine == 'vispy':
                    return EngineVisPy()
            if engine == 'plotly':
                return EnginePlotly()

    def _iplot(self, data_frame, engine=None, chart_type=None, style=None):
        return Chart.get_engine(engine).plot_chart(data_frame, style, chart_type)