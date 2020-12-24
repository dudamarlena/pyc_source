# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webplotlib/chart_builders.py
# Compiled at: 2011-05-24 19:56:22
import itertools
from StringIO import StringIO
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
font_params = {'sans-serif': [
                'Helvetica Neue', 'Arial', 'Liberation Sans',
                'FreeSans', 'sans-serif'], 
   'size': 13.0}
matplotlib.rc('font', **font_params)
colors_default = itertools.cycle([
 '#7C8BD9',
 '#DE2D26',
 '#2CA25F'])
linestyles_default = itertools.cycle([
 '-',
 '--',
 '-.',
 ':'])

def _create_timeseries_figure(ts_data_dct, labels_dct, template, show_title=False, set_y_origin_zero=True):
    """
    For a given dictionary of timeseries data (key 'data' should have
    sequence of 1+ sequences), creates and returns a Matplotlib
    Figure(Canvas) plotting the timeseries.  That Figure can then be
    written to different formats, e.g. PNG or PDF.

    This was the original function that did most of the work; it's
    since been refactored to do styling separately.
    """
    assert isinstance(ts_data_dct, dict), 'Unknown type for ts_data_dct: %s' % ts_data_dct
    tseries_data = ts_data_dct['data']
    assert all([ len(this_ts) > 0 for this_ts in tseries_data ])
    tseries_names = ts_data_dct.get('names')
    if 'colors' in ts_data_dct:
        colors = itertools.cycle(ts_data_dct['colors'])
    else:
        colors = colors_default
    if 'linestyles' in ts_data_dct:
        linestyles = itertools.cycle(ts_data_dct['linestyles'])
    else:
        linestyles = linestyles_default
    the_figure = Figure()
    ax = the_figure.add_subplot(1, 1, 1)
    ts_lines = []
    for ts in tseries_data:
        (this_ts_line,) = ax.plot(ts, linestyle=linestyles.next(), color=colors.next(), linewidth=1)
        ts_lines.append(this_ts_line)

    if tseries_names:
        ax.legend(ts_lines, tseries_names, 'upper right', frameon=False)
    if 'title' in labels_dct and show_title:
        the_figure.suptitle(labels_dct['title'])
    if 'x' in labels_dct:
        ax.set_xlabel(labels_dct['x'])
    else:
        ax.set_xlabel('Time')
    if 'y' in labels_dct:
        ax.set_ylabel(labels_dct['y'])
    else:
        ax.set_ylabel('Data')
    _stylize_figure(the_figure)
    return FigureCanvas(the_figure)


def _create_barchart_figure(data_dct, labels_dct, template, show_title=False, set_y_origin_zero=True, x_zero_indexed=False):
    """
    Given 1+ sequences, create and return a Matplotlib Figure(Canvas)
    barchart visualization.

    This function parallels _create_timeseries_figure and was derived
    from it.  While it may be possible to merge them into a single
    more general function, for now there are enough differences to
    keep them separate.
    """
    assert isinstance(data_dct, dict), 'Unknown type for data_dct: %s' % data_dct
    series_data = data_dct['data']
    assert all([ len(this_data) > 0 for this_data in series_data ])
    if 'colors' in data_dct:
        colors = itertools.cycle(data_dct['colors'])
    else:
        colors = colors_default
    the_figure = Figure()
    ax = the_figure.add_subplot(1, 1, 1)
    plotted_data = []
    bar_width = 0.7
    for series in series_data:
        x_indices = np.arange(1, len(series) + 1)
        if x_zero_indexed:
            x_indices = np.arange(len(series))
        this_series = ax.bar(x_indices, series, bar_width, color=colors.next(), edgecolor='#AAAAAA')
        plotted_data.append(this_series)

    ax.set_xticks(x_indices + bar_width / 2)
    ax.set_xticklabels(x_indices)
    if 'x' in labels_dct:
        ax.set_xlabel(labels_dct['x'])
    else:
        ax.set_xlabel('')
    if 'y' in labels_dct:
        ax.set_ylabel(labels_dct['y'])
    else:
        ax.set_ylabel('Data')
    _stylize_figure(the_figure)
    return FigureCanvas(the_figure)


def _stylize_figure(the_figure, style_template=None):
    """
    A mutator that updates the appearance of the given Figure
    instance, per style_template.  There is no return value.

    This code was originally part of _create_timeseries_figure, but is
    much better being separate.
    """
    bgcolor = '#FFFFFF'
    border_color = '#CCCCCC'
    axis_label_color = '#555555'
    axis_ticks_color = '#555555'
    the_figure.patch.set_color(bgcolor)
    for ax in the_figure.get_axes():
        for child in ax.get_children():
            if isinstance(child, matplotlib.spines.Spine):
                child.set_color(border_color)

        ax.xaxis.get_label().set_color(axis_label_color)
        for label in ax.xaxis.get_ticklabels():
            label.set_color(axis_ticks_color)

        ax.yaxis.get_label().set_color(axis_label_color)
        for label in ax.yaxis.get_ticklabels():
            label.set_color(axis_ticks_color)


def create_chart_as_png_str(chart_type, data_dct, labels_dct=None, template=None):
    """
    This is the public-facing API call to create and return a chart as
    a PNG-format string.
    """
    assert chart_type in ('timeseries', 'barchart')
    assert isinstance(data_dct, dict) and 'data' in data_dct
    assert len(data_dct['data'][0]) > 0
    if labels_dct:
        assert isinstance(labels_dct, dict)
        assert 'title' in labels_dct
    if chart_type == 'timeseries':
        figure_fn = _create_timeseries_figure
    elif chart_type == 'barchart':
        figure_fn = _create_barchart_figure
    else:
        raise Exception('Unknown chart_type %s' % chart_type)
    figure = figure_fn(data_dct, labels_dct, template)
    img_data_str = StringIO()
    figure.print_png(img_data_str)
    img_data_str.seek(0)
    return img_data_str.read()