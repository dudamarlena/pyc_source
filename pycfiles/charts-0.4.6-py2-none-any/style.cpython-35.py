# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Remote\chartpy\chartpy\style.py
# Compiled at: 2018-03-19 11:06:59
# Size of source mod 2**32: 25150 bytes
from __future__ import division
__author__ = 'saeedamen'
import datetime
from chartpy.chartconstants import ChartConstants

class Style(object):
    cc = ChartConstants()

    def __init__(self, title='', x_title='', y_title='', units='', engine=None, chart_type=None, color=[], color_2=[], color_2_series=[], exclude_from_color=[], normalize_colormap=True, bubble_series=None, bubble_size_scalar=cc.chartfactory_bubble_size_scalar, candlestick_series=None, candlestick_increasing_color=None, candlestick_increasing_line_color=None, candlestick_decreasing_color=None, candlestick_decreasing_line_color=None, subplots=False, share_subplot_x=False, scale_factor=cc.chartfactory_scale_factor, dpi=cc.chartfactory_dpi, width=cc.chartfactory_width, height=cc.chartfactory_height, resample=None, thin_margin=False, block_new_plots=False, animate_figure=False, animate_titles=None, animate_frame_ms=250, y_axis_2_series=[], linewidth_2_series=[], linewidth=None, linewidth_2=None, marker_size=1, line_of_best_fit=False, line_shape=None, x_axis_showgrid=True, y_axis_showgrid=True, y_axis_2_showgrid=True, x_y_line=[], x_axis_range=None, y_axis_range=None, connect_line_gaps=False, brand_label=cc.chartfactory_brand_label, display_brand_label=cc.chartfactory_display_brand_label, source=cc.chartfactory_source, source_color='black', display_source_label=cc.chartfactory_display_source_label, display_legend=True, xkcd=False, silent_display=False, file_output=None, date_formatter=None, html_file_output=None, display_mpld3=False, auto_generate_filename=False, auto_generate_html_filename=False, save_fig=True, plotly_url=None, plotly_as_image=False, plotly_username=cc.plotly_default_username, plotly_api_key=None, plotly_world_readable=cc.plotly_world_readable, plotly_sharing=cc.plotly_sharing, plotly_theme=None, plotly_plot_mode=cc.plotly_plot_mode, plotly_webgl=cc.plotly_webgl, bokeh_plot_mode=cc.bokeh_plot_mode, style_sheet=cc.chartfactory_default_stylesheet, convert_matplotlib_to_plotly=False):
        self.engine = engine
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.units = units
        self.chart_type = chart_type
        self.color = color
        self.color_2 = color_2
        self.color_2_series = color_2_series
        self.exclude_from_color = exclude_from_color
        self.normalize_colormap = normalize_colormap
        self.bubble_series = bubble_series
        self.bubble_size_scalar = bubble_size_scalar
        self.candlestick_series = candlestick_series
        self.candlestick_increasing_color = candlestick_increasing_color
        self.candlestick_increasing_line_color = candlestick_increasing_line_color
        self.candlestick_decreasing_color = candlestick_decreasing_color
        self.candlestick_decreasing_line_color = candlestick_decreasing_line_color
        self.subplots = subplots
        self.share_subplot_x = share_subplot_x
        self.scale_factor = scale_factor
        self.dpi = dpi
        self.width = width
        self.height = height
        self.resample = resample
        self.thin_margin = thin_margin
        self.block_new_plots = block_new_plots
        self.animate_figure = animate_figure
        self.animate_titles = animate_titles
        self.animate_frame_ms = animate_frame_ms
        self.y_axis_2_series = y_axis_2_series
        self.linewidth_2_series = linewidth_2_series
        self.linewidth = linewidth
        self.linewidth_2 = linewidth_2
        self.marker_size = marker_size
        self.line_of_best_fit = line_of_best_fit
        self.line_shape = line_shape
        self.x_axis_showgrid = x_axis_showgrid
        self.y_axis_showgrid = y_axis_showgrid
        self.y_axis_2_showgrid = y_axis_2_showgrid
        self.x_y_line = x_y_line
        self.x_axis_range = x_axis_range
        self.y_axis_range = y_axis_range
        self.connect_line_gaps = connect_line_gaps
        self.brand_label = brand_label
        self.display_brand_label = display_brand_label
        self.source = source
        self.source_color = source_color
        self.display_source_label = display_source_label
        self.display_legend = display_legend
        self.xkcd = xkcd
        self.silent_display = silent_display
        self.file_output = file_output
        self.save_fig = save_fig
        self.date_formatter = date_formatter
        self.html_file_output = html_file_output
        self.display_mpld3 = display_mpld3
        self.auto_generate_filename = auto_generate_filename
        self.auto_generate_html_filename = auto_generate_html_filename
        self.bokeh_plot_mode = bokeh_plot_mode
        if plotly_url is None:
            plotly_url = title + datetime.datetime.utcnow().strftime('%b-%d-%Y-%H-%M-%S')
        self.plotly_url = plotly_url
        self.plotly_as_image = plotly_as_image
        self.plotly_username = plotly_username
        self.plotly_webgl = plotly_webgl
        try:
            if plotly_api_key is None:
                plotly_api_key = ChartConstants().plotly_creds[plotly_username]
        except:
            pass

        self.plotly_api_key = plotly_api_key
        self.plotly_world_readable = plotly_world_readable
        self.plotly_sharing = plotly_sharing
        self.plotly_theme = plotly_theme
        self.plotly_plot_mode = plotly_plot_mode
        self.style_sheet = style_sheet
        self.convert_matplotlib_to_plotly = convert_matplotlib_to_plotly

    def str_list(self, original):
        try:
            original = original.tolist()
        except:
            pass

        if isinstance(original, list):
            original = [str(x) for x in original]
        return original

    @property
    def engine(self):
        return self._Style__engine

    @engine.setter
    def engine(self, engine):
        self._Style__engine = engine

    @property
    def title(self):
        return self._Style__title

    @title.setter
    def title(self, title):
        self._Style__title = title

    @property
    def x_title(self):
        return self._Style__x_title

    @x_title.setter
    def x_title(self, x_title):
        self._Style__x_title = x_title

    @property
    def y_title(self):
        return self._Style__y_title

    @y_title.setter
    def y_title(self, y_title):
        self._Style__y_title = y_title

    @property
    def units(self):
        return self._Style__units

    @units.setter
    def units(self, units):
        self._Style__units = units

    @property
    def chart_type(self):
        return self._Style__chart_type

    @chart_type.setter
    def chart_type(self, chart_type):
        self._Style__chart_type = chart_type

    @property
    def color(self):
        return self._Style__color

    @color.setter
    def color(self, color):
        self._Style__color = color

    @property
    def color_2(self):
        return self._Style__color_2

    @color_2.setter
    def color_2(self, color_2):
        self._Style__color_2 = color_2

    @property
    def color_2_series(self):
        return self._Style__color_2_series

    @color_2_series.setter
    def color_2_series(self, color_2_series):
        self._Style__color_2_series = self.str_list(color_2_series)

    @property
    def exclude_from_color(self):
        return self._Style__exclude_from_color

    @exclude_from_color.setter
    def exclude_from_color(self, exclude_from_color):
        self._Style__exclude_from_color = self.str_list(exclude_from_color)

    @property
    def normalize_colormap(self):
        return self._Style__normalize_colormap

    @normalize_colormap.setter
    def normalize_colormap(self, normalize_colormap):
        self._Style__normalize_colormap = self.str_list(normalize_colormap)

    @property
    def bubble_series(self):
        return self._Style__bubble_series

    @bubble_series.setter
    def bubble_series(self, bubble_series):
        self._Style__bubble_series = self.str_list(bubble_series)

    @property
    def bubble_size_scalar(self):
        return self._Style__bubble_size_scalar

    @bubble_size_scalar.setter
    def bubble_size_scalar(self, bubble_size_scalar):
        self._Style__bubble_size_scalar = bubble_size_scalar

    @property
    def candlestick_series(self):
        return self._Style__candlestick_series

    @candlestick_series.setter
    def candlestick_series(self, candlestick_series):
        self._Style__candlestick_series = self.str_list(candlestick_series)

    @property
    def candlestick_increasing_color(self):
        return self._Style__candlestick_increasing_color

    @candlestick_increasing_color.setter
    def candlestick_increasing_color(self, candlestick_increasing_color):
        self._Style__candlestick_increasing_color = candlestick_increasing_color

    @property
    def candlestick_increasing_line_color(self):
        return self._Style__candlestick_increasing_line_color

    @candlestick_increasing_line_color.setter
    def candlestick_increasing_line_color(self, candlestick_increasing_line_color):
        self._Style__candlestick_increasing_line_color = candlestick_increasing_line_color

    @property
    def candlestick_decreasing_color(self):
        return self._Style__candlestick_decreasing_color

    @candlestick_decreasing_color.setter
    def candlestick_decreasing_color(self, candlestick_decreasing_color):
        self._Style__candlestick_decreasing_color = candlestick_decreasing_color

    @property
    def candlestick_decreasing_line_color(self):
        return self._Style__candlestick_decreasing_line_color

    @candlestick_decreasing_line_color.setter
    def candlestick_decreasing_line_color(self, candlestick_decreasing_line_color):
        self._Style__candlestick_decreasing_line_color = candlestick_decreasing_line_color

    @property
    def subplots(self):
        return self._Style__subplots

    @subplots.setter
    def subplots(self, subplots):
        self._Style__subplots = subplots

    @property
    def share_subplot_x(self):
        return self._Style__share_subplot_x

    @share_subplot_x.setter
    def share_subplot_x(self, share_subplot_x):
        self._Style__share_subplot_x = share_subplot_x

    @property
    def scale_factor(self):
        return self._Style__scale_factor

    @scale_factor.setter
    def scale_factor(self, scale_factor):
        self._Style__scale_factor = scale_factor

    @property
    def dpi(self):
        return self._Style__dpi

    @dpi.setter
    def dpi(self, dpi):
        self._Style__dpi = dpi

    @property
    def width(self):
        return self._Style__width

    @width.setter
    def width(self, width):
        self._Style__width = width

    @property
    def height(self):
        return self._Style__height

    @height.setter
    def height(self, height):
        self._Style__height = height

    @property
    def thin_margin(self):
        return self._Style__thin_margin

    @thin_margin.setter
    def thin_margin(self, thin_margin):
        self._Style__thin_margin = thin_margin

    @property
    def block_new_plots(self):
        return self._Style__block_new_plots

    @block_new_plots.setter
    def block_new_plots(self, block_new_plots):
        self._Style__block_new_plots = block_new_plots

    @property
    def animate_figure(self):
        return self._Style__animate_figure

    @animate_figure.setter
    def animate_figure(self, animate_figure):
        self._Style__animate_figure = animate_figure

    @property
    def animate_titles(self):
        return self._Style__animate_titles

    @animate_titles.setter
    def animate_titles(self, animate_titles):
        self._Style__animate_titles = animate_titles

    @property
    def animate_frame_ms(self):
        return self._Style__animate_frame_ms

    @animate_frame_ms.setter
    def animate_frame_ms(self, animate_frame_ms):
        self._Style__animate_frame_ms = animate_frame_ms

    @property
    def resample(self):
        return self._Style__resample

    @resample.setter
    def resample(self, resample):
        self._Style__resample = resample

    @property
    def y_axis_2_series(self):
        return self._Style__y_axis_2_series

    @y_axis_2_series.setter
    def y_axis_2_series(self, y_axis_2_series):
        self._Style__y_axis_2_series = self.str_list(y_axis_2_series)

    @property
    def linewidth_2_series(self):
        return self._Style__linewidth_2_series

    @linewidth_2_series.setter
    def linewidth_2_series(self, linewidth_2_series):
        self._Style__linewidth_2_series = self.str_list(linewidth_2_series)

    @property
    def linewidth(self):
        return self._Style__linewidth

    @linewidth.setter
    def linewidth(self, linewidth):
        self._Style__linewidth = linewidth

    @property
    def linewidth_2(self):
        return self._Style__linewidth_2

    @linewidth_2.setter
    def linewidth_2(self, linewidth_2):
        self._Style__linewidth_2 = linewidth_2

    @property
    def marker_size(self):
        return self._Style__marker_size

    @marker_size.setter
    def marker_size(self, marker_size):
        self._Style__marker_size = marker_size

    @property
    def line_of_best_fit(self):
        return self._Style__line_of_best_fit

    @line_of_best_fit.setter
    def line_of_best_fit(self, line_of_best_fit):
        self._Style__line_of_best_fit = line_of_best_fit

    @property
    def line_shape(self):
        return self._Style__line_shape

    @line_shape.setter
    def line_shape(self, line_shape):
        self._Style__line_shape = line_shape

    @property
    def x_axis_showgrid(self):
        return self._Style__x_axis_showgrid

    @x_axis_showgrid.setter
    def x_axis_showgrid(self, x_axis_showgrid):
        self._Style__x_axis_showgrid = x_axis_showgrid

    @property
    def y_axis_showgrid(self):
        return self._Style__y_axis_showgrid

    @y_axis_showgrid.setter
    def y_axis_showgrid(self, y_axis_showgrid):
        self._Style__y_axis_showgrid = y_axis_showgrid

    @property
    def y_axis_2_showgrid(self):
        return self._Style__y_axis_2_showgrid

    @y_axis_2_showgrid.setter
    def y_axis_2_showgrid(self, y_axis_2_showgrid):
        self._Style__y_axis_2_showgrid = y_axis_2_showgrid

    @property
    def x_y_line(self):
        return self._Style__x_y_line

    @x_y_line.setter
    def x_y_line(self, x_y_line):
        self._Style__x_y_line = x_y_line

    @property
    def x_axis_range(self):
        return self._Style__x_axis_range

    @x_axis_range.setter
    def x_axis_range(self, x_axis_range):
        self._Style__x_axis_range = x_axis_range

    @property
    def y_axis_range(self):
        return self._Style__y_axis_range

    @y_axis_range.setter
    def y_axis_range(self, y_axis_range):
        self._Style__y_axis_range = y_axis_range

    @property
    def connect_line_gaps(self):
        return self._Style__connect_line_gaps

    @connect_line_gaps.setter
    def connect_line_gaps(self, connect_line_gaps):
        self._Style__connect_line_gaps = connect_line_gaps

    @property
    def brand_label(self):
        return self._Style__brand_label

    @brand_label.setter
    def brand_label(self, brand_label):
        self._Style__brand_label = brand_label

    @property
    def display_brand_label(self):
        return self._Style__display_brand_label

    @display_brand_label.setter
    def display_brand_label(self, display_brand_label):
        self._Style__display_brand_label = display_brand_label

    @property
    def source(self):
        return self._Style__source

    @source.setter
    def source(self, source):
        self._Style__source = source

    @property
    def source(self):
        return self._Style__source_color

    @source.setter
    def source(self, source_color):
        self._Style__source_color = source_color

    @property
    def display_source_label(self):
        return self._Style__display_source_label

    @display_source_label.setter
    def display_source_label(self, display_source_label):
        self._Style__display_source_label = display_source_label

    @property
    def display_legend(self):
        return self._Style__display_legend

    @display_legend.setter
    def display_legend(self, display_legend):
        self._Style__display_legend = display_legend

    @property
    def xkcd(self):
        return self._Style__xkcd

    @xkcd.setter
    def xkcd(self, xkcd):
        self._Style__xkcd = xkcd

    @property
    def silent_display(self):
        return self._Style__silent_display

    @silent_display.setter
    def silent_display(self, silent_display):
        self._Style__silent_display = silent_display

    @property
    def file_output(self):
        return self._Style__file_output

    @file_output.setter
    def file_output(self, file_output):
        self._Style__file_output = file_output

    @property
    def save_fig(self):
        return self._Style__save_fig

    @save_fig.setter
    def save_fig(self, save_fig):
        self._Style__save_fig = save_fig

    @property
    def date_formatter(self):
        return self._Style__date_formatter

    @date_formatter.setter
    def date_formatter(self, date_formatter):
        self._Style__date_formatter = date_formatter

    @property
    def html_file_output(self):
        return self._Style__html_file_output

    @html_file_output.setter
    def html_file_output(self, html_file_output):
        self._Style__html_file_output = html_file_output

    @property
    def display_mpld3(self):
        return self._Style__display_mpld3

    @display_mpld3.setter
    def display_mpld3(self, display_mpld3):
        self._Style__display_mpld3 = display_mpld3

    @property
    def auto_generate_filename(self):
        return self._Style__auto_generate_filename

    @auto_generate_filename.setter
    def auto_generate_filename(self, auto_generate_filename):
        self._Style__auto_generate_filename = auto_generate_filename

    @property
    def auto_generate_html_filename(self):
        return self._Style__auto_generate_html_filename

    @auto_generate_html_filename.setter
    def auto_generate_html_filename(self, auto_generate_html_filename):
        self._Style__auto_generate_html_filename = auto_generate_html_filename

    @property
    def plotly_url(self):
        return self._Style__plotly_url

    @plotly_url.setter
    def plotly_url(self, plotly_url):
        self._Style__plotly_url = plotly_url

    @property
    def plotly_as_image(self):
        return self._Style__plotly_as_image

    @plotly_as_image.setter
    def plotly_as_image(self, plotly_as_image):
        self._Style__plotly_as_image = plotly_as_image

    @property
    def plotly_username(self):
        return self._Style__plotly_username

    @plotly_username.setter
    def plotly_username(self, plotly_username):
        self._Style__plotly_username = plotly_username
        try:
            self.plotly_api_key = ChartConstants().plotly_creds[plotly_username]
        except:
            pass

    @property
    def plotly_api_key(self):
        return self._Style__plotly_api_key

    @plotly_api_key.setter
    def plotly_api_key(self, plotly_api_key):
        self._Style__plotly_api_key = plotly_api_key

    @property
    def plotly_world_readable(self):
        return self._Style__plotly_world_readable

    @plotly_world_readable.setter
    def plotly_world_readable(self, plotly_world_readable):
        self._Style__plotly_world_readable = plotly_world_readable

    @property
    def plotly_sharing(self):
        return self._Style__plotly_sharing

    @plotly_sharing.setter
    def plotly_sharing(self, plotly_sharing):
        self._Style__plotly_sharing = plotly_sharing

    @property
    def plotly_theme(self):
        return self._Style__plotly_theme

    @plotly_theme.setter
    def plotly_theme(self, plotly_theme):
        self._Style__plotly_theme = plotly_theme

    @property
    def plotly_plot_mode(self):
        return self._Style__plotly_plot_mode

    @plotly_plot_mode.setter
    def plotly_plot_mode(self, plotly_plot_mode):
        self._Style__plotly_plot_mode = plotly_plot_mode

    @property
    def plotly_webgl(self):
        return self._Style__plotly_webgl

    @plotly_webgl.setter
    def plotly_webgl(self, plotly_webgl):
        self._Style__plotly_webgl = plotly_webgl

    @property
    def bokeh_plot_mode(self):
        return self._Style__bokeh_plot_mode

    @bokeh_plot_mode.setter
    def bokeh_plot_mode(self, bokeh_plot_mode):
        self._Style__bokeh_plot_mode = bokeh_plot_mode

    @property
    def style_sheet(self):
        return self._Style__style_sheet

    @style_sheet.setter
    def style_sheet(self, style_sheet):
        self._Style__style_sheet = style_sheet

    @property
    def convert_matplotlib_to_plotly(self):
        return self._Style__convert_matplotlib_to_plotly

    @convert_matplotlib_to_plotly.setter
    def convert_matplotlib_to_plotly(self, convert_matplotlib_to_plotly):
        self._Style__convert_matplotlib_to_plotly = convert_matplotlib_to_plotly