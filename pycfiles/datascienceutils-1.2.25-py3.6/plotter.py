# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/plotter.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 23160 bytes
from pandas.api import types as ptypes
from bokeh.mpl import to_bokeh
from bokeh.plotting import figure
from bokeh.io import gridplot
from bokeh.plotting import figure, show, output_file, output_notebook, ColumnDataSource
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import Text, PanTool, WheelZoomTool, LinearAxis, SingleIntervalTicker, Range1d, Plot, Text, Circle, HoverTool, Triangle
from bokeh.charts import Chart, Line
from math import ceil
import itertools, numpy as np, operator, os, random, tempfile
from . import utils
AXIS_FORMATS = dict(minor_tick_in=None,
  minor_tick_out=None,
  major_tick_in=None,
  major_label_text_font_size='10pt',
  major_label_text_font_style='normal',
  axis_label_text_font_size='10pt',
  axis_line_color='#AAAAAA',
  major_tick_line_color='#AAAAAA',
  major_label_text_color='#666666',
  major_tick_line_cap='round',
  axis_line_cap='round',
  axis_line_width=1,
  major_tick_line_width=1)
BOKEH_TOOLS = 'resize,crosshair,pan,wheel_zoom,box_zoom,reset,tap,previewsave,box_select,poly_select,lasso_select'

def genColors(n, ptype=None):
    """
    """
    from bokeh.palettes import Blues3, Blues4, Blues5, Blues6, Blues7, Blues8, Blues9, Greens3, Greens4, Greens5, Greens6, Greens7, Greens8, Greens9, Reds3, Reds4, Reds5, Reds6, Reds7, Reds8, Reds9, Spectral3, Spectral4, Spectral5, Spectral6, Spectral7, Spectral8, Spectral9
    if n <= 2:
        given_val = 3
    else:
        given_val = n
    if ptype == 'magma':
        chosen = eval('Spectral' + '%s' % str(given_val))
    else:
        if ptype == 'inferno':
            chosen = eval('Greens' + '%s' % str(given_val))
        else:
            if ptype == 'plasma':
                chosen = eval('Reds' + '%s' % str(given_val))
            else:
                chosen = eval('Blues' + '%s' % str(given_val))
    if given_val == 3:
        return chosen[:n]
    else:
        return chosen


def contour_plot(dataframe, model, **kwargs):
    import matplotlib.pyplot as plt
    xx, yy = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
    Z = model.decision_function(np.c_[(xx.ravel(), yy.ravel())])
    Z = Z.reshape(xx.shape)
    if not levels:
        levels = np.linspace(Z.min(), threshold, 7)
    plot1 = plt.plot()
    (plot1.contourf)(xx, yy, Z, levels=levels, cmap=plt.cm.Blues_r, **kwargs)
    return plot1


def grid_plot(plots, chunks=2):
    grid = gridplot(list(utils.chunks(plots, size=2)))
    show(grid)


def plot_patches(bandx, bandy, **kwargs):
    p = figure(x_range=(0, 10), y_range=(0, 10), title=(kwargs.pop('title')))
    p.xaxis.axis_label = kwargs.pop('xlabel')
    p.yaxis.axis_label = kwargs.pop('ylabel')
    (p.patch)(bandx, bandy, **kwargs)
    return p


def show_image(image, **kwargs):
    p = figure(x_range=(0, 10), y_range=(0, 10), **kwargs)
    p.image(image=[image], x=0, y=0, dw=10, dh=10, palette='Spectral11')
    return p


def show_var_imp(model, X, y):
    imp = pd.DataFrame((model.feature_importances_),
      columns=[
     'Importance'],
      index=(X.columns))
    imp = imp.sort_values(['Importance'], ascending=True)
    imp[:10].plot(kind='barh')
    print(model.score(X, y))


def show_graph(graph):
    import networkx
    fout = tempfile.NamedTemporaryFile(suffix='.png')
    dot_fname = '.'.join([fout.name.split('.')[0], 'dot'])
    gr = networkx.draw_graphviz(graph)
    dot_data = tree.export_graphviz(model, out_file=dot_fname)
    os.system('dot -Tpng %s -o %s' % (dot_fname, fout.name))
    show(show_image(io.imread(fout.name)))
    os.remove(dot_fname)


def show_tree_model(model, model_type='tree'):
    if not model_type in ('tree', 'randomforest', 'xgboost'):
        raise AssertionError
    else:
        from sklearn import tree
        import pydotplus
        from skimage import io
        if model_type == 'tree':
            fout = tempfile.NamedTemporaryFile(suffix='.png')
            dot_fname = '.'.join([fout.name.split('.')[0], 'dot'])
            dot_data = tree.export_graphviz(model, out_file=dot_fname)
            os.system('dot -Tpng %s -o %s' % (dot_fname, fout.name))
            show(show_image(io.imread(fout.name)))
            os.remove(dot_fname)
        else:
            if model_type == 'randomforest':
                graph_plots = list()
                if len(model.estimators_) > 10:
                    print("Sorry more that 10 trees can't be displayed")
                    return
                for tree_model in model.estimators_:
                    fout = tempfile.NamedTemporaryFile(suffix='.png')
                    dot_fname = '.'.join([fout.name.split('.')[0], 'dot'])
                    dot_data = tree.export_graphviz(tree_model, out_file=dot_fname)
                    os.system('dot -Tpng %s -o %s' % (dot_fname, fout.name))
                    graph_plots.append(show_image(io.imread(fout.name)))

                grid = gridplot(list(utils.chunks(graph_plots, size=3)))
                show(grid)
                os.remove(dot_fname)
            else:
                import xgboost
                xgboost.to_graphviz(model)
                fout = tempfile.NamedTemporaryFile(suffix='.png')
                dot_fname = '.'.join([fout.name.split('.')[0], 'dot'])
                dot_data = tree.export_graphviz(tree_model, out_file=dot_fname)
                os.system('dot -Tpng %s -o %s' % (dot_fname, fout.name))
                show(show_image(io.imread(fout.name)))
                os.remove(dot_fname)


def show_model_interpretation(model, model_type='randomforest'):
    import lime


def lineplot(df, legend=None, title=None, **kwargs):
    assert all([ptypes.is_numeric_dtype(df[col]) for col in df.columns]), 'Only numeric datatypes'
    if not title:
        title = '%s Vs %s' % (kwargs.get('xcol'), kwargs.get('ycol'))
    return Line(df, title=title, legend=True)


def timestamp(datetimeObj):
    timestamp = (datetimeObj - datetime(1970, 1, 1)).total_seconds()
    return timestamp


def month_year_format(datetimeObj):
    return str(datetimeObj.strftime('%b-%Y'))


def multi_line_plot(dataframe, idx=None):
    if idx:
        dataframe.set_index(idx)
        dataframe.drop(idx, 1, inplace=True)
    numlines = len(dataframe.columns)
    mypalette = genColors(numlines, ptype='magma')
    p = figure(width=500, height=300, x_axis_type='datetime')
    p.multi_line(xs=([dataframe.index.values] * numlines), ys=[dataframe[name].values for name in dataframe],
      line_color=mypalette,
      line_width=5)
    return p


def plot_twin_y_axis_scatter(conn, query1=None, query2=None, xy1={}, xy2={}):
    """
    Plots twin y axis scatter plot you just have to give conn sqlalchemy obj and
    two query/dictionary of x and y values
    :param conn: Sqlaclhemy connection object
    :param query1: query 1 for x and y1
    :param query2: query 2 for x and y2
    :param xy1: dictionary containing x and y key values
    :param xy2: dictionary containing x and y key values
    :return: Bokeh plot object (script,div)
    """
    if query1:
        result = conn.execute(query1)
        plot_data1 = {'x':[],  'y':[]}
        for row in result:
            if row[0] and row[1]:
                plot_data1['x'].append(float(row[0]))
                plot_data1['y'].append(str(row[1]))

    elif isinstance(xy1, dict):
        if xy1:
            plot_data1 = xy1
        else:
            raise ValueError('Parameters values not given properly')
    else:
        if query2:
            result = conn.execute(query2)
            plot_data2 = {'x':[],  'y':[]}
            for row in result:
                if row[0] and row[1]:
                    plot_data2['x'].append(float(row[0]))
                    plot_data2['y'].append(str(row[1]))

        elif isinstance(xy2, dict) and xy2:
            plot_data2 = xy2
        else:
            raise ValueError('Parameters values not given properly')
    renderer_source = ColumnDataSource({'x':plot_data1['x'],  'y':plot_data1['y']})
    renderer_source2 = ColumnDataSource({'x':plot_data2['x'],  'y':plot_data2['y']})
    bokeh_plot = BokehTwinLinePlot(plot_data1, plot_data2, xlabel='No. of Accounts',
      ylabel='No. of. Leave Transactions',
      ylabel2='No. of services')
    plot = bokeh_plot.get_plot()
    plot = bokeh_plot.add_text(plot)
    triangle_glyph = Triangle(x='x',
      y='y',
      size=15,
      fill_color='#4682B4',
      fill_alpha=0.8,
      line_color='#4682B4',
      line_width=0.5,
      line_alpha=0.5)
    circle_glyph = Circle(x='x',
      y='y',
      size=15,
      fill_color='#d24726',
      fill_alpha=0.8,
      line_color='#d24726',
      line_width=0.5,
      line_alpha=0.5)
    triangle_renderer = plot.add_glyph(renderer_source, triangle_glyph)
    circle_renderer = plot.add_glyph(renderer_source2, circle_glyph, y_range_name='y_range2')
    tooltips = '@index'
    plot.add_tools(HoverTool(tooltips=tooltips, renderers=[triangle_renderer, circle_renderer]))
    plot.add_tools(PanTool(), WheelZoomTool())
    return plot


class BokehTwinLinePlot(object):
    __doc__ = '\n    Class for creating basic bokeh structure of two y axis and one x axis\n    '

    def __init__(self, plot_data1, plot_data2, xlabel='x', ylabel='y', ylabel2='y2'):
        self.plot_data1 = plot_data1
        self.plot_data2 = plot_data2
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ylabel2 = ylabel2

    def get_plot(self):
        """
        Creates the basic bokeh plot with xrange, y range
        :return: Boekh plot obj.
        """
        min_x_range, max_x_range = self.get_x_ranges()
        min_y_range, max_y_range = self.get_y_ranges(self.plot_data1)
        min_y2_range, max_y2_range = self.get_y_ranges(self.plot_data2)
        xdr = Range1d(min_x_range - min_x_range / 1.2, max_x_range + max_x_range / 1.2)
        ydr = Range1d(min_y_range - min_y_range / 1.2, max_y_range + max_y_range / 1.2)
        ydr2 = Range1d(min_y2_range - min_y2_range / 10, max_y2_range + max_y2_range / 10)
        plot = Plot(x_range=xdr,
          y_range=ydr,
          extra_y_ranges={'y_range2': ydr2},
          title='',
          plot_width=550,
          plot_height=550,
          outline_line_color=None,
          toolbar_location=None)
        return plot

    def add_axes(self, plot):
        """
        Adds axis to Bokeh plot Obj
        :param plot: Bokeh plot obj. from get_plot method
        :return: Bokeh plot obj
        """
        min_x_range, max_x_range = self.get_x_ranges()
        min_y_range, max_y_range = self.get_y_ranges(self.plot_data1)
        min_y2_range, max_y2_range = self.get_y_ranges(self.plot_data2)
        x_interval = utils.roundup(max_x_range)
        y_interval = utils.roundup(max_y_range)
        y2_interval = utils.roundup(max_y2_range)
        xaxis = LinearAxis(SingleIntervalTicker(interval=x_interval), axis_label=self.xlabel, **AXIS_FORMATS)
        yaxis = LinearAxis(SingleIntervalTicker(interval=y_interval), axis_label=self.ylabel, **AXIS_FORMATS)
        yaxis2 = LinearAxis(SingleIntervalTicker(interval=y2_interval), y_range_name='y_range2', axis_label=self.ylabel2, **AXIS_FORMATS)
        plot.add_layout(xaxis, 'below')
        plot.add_layout(yaxis, 'left')
        plot.add_layout(yaxis2, 'right')
        return plot

    def add_text(self, plot):
        """
        Adds text to Bokeh plot
        :param plot: Bokeh plot obj.
        :return: Bokeh plot obj.
        """
        plot = self.add_axes(plot)
        return plot

    def get_x_ranges(self):
        """
        get the minimum and maximum values of x
        :return: Minimum x value, Maximum x value
        """
        plot_data1_x = list(self.plot_data1['x'])
        plot_data2_x = list(self.plot_data2['x'])
        if not plot_data1_x:
            plot_data1_x = [
             0]
        if not plot_data2_x:
            plot_data2_x = [
             0]
        min_x_range = min([min(plot_data1_x), min(plot_data2_x)])
        max_x_range = max([max(plot_data1_x), max(plot_data2_x)])
        return (
         min_x_range, max_x_range)

    def get_y_ranges(self, plot_data):
        """
        get the minimum and maximum values of y
        :return: Minimum y value, Maximum y value
        """
        plot_data_y = map(float, list(plot_data['y']))
        if not plot_data_y:
            plot_data_y = [
             0]
        min_y_range = min(plot_data_y)
        max_y_range = max(plot_data_y)
        return (min_y_range, max_y_range)


def histogram(histDF, values, bayesian_bins=False, **kwargs):
    if not bayesian_bins:
        from bokeh.charts import Histogram
        return Histogram((histDF[values]), **kwargs)
    else:
        import numpy as np
        bins = utils.bayesian_blocks(histDF[values])
        p1 = figure(title=(kwargs.pop('title', 'Histogram of %s' % values)), tools='save',
          background_fill_color='#E8DDCB')
        hist, edges = np.histogram((histDF[values]), bins=bins)
        p1.quad(top=hist, bottom=0, left=(edges[:-1]), right=(edges[1:]), fill_color='#036564',
          line_color='#033649')
        p1.legend.location = 'top_left'
        p1.xaxis.axis_label = 'x'
        p1.yaxis.axis_label = 'Frequency'
        return p1


def barplot(barDF, xlabel, ylabel, title='Bar Plot', agg='sum', **kwargs):
    from bokeh.charts import Bar
    barplot = Bar(barDF, xlabel, values=ylabel, agg=agg, title=title, **kwargs)
    return barplot


def boxplot(boxDF, values_label, xlabel, title='boxplot', **kwargs):
    from bokeh.charts import BoxPlot
    boxplot = BoxPlot(boxDF, values=values_label, label=xlabel, color=xlabel, title=title, **kwargs)
    return boxplot


def heatmap(heatMapDF, xlabel, ylabel, value_label, title='heatmap', palette=None, width=500, height=500, **kwargs):
    from bokeh._legacy_charts import HeatMap
    if not palette:
        from bokeh.palettes import RdBu11 as palette_tmpl
        palette = palette_tmpl
    hm = HeatMap(heatMapDF, x=xlabel, y=ylabel, values=value_label, title=title, 
     height=height, width=width, palette=palette, **kwargs)
    return hm


def scatterplot(scatterDF, xcol, ycol, xlabel=None, ylabel=None, groupCol=None, plttitle=None, **kwargs):
    fig_kwargs = kwargs.get('figure')
    if fig_kwargs:
        p = figure(title=plttitle, **fig_kwargs)
    else:
        p = figure(title=plttitle)
    from bokeh.charts import Scatter
    if not xlabel:
        xlabel = xcol
    else:
        if not ylabel:
            ylabel = ycol
        if not groupCol:
            kwargs.pop('groupCol', None)
            (p.circle)(scatterDF[xcol], scatterDF[ycol], size=5, **kwargs)
        else:
            groups = list(scatterDF[groupCol].unique())
            colors = genColors((len(groups)), ptype='plasma')
            colors = list(np.hstack([colors] * 20))
            for group in groups:
                color = colors.pop(random.randrange(len(colors)))
                p.circle((scatterDF[(scatterDF[groupCol] == group)][xcol]), (scatterDF[(scatterDF[groupCol] == group)][ycol]),
                  size=5,
                  color=color)

    p.xaxis.axis_label = str(xcol)
    p.yaxis.axis_label = str(ycol)
    return p


def pieChart(df, column, **kwargs):
    wedges = []
    wedge_sum = 0
    total = len(df)
    colors = genColors((df[column].nunique()), ptype='magma')
    for i, (key, val) in enumerate(df.groupby(column).size().iteritems()):
        wedge = dict()
        pct = val / float(total)
        wedge['start'] = 2 * np.pi * wedge_sum
        wedge_sum = val / float(total) + wedge_sum
        wedge['end'] = 2 * np.pi * wedge_sum
        wedge['name'] = '{}-{:.2f} %'.format(key, pct)
        wedge['color'] = colors.pop()
        wedges.append(wedge)

    p = figure(x_range=(-1, 1), y_range=(-1, 1), x_axis_label=column, **kwargs)
    for i, wedge in enumerate(wedges):
        p.wedge(x=0, y=0, radius=1, start_angle=(wedge['start']), end_angle=(wedge['end']), color=(wedge['color']),
          legend=(wedge['name']))

    return p


def mcircle(p, x, y, **kwargs):
    (p.circle)(x, y, **kwargs)


def mscatter(p, x, y, typestr='o'):
    p.scatter(x, y, marker=typestr, alpha=0.5)


def mtext(p, x, y, textstr, **kwargs):
    p.text(x, y, text=[textstr], text_color=(kwargs.get('text_color')),
      text_align='center',
      text_font_size='10pt')


def boxplot(xrange, yrange, boxSource, xlabel='x', ylabel='y', colors=list()):
    p = figure(title='"Party" Disturbance Calls in LA',
      x_range=xrange,
      y_range=yrange)
    p.plot_width = 900
    p.plot_height = 400
    p.toolbar_location = 'left'
    p.rect(xlabel, ylabel, 1, 1, source=boxSource, color=colors, line_color=None)
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = '10pt'
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi / 3
    return p


def sb_boxplot(dataframe, quant_field, cat_fields=None, facetCol=None):
    if not quant_field:
        raise AssertionError
    else:
        if cat_fields:
            assert len(cat_fields) <= 2
            import seaborn as sns
            sns.set_style('whitegrid')
            tips = sns.load_dataset('tips')
            if not facetCol:
                ax = cat_fields or sns.boxplot(dataframe[quant_field])
            else:
                if len(cat_fields) == 1:
                    sns.boxplot(x=(cat_fields[0]), y=quant_field, data=dataframe)
                else:
                    sns.boxplot(x=(cat_fields[0]), y=quant_field, hue=(cat_fields[1]),
                      data=dataframe,
                      palette='Set3',
                      linewidth=2.5)
        else:
            fg = sns.FacetGrid(dataframe, col=facetCol, size=4, aspect=7)
            fg.map(sns.boxplot, cat_fields[0], quant_field, cat_fields[1]).despine(left=True).add_legend(title=(cat_fields[1]))


def sb_heatmap(df, label):
    import seaborn as sns
    sns.set(style='white')
    sns.heatmap((df.T), mask=(df.T.isnull()), annot=True, fmt='.0%')


def sb_piechart(df, column):
    pass


def sb_distplot(df, column, **kwargs):
    import seaborn as sns
    sns.set(style='white')
    row = kwargs.get('row', None)
    col = kwargs.get('col', None)
    facet = sns.FacetGrid(df, aspect=4, row=row, col=col)
    facet.map((sns.kdeplot), column, shade=True)
    facet.set(xlim=(df[column], df[column].max()))
    facet.add_legend()
    facet.show()


def sb_violinplot(series, dataframe=None, groupCol=None, **kwargs):
    import seaborn as sns
    sns.set(style='white')
    import pandas as pd
    if not groupCol:
        assert isinstance(series, pd.Series)
        plt = (sns.violinplot)(x=series, **kwargs)
    else:
        if not (dataframe and groupCol):
            raise AssertionError
        elif not isinstance(series, str):
            raise AssertionError
        plt = (sns.violinplot)(x=groupCol, y=series, data=dataframe, **kwargs)
    plt.show()


def sb_jointplot(series1, series2):
    import numpy as np, seaborn as sns
    sns.set(style='white')
    plt = sns.jointplot(series1, series2, kind='kde', size=7, space=0)


def facets_dashboard(dataframe, **kwargs):
    jsonstr = dataframe.to_csv(orient='records')
    from IPython.core.display import display, HTML
    HTML_TEMPLATE = '<link rel="import" href="/nbextensions/facets-dist/facets-jupyter.html">\n            <facets-dive id="elem" height="600"></facets-dive>\n            <script>\n              var data = JSON.parse(\'{jsonstr}\');\n              document.querySelector("#elem").data = data;\n            </script>'
    html = HTML_TEMPLATE.format(jsonstr=jsonstr)
    display(HTML(html))


def hyper_plot(dataframe, pca_plot=False, cluster=False, n_clusters=None, **kwargs):
    import hypertools as hyp
    if pca_plot:
        hyp.tools.describe_pca(dataframe)
    else:
        if cluster:
            assert n_clusters
            (hyp.plot)(dataframe, 'o', n_clusters=n_clusters, **kwargs)
        else:
            (hyp.plot)(dataframe, 'o', **kwargs)


def gp_pointplot(geo_dataframe, geo_locations, scale_column):
    import geoplot.crs as gcrs, geoplot as gplt
    proj = gcrs.AlbersEqualArea()
    ax = (gplt.polyplot)(geo_locations, projection=proj, 
     zorder=-1, 
     linewidth=0.5, 
     legend_kwargs={'frameon':False, 
 'loc':'lower right'}, **kwargs)
    (gplt.pointplot)(geo_dataframe, scale=scale_column, 
     ax=ax, 
     projection=proj, **kwargs)


def gp_polyplot(geo_dataframe):
    import geoplot as gplt


def candle_stick_plot():
    import matplotlib.ticker as mticker
    from matplotlib.finance import candlestick_ohlc
    fig = plt.figure(figsize=(12, 8))
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    temp_df = df[(df['Date'] > '2017-05-01')]
    ohlc = []
    for ind, row in temp_df.iterrows():
        ol = [
         row['Date_mpl'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']]
        ohlc.append(ol)

    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price in USD', fontsize=12)
    plt.title('Candlestick chart for Bitcoin', fontsize=15)
    plt.subplots_adjust(left=0.09, bottom=0.2, right=0.94, top=0.9, wspace=0.2, hspace=0)
    plt.show()


def show_volume(dataframe, cols, vec_cols=None, plt_type='vol'):
    import ipyvolume as ipv
    if plt_type == 'vol':
        assert len(cols) == 3, 'Only 3d Volumes'
        ipv.quickvolshow((dataframe[cols]), level=[0.25, 0.75], opacity=0.03, level_width=0.1, data_min=0, data_max=1)
    else:
        if plt_type == 'scatter':
            ipv.quickscatter((dataframe[cols]), size=1, marker='sphere')
        else:
            if plt_type == 'quiver':
                assert vec_cols, 'Vector Columns needed'
                x, y, z = dataframe[cols]
                u, v, w = dataframe[vec_cols]
                ipv.quickquiver(x, y, z, u, v, w, size=5)
            else:
                if plt_type('mesh'):
                    m = ipv.plot(x, y, z, wireframe=False)
                    ipv.squarelim()
                    ipv.show()
                else:
                    raise 'Unsupported plot type'