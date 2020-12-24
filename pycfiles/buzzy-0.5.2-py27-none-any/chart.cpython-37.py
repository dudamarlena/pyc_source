# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/explorer/parts/chart.py
# Compiled at: 2020-03-21 10:51:23
# Size of source mod 2**32: 1573 bytes
import plotly.figure_factory as ff
import plotly.graph_objects as go
CHART_TYPES = {
 'line',
 'bar',
 'heatmap',
 'area',
 'stacked_bar',
 'distplot',
 'stacked_distplot'}

def _bar_chart(row):
    return dict(x=(list(row.index)), y=(list(row)), type='bar', name=(row.name))


def _line_chart(row):
    return go.Scatter(x=(list(row.index)),
      y=(list(row)),
      mode='lines+markers',
      name=(row.name))


def _area_chart(row):
    return go.Scatter(x=(list(row.index)),
      y=(list(row)),
      hoverinfo='x+y',
      mode='lines',
      stackgroup='one',
      name=(row.name))


def _distplot(df):
    data = df.T.values
    labels = df.columns
    result = ff.create_distplot(data, labels)
    return (
     result['data'], result['layout'])


def _heatmap(df):
    return [
     go.Heatmap(z=(df.T.values), x=(list(df.index)), y=(list(df.columns)))]


def _df_to_figure(df, kind='bar'):
    """
    Helper to generate charts
    """
    plotters = dict(line=_line_chart,
      bar=_bar_chart,
      heatmap=_heatmap,
      area=_area_chart,
      stacked_bar=_bar_chart,
      distplot=_distplot,
      stacked_distplot=_distplot)
    plotter = plotters[kind]
    layout = {}
    if kind == 'heatmap':
        datapoints = plotter(df)
    elif kind.endswith('distplot'):
        datapoints, layout = plotter(df)
    else:
        datapoints = df.apply(plotter)
    layout['width'] = 1300
    if kind.startswith('stacked'):
        layout['barmode'] = 'stack'
    return dict(data=datapoints, layout=layout)