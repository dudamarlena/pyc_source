# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/redhat/cuemacro/chartpy/chartpy/engine.py
# Compiled at: 2019-08-19 09:34:02
__author__ = 'saeedamen'
import abc
from math import log10, floor
import numpy, pandas, datetime
from chartpy.style import Style
from chartpy.chartconstants import ChartConstants
cc = ChartConstants()
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

class EngineTemplate(ABC):

    def init(self):
        pass

    @abc.abstractmethod
    def plot_chart(self, data_frame, style, type):
        pass

    def get_time_stamp(self):
        return str(datetime.datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')

    def get_bar_indices(self, data_frame, style, chart_type, bar_ind):
        has_bar = 'no-bar'
        xd = data_frame.index
        no_of_bars = len(data_frame.columns)
        if style.chart_type is not None:
            if isinstance(style.chart_type, list):
                if 'bar' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = style.chart_type.count('bar')
                    has_bar = 'barv'
                elif 'stacked' in style.chart_type:
                    xd = bar_ind
                    no_of_bars = 1
                    has_bar = 'barv'
            elif 'bar' == style.chart_type:
                xd = bar_ind
                has_bar = 'barv'
            elif 'barh' == style.chart_type:
                xd = bar_ind
                has_bar = 'barh'
            elif 'stacked' == style.chart_type:
                xd = bar_ind
                has_bar = 'barh'
        elif chart_type == 'bar' or chart_type == 'stacked':
            xd = bar_ind
            has_bar = 'barv'
        return (xd, bar_ind, has_bar, no_of_bars)

    def assign(self, structure, field, default):
        if hasattr(structure, field):
            default = getattr(structure, field)
        return default

    def assign_list(self, style, field, list):
        if hasattr(style, field):
            list = [ str(x) for x in getattr(style, field) ]
        return list

    def get_linewidth(self, label, linewidth_1, linewidth_2, linewidth_2_series):
        if label in linewidth_2_series:
            return linewidth_2
        return linewidth_1

    def round_to_1(self, x):
        return round(x, -int(floor(log10(x))))

    def split_data_frame_to_list(self, data_frame, style):
        data_frame_list = []
        if isinstance(data_frame, list):
            data_frame_list = data_frame
        elif style.subplots == True:
            for col in data_frame.columns:
                data_frame_list.append(pandas.DataFrame(index=data_frame.index, columns=[col], data=data_frame[col]))

        else:
            data_frame_list.append(data_frame)
        return data_frame_list

    def generate_file_names(self, style, engine):
        if style.html_file_output is not None and not style.auto_generate_html_filename:
            pass
        else:
            import time
            style.html_file_output = self.get_time_stamp() + '-' + engine + '.html'
            style.auto_generate_html_filename = True
        if style.file_output is not None and not style.auto_generate_filename:
            pass
        else:
            import time
            style.file_output = self.get_time_stamp() + '-' + engine + '.png'
            style.auto_generate_filename = True
        return style

    def get_max_min_dataframes(self, data_frame_list):
        """Gets minimum and maximum values for a series of dataframes. Can be particularly useful for adjusting colormaps
        for lightness/darkness.

        Parameters
        ----------
        data_frame_list : DataFrame (list)
            DataFrames to be checked

        Returns
        -------
        float, float
            Minimum and maximum values
        """
        if not isinstance(data_frame_list, list):
            data_frame_list = [
             data_frame_list]
        import sys
        minz = sys.float_info.max
        maxz = sys.float_info.min
        for data_frame in data_frame_list:
            minz_1 = data_frame.min(axis=0).min()
            maxz_1 = data_frame.max(axis=0).max()
            if minz_1 != numpy.nan:
                minz = min(minz, minz_1)
            if maxz_1 != numpy.nan:
                maxz = max(maxz, maxz_1)

        return (
         minz, maxz)

    def get_max_min_x_axis(self, data_frame_list):
        """Gets minimum and maximum values for the x_axis. Can be particularly useful for adjusting colormaps
        for lightness/darkness.

        Parameters
        ----------
        data_frame_list : DataFrame (list)
            DataFrames to be checked

        Returns
        -------
        obj, obj
            Minimum and maximum values
        """
        import sys
        minz = data_frame_list[0].index[0]
        maxz = data_frame_list[0].index[(-1)]
        for data_frame in data_frame_list:
            minz_1 = data_frame.index[0]
            maxz_1 = data_frame.index[(-1)]
            if minz_1 != numpy.nan:
                minz = min(minz, minz_1)
            if maxz_1 != numpy.nan:
                maxz = max(maxz, maxz_1)

        return (
         minz, maxz)


try:
    from bokeh.plotting import figure, output_file, show, gridplot, save
    from bokeh.models import Range1d
    from bokeh.charts import HeatMap
except:
    pass

class EngineBokeh(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):
        cm = ColorMaster()
        if style.scale_factor > 0:
            scale_factor = abs(style.scale_factor) * 2 / 3
        else:
            scale_factor = abs(style.scale_factor)
        try:
            if style.bokeh_plot_mode == 'offline_jupyter':
                from bokeh.io import output_notebook
                output_notebook()
        except:
            pass

        try:
            style = self.generate_file_names(style, 'bokeh')
            output_file(style.html_file_output)
        except:
            pass

        data_frame_list = self.split_data_frame_to_list(data_frame, style)
        plot_list = []
        plot_width = int(style.width * scale_factor)
        plot_height = int(style.height * scale_factor / len(data_frame_list))
        for data_frame in data_frame_list:
            bar_ind = numpy.arange(1, len(data_frame.index) + 1)
            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)
            separate_chart = False
            if chart_type == 'heatmap':
                p1 = HeatMap(data_frame, title='Random', plot_width=plot_width, plot_height=plot_height)
                separate_chart = True
            elif has_bar == 'barv':
                p1 = figure(plot_width=plot_width, plot_height=plot_height, x_range=[ str(x).replace(':', '.') for x in data_frame.index ])
                from math import pi
                p1.xaxis.major_label_orientation = pi / 2
            elif type(data_frame.index) == pandas.Timestamp or type(xd[0]) == pandas.Timestamp and type(xd[(-1)]) == pandas.Timestamp or type(data_frame.index) == pandas.DatetimeIndex:
                p1 = figure(x_axis_type='datetime', plot_width=plot_width, plot_height=plot_height)
            else:
                p1 = figure(plot_width=plot_width, plot_height=plot_height, x_range=(
                 xd[0], xd[(-1)]))
            p1.axis.major_label_text_font_size = str(10) + 'pt'
            p1.axis.major_label_text_font = cc.bokeh_font
            p1.axis.major_label_text_font_style = cc.bokeh_font_style
            p1.xaxis.axis_label_text_font_size = str(10) + 'pt'
            p1.xaxis.axis_label_text_font = cc.bokeh_font
            p1.xaxis.axis_label_text_font_style = cc.bokeh_font_style
            p1.xaxis.axis_label = style.x_title
            p1.xaxis.visible = style.x_axis_showgrid
            p1.yaxis.axis_label_text_font_size = str(10) + 'pt'
            p1.yaxis.axis_label_text_font = cc.bokeh_font
            p1.yaxis.axis_label_text_font_style = cc.bokeh_font_style
            p1.yaxis.axis_label = style.y_title
            p1.yaxis.visible = style.y_axis_showgrid
            p1.legend.location = 'top_left'
            p1.legend.label_text_font_size = str(10) + 'pt'
            p1.legend.label_text_font = cc.bokeh_font
            p1.legend.label_text_font_style = cc.bokeh_font_style
            p1.legend.background_fill_alpha = 0.75
            p1.legend.border_line_width = 0
            p1.outline_line_width = 0
            p1.title.text_font_size = str(14) + 'pt'
            p1.title.text_font = cc.bokeh_font
            color_spec = cm.create_color_list(style, data_frame)
            import matplotlib
            bar_space = 0.2
            bar_width = (1 - bar_space) / no_of_bars
            bar_index = 0
            has_bar = 'no-bar'
            if not separate_chart:
                for i in range(0, len(data_frame.columns)):
                    label = str(data_frame.columns[i])
                    glyph_name = 'glpyh' + str(i)
                    if isinstance(chart_type, list):
                        chart_type_ord = chart_type[i]
                    else:
                        chart_type_ord = chart_type
                    if color_spec[i] is None:
                        color_spec[i] = self.get_color_list(i)
                    try:
                        color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                    except:
                        pass

                    yd = data_frame.iloc[:, i]
                    if chart_type_ord == 'line':
                        linewidth_t = self.get_linewidth(label, style.linewidth, style.linewidth_2, style.linewidth_2_series)
                        if linewidth_t is None:
                            linewidth_t = 1
                        if style.display_legend:
                            p1.line(xd, yd, color=color_spec[i], line_width=linewidth_t, name=glyph_name, legend=label)
                        else:
                            p1.line(xd, data_frame.iloc[:, i], color=color_spec[i], line_width=linewidth_t, name=glyph_name)
                    elif chart_type_ord == 'bar':
                        bar_pos = [ k - (1 - bar_space) / 2.0 + bar_index * bar_width for k in range(1, len(bar_ind) + 1) ]
                        bar_pos_right = [ x + bar_width for x in bar_pos ]
                        if style.display_legend:
                            p1.quad(top=yd, bottom=0 * yd, left=bar_pos, right=bar_pos_right, color=color_spec[i], legend=label)
                        else:
                            p1.quad(top=yd, bottom=0 * yd, left=bar_pos, right=bar_pos_right, color=color_spec[i])
                        bar_index = bar_index + 1
                        bar_ind = bar_ind + bar_width
                    elif chart_type_ord == 'barh':
                        pass
                    elif chart_type_ord == 'scatter':
                        linewidth_t = self.get_linewidth(label, style.linewidth, style.linewidth_2, style.linewidth_2_series)
                        if linewidth_t is None:
                            linewidth_t = 1
                        if style.display_legend:
                            p1.circle(xd, yd, color=color_spec[i], line_width=linewidth_t, name=glyph_name, legend=label)
                        else:
                            p1.circle(xd, yd, color=color_spec[i], line_width=linewidth_t, name=glyph_name)

                p1.grid.grid_line_alpha = 0.3
                p1.min_border = -50
            plot_list.append(p1)

        p_final = gridplot(plot_list, ncols=1)
        try:
            p_final.title.text = style.title
        except:
            pass

        if style.silent_display:
            save(p_final)
        else:
            show(p_final)
        return

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette
        return color_palette[(i % len(color_palette))]

    def generic_settings(self):
        pass


try:
    from IPython.display import display
    from bqplot import OrdinalScale, LinearScale, Bars, Lines, Axis, Figure
except:
    pass

class EngineBqplot(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):
        pass

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette
        return color_palette[(i % len(color_palette))]

    def generic_settings(self):
        pass


try:
    from vispy import plot as vp
except:
    pass

class EngineVisPy(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):
        cm = ColorMaster()
        scale_factor = abs(style.scale_factor)
        try:
            if style.vispy_plot_mode == 'offline_jupyter':
                pass
        except:
            pass

        try:
            style = self.generate_file_names(style, 'vispy')
        except:
            pass

        data_frame_list = self.split_data_frame_to_list(data_frame, style)
        plot_list = []
        plot_width = int(style.width * scale_factor)
        plot_height = int(style.height * scale_factor / len(data_frame_list))
        fig = vp.Fig(size=(plot_width, plot_height), show=False, title=style.title)
        min_x, max_x = self.get_max_min_x_axis(data_frame_list=data_frame_list)
        for data_frame in data_frame_list:
            bar_ind = numpy.arange(1, len(data_frame.index) + 1)
            if data_frame.index.name == 'Date':
                data_frame = data_frame.copy()
                data_frame = data_frame.reset_index()
                data_frame = data_frame.drop(['Date'], axis=1)
            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)
            xd = data_frame.index
            separate_chart = False
            color_spec = cm.create_color_list(style, data_frame)
            import matplotlib
            bar_space = 0.2
            bar_width = (1 - bar_space) / no_of_bars
            bar_index = 0
            separate_chart = False
            if chart_type == 'surface':
                separate_chart = True
            has_bar = 'no-bar'
            if not separate_chart:
                for i in range(0, len(data_frame.columns)):
                    label = str(data_frame.columns[i])
                    glyph_name = 'glpyh' + str(i)
                    if isinstance(chart_type, list):
                        chart_type_ord = chart_type[i]
                    else:
                        chart_type_ord = chart_type
                    if color_spec[i] is None:
                        color_spec[i] = self.get_color_list(i)
                    try:
                        color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                    except:
                        pass

                    yd = data_frame.iloc[:, i]
                    if chart_type_ord == 'line':
                        fig[(0, 0)].plot(np.array((xd, yd)).T, marker_size=0, color=color_spec[i])
                    elif chart_type_ord == 'bar':
                        pass
                    elif chart_type_ord == 'barh':
                        pass
                    elif chart_type_ord == 'scatter':
                        continue

        if style.silent_display:
            pass
        else:
            if style.save_fig:
                import vispy.io as io
                io.write_png(style.file_output, fig.render())
            fig.show(run=True)
        return

    def get_color_list(self, i):
        color_palette = cc.bokeh_palette
        return color_palette[(i % len(color_palette))]

    def generic_settings(self):
        pass


from datetime import timedelta
import numpy as np
try:
    import matplotlib, matplotlib.pyplot as plt
except:
    pass

try:
    from mpl_toolkits.mplot3d import Axes3D
except:
    pass

try:
    from matplotlib.dates import YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator
    from matplotlib.ticker import MultipleLocator
except:
    pass

class EngineMatplotlib(EngineTemplate):

    def plot_chart(self, data_frame, style, chart_type):
        self.apply_style_sheet(style)
        if style.xkcd:
            plt.xkcd()
        fig = plt.figure(figsize=(style.width * abs(style.scale_factor) / style.dpi,
         style.height * abs(style.scale_factor) / style.dpi), dpi=style.dpi)
        try:
            cyc = matplotlib.rcParams['axes.prop_cycle']
            color_cycle = [ x['color'] for x in cyc ]
        except KeyError:
            pass

        cm = ColorMaster()
        data_frame_list = self.split_data_frame_to_list(data_frame, style)
        subplot_no = 1
        first_ax = None
        movie_frame = []
        ordinal = 0
        minz, maxz = self.get_max_min_dataframes(data_frame_list=data_frame_list)
        for data_frame in data_frame_list:
            bar_ind = np.arange(0, len(data_frame.index))
            xd, bar_ind, has_bar, no_of_bars = self.get_bar_indices(data_frame, style, chart_type, bar_ind)
            try:
                xd = xd.to_pydatetime()
            except:
                pass

            ax, ax2, subplot_no, ordinal = self._create_subplot(fig, chart_type, style, subplot_no, first_ax, ordinal)
            yoff_pos = np.zeros(len(data_frame.index.values))
            yoff_neg = np.zeros(len(data_frame.index.values))
            zeros = np.zeros(len(data_frame.index.values))
            bar_space = 0.2
            bar_width = (1 - bar_space) / no_of_bars
            bar_index = 0
            try:
                has_matrix = 'no'
                if not isinstance(chart_type, list):
                    ax_temp = ax
                    color = style.color
                    if style.color == []:
                        color = cc.chartfactory_default_colormap
                    elif isinstance(style.color, list):
                        color = style.color[(subplot_no - 1)]
                    if chart_type == 'heatmap':
                        ax_temp.set_frame_on(False)
                        data_frame = data_frame.iloc[::-1]
                        if style.normalize_colormap:
                            movie_frame.append(ax_temp.pcolor(data_frame.values, cmap=color, alpha=0.8, vmax=maxz, vmin=minz))
                        else:
                            movie_frame.append(ax_temp.pcolor(data_frame.values, cmap=color, alpha=0.8))
                        has_matrix = '2d-matrix'
                    elif chart_type == 'surface':
                        X, Y = np.meshgrid(range(0, len(data_frame.columns)), range(0, len(data_frame.index)))
                        Z = data_frame.values
                        if style.normalize_colormap:
                            movie_frame.append(ax_temp.plot_surface(X, Y, Z, cmap=color, rstride=1, cstride=1, vmax=maxz, vmin=minz))
                        else:
                            movie_frame.append(ax_temp.plot_surface(X, Y, Z, cmap=color, rstride=1, cstride=1))
                        has_matrix = '3d-matrix'
                if has_matrix == 'no':
                    color_spec = cm.create_color_list(style, data_frame)
                    for i in range(0, len(data_frame.columns.values)):
                        if isinstance(chart_type, list):
                            chart_type_ord = chart_type[i]
                        else:
                            chart_type_ord = chart_type
                        label = str(data_frame.columns[i])
                        ax_temp = self.get_axis(ax, ax2, label, style.y_axis_2_series)
                        yd = data_frame.iloc[:, i]
                        if color_spec[i] is None:
                            color_spec[i] = color_cycle[(i % len(color_cycle))]
                        if chart_type_ord == 'line':
                            linewidth_t = self.get_linewidth(label, style.linewidth, style.linewidth_2, style.linewidth_2_series)
                            if linewidth_t is None:
                                linewidth_t = matplotlib.rcParams['axes.linewidth']
                            movie_frame.append(ax_temp.plot(xd, yd, label=label, color=color_spec[i], linewidth=linewidth_t))
                        elif chart_type_ord == 'bar':
                            bar_pos = [ k - (1 - bar_space) / 2.0 + bar_index * bar_width for k in range(0, len(bar_ind)) ]
                            movie_frame.append(ax_temp.bar(bar_pos, yd, bar_width, label=label, color=color_spec[i]))
                            bar_index = bar_index + 1
                        elif chart_type_ord == 'barh':
                            bar_pos = [ k - (1 - bar_space) / 2.0 + bar_index * bar_width for k in range(0, len(bar_ind)) ]
                            movie_frame.append(ax_temp.barh(bar_pos, yd, bar_width, label=label, color=color_spec[i]))
                            bar_index = bar_index + 1
                        elif chart_type_ord == 'stacked':
                            bar_pos = [ k - (1 - bar_space) / 2.0 + bar_index * bar_width for k in range(0, len(bar_ind)) ]
                            yoff = np.where(yd > 0, yoff_pos, yoff_neg)
                            movie_frame.append(ax_temp.bar(bar_pos, yd, label=label, color=color_spec[i], bottom=yoff))
                            yoff_pos = yoff_pos + np.maximum(yd, zeros)
                            yoff_neg = yoff_neg + np.minimum(yd, zeros)
                        elif chart_type_ord == 'scatter':
                            movie_frame.append(ax_temp.scatter(xd, yd, label=label, color=color_spec[i]))
                            if style.line_of_best_fit is True:
                                self.trendline(ax_temp, xd.values, yd.values, order=1, color=color_spec[i], alpha=1, scale_factor=abs(style.scale_factor))

                self.format_x_axis(ax_temp, data_frame, style, has_bar, bar_ind, bar_width, has_matrix)
            except Exception as e:
                pass

            self._create_legend(ax, ax2, style)

        try:
            ax_temp.set_zlim(minz, maxz)
        except:
            pass

        anim = None
        if style.animate_figure:
            if style.animate_titles is None:
                titles = range(1, len(data_frame_list) + 1)
            else:
                titles = style.animate_titles

            def init():
                return [
                 movie_frame[(-1)]]

            def update(i):
                fig.canvas.set_window_title(str(titles[i]))
                return [
                 movie_frame[i]]

            import matplotlib.animation as animation
            try:
                anim = animation.FuncAnimation(plt.gcf(), update, interval=style.animate_frame_ms, blit=True, frames=len(data_frame_list), init_func=init, repeat=True)
            except Exception as e:
                print str(e)

        try:
            style = self.generate_file_names(style, 'matplotlib')
            if style.save_fig:
                if style.animate_figure:
                    file = style.file_output.upper()
                plt.savefig(style.file_output, transparent=False)
        except Exception as e:
            print str(e)

        try:
            import mpld3
            if style.display_mpld3 == True:
                mpld3.save_d3_html(fig, style.html_file_output)
                mpld3.show(fig)
        except:
            pass

        try:
            if style.convert_matplotlib_to_bokeh == True:
                from bokeh.plotting import output_file, show
                from bokeh import mpl
                output_file(style.html_file_output)
                show(mpl.to_bokeh())
        except:
            pass

        try:
            import plotly.plotly as py, plotly, plotly.tools as tls
            if style.convert_matplotlib_to_plotly == True:
                plotly.tools.set_credentials_file(username=style.plotly_username, api_key=style.plotly_api_key)
                py_fig = tls.mpl_to_plotly(fig, strip_style=True)
                plot_url = py.plot_mpl(py_fig, filename=style.plotly_url)
        except:
            pass

        try:
            if cc.chartfactory_silent_display == True:
                plt.close(fig)
                return fig
            if style.silent_display == False:
                if not style.block_new_plots:
                    pass
                plt.show()
            else:
                plt.close(fig)
                return fig
        except:
            pass

        return

    def apply_style_sheet(self, style):
        matplotlib.rcdefaults()
        try:
            plt.style.use(cc.chartfactory_style_sheet[style.style_sheet])
        except:
            plt.style.use(style.style_sheet)

        matplotlib.rcParams.update({'font.size': matplotlib.rcParams['font.size'] * abs(style.scale_factor)})
        matplotlib.rcParams.update({'axes.formatter.useoffset': False})

    def format_x_axis(self, ax, data_frame, style, has_bar, bar_ind, bar_width, has_matrix):
        if has_matrix == '2d-matrix' or has_matrix == '3d-matrix':
            x_bar_ind = np.arange(0, len(data_frame.columns))
            y_bar_ind = np.arange(0, len(data_frame.index))
            offset = 0.5
            ax.set_xticks(x_bar_ind + offset)
            ax.set_xlim([0, len(x_bar_ind)])
            ax.set_yticks(y_bar_ind + offset)
            ax.set_ylim([0, len(y_bar_ind)])
            plt.setp(plt.yticks()[1], rotation=90)
            ax.set_xticklabels(data_frame.columns, minor=False)
            ax.set_yticklabels(data_frame.index, minor=False)
            ax.plot([], [])
            for x in range(len(data_frame.index)):
                for y in range(len(data_frame.columns)):
                    plt.text(x + offset, y + offset, '%.0f' % data_frame.iloc[(x, y)], horizontalalignment='center', verticalalignment='center')

            return
        if has_bar == 'barv':
            if matplotlib.__version__ > '1.9':
                offset = bar_width / 2.0
            else:
                offset = 0
            ax.set_xticks(bar_ind - offset)
            ax.set_xticklabels(data_frame.index)
            ax.set_xlim([-1, len(bar_ind)])
            if len(bar_ind) > 6:
                plt.setp(plt.xticks()[1], rotation=90)
                import matplotlib.dates as mdates
                if style.date_formatter is not None:
                    myFmt = mdates.DateFormatter(style.date_formatter)
                plt.tight_layout()
            return
        if has_bar == 'barh':
            ax.set_yticks(bar_ind)
            ax.set_yticklabels(data_frame.index)
            ax.set_ylim([-1, len(bar_ind)])
            if len(bar_ind) > 6:
                import matplotlib.dates as mdates
                if style.date_formatter is not None:
                    ax.format_ydata = mdates.DateFormatter(style.date_formatter)
                plt.tight_layout()
            return
        dates = data_frame.index
        if hasattr(data_frame.index[0], 'hour') and not hasattr(data_frame.index[0], 'month'):
            ax.xaxis.set_major_locator(MultipleLocator(86400.0 / 3.0))
            ax.xaxis.set_minor_locator(MultipleLocator(86400.0 / 24.0))
            ax.grid(b=style.x_axis_showgrid, which='minor', color='w', linewidth=0.5)
        else:
            try:
                dates = dates.to_pydatetime()
                diff = data_frame.index[(-1)] - data_frame.index[0]
                import matplotlib.dates as md
                if style.date_formatter is not None:
                    ax.xaxis.set_major_formatter(md.DateFormatter(style.date_formatter))
                elif diff < timedelta(days=4):
                    date_formatter = '%H:%M'
                    xfmt = md.DateFormatter(date_formatter)
                    ax.xaxis.set_major_formatter(xfmt)
                    if diff < timedelta(minutes=20):
                        ax.xaxis.set_major_locator(MinuteLocator(byminute=range(60), interval=2))
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=1))
                    elif diff < timedelta(hours=1):
                        ax.xaxis.set_major_locator(MinuteLocator(byminute=range(60), interval=5))
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=2))
                    elif diff < timedelta(hours=6):
                        locator = HourLocator(interval=1)
                        ax.xaxis.set_major_locator(locator)
                        ax.xaxis.set_minor_locator(MinuteLocator(interval=30))
                    elif diff < timedelta(days=3):
                        ax.xaxis.set_major_locator(HourLocator(interval=6))
                        ax.xaxis.set_minor_locator(HourLocator(interval=1))
                elif diff < timedelta(days=10):
                    locator = DayLocator(interval=2)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %y'))
                    day_locator = DayLocator(interval=1)
                    ax.xaxis.set_minor_locator(day_locator)
                elif diff < timedelta(days=40):
                    locator = DayLocator(interval=10)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b %y'))
                    day_locator = DayLocator(interval=1)
                    ax.xaxis.set_minor_locator(day_locator)
                elif diff < timedelta(days=182.5):
                    locator = MonthLocator(bymonthday=1, interval=2)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))
                    months_locator = MonthLocator(interval=1)
                    ax.xaxis.set_minor_locator(months_locator)
                elif diff < timedelta(days=730):
                    locator = MonthLocator(bymonthday=1, interval=3)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))
                    months_locator = MonthLocator(interval=1)
                    ax.xaxis.set_minor_locator(months_locator)
                elif diff < timedelta(days=1825):
                    locator = YearLocator()
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
                else:
                    years = floor(diff.days / 365.0 / 5.0)
                    locator = YearLocator(years)
                    ax.xaxis.set_major_locator(locator)
                    ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
                if matplotlib.__version__ > '1.9':
                    max = dates.max()
                    min = dates.min()
                    plt.xlim(min, max)
            except:
                try:
                    max = dates.max()
                    min = dates.min()
                    big_step = self.round_to_1((max - min) / 10)
                    small_step = big_step / 5
                    ax.xaxis.set_major_locator(MultipleLocator(big_step))
                    ax.xaxis.set_minor_locator(MultipleLocator(small_step))
                    plt.xlim(min, max)
                except:
                    pass

        return

    def get_axis(self, ax, ax2, label, y_axis_2_series):
        if label in y_axis_2_series:
            return ax2
        return ax

    def trendline(self, ax, xd, yd, order=1, color='red', alpha=1, Rval=False, scale_factor=1):
        """ Make a line of best fit """
        xd[np.isnan(xd)] = 0
        yd[np.isnan(yd)] = 0
        coeffs = np.polyfit(xd, yd, order)
        intercept = coeffs[(-1)]
        slope = coeffs[(-2)]
        if order == 2:
            power = coeffs[0]
        else:
            power = 0
        minxd = np.min(xd)
        maxxd = np.max(xd)
        xl = np.array([minxd, maxxd])
        yl = power * xl ** 2 + slope * xl + intercept
        ax.plot(xl, yl, color=color, alpha=alpha)
        p = np.poly1d(coeffs)
        ybar = np.sum(yd) / len(yd)
        ssreg = np.sum((p(xd) - ybar) ** 2)
        sstot = np.sum((yd - ybar) ** 2)
        Rsqr = ssreg / sstot
        if Rval == False:
            text = 'R^2 = %0.2f, m = %0.4f, c = %0.4f' % (Rsqr, slope, intercept)
            ax.annotate(text, xy=(1, 1), xycoords='axes fraction', fontsize=8 * abs(scale_factor), xytext=(
             -5 * abs(scale_factor), 10 * abs(scale_factor)), textcoords='offset points', ha='right', va='top')
        else:
            return Rsqr

    def _create_brand_label(self, ax, anno, scale_factor):
        ax.annotate(anno, xy=(1, 1), xycoords='axes fraction', fontsize=10 * abs(scale_factor), color='white', xytext=(
         0 * abs(scale_factor), 15 * abs(scale_factor)), textcoords='offset points', va='center', ha='center', bbox=dict(boxstyle='round,pad=0.0', facecolor=cc.chartfactory_brand_color))

    def _create_subplot(self, fig, chart_type, style, subplot_no, first_ax, ordinal):
        if style.title is not None:
            fig.suptitle(style.title, fontsize=14 * abs(style.scale_factor))
        chart_projection = '2d'
        if not isinstance(chart_type, list):
            if chart_type == 'surface':
                chart_projection = '3d'
        if style.subplots == False and first_ax is None:
            if chart_projection == '3d':
                ax = fig.add_subplot(111, projection=chart_projection)
            else:
                ax = fig.add_subplot(111)
        else:
            if first_ax is None:
                if chart_projection == '3d':
                    ax = fig.add_subplot(2, 1, subplot_no, projection=chart_projection)
                else:
                    ax = fig.add_subplot(2, 1, subplot_no)
                first_ax = ax
            if style.share_subplot_x:
                if chart_projection == '3d':
                    ax = fig.add_subplot(2, 1, subplot_no, sharex=first_ax, projection=chart_projection)
                else:
                    ax = fig.add_subplot(2, 1, subplot_no, sharex=first_ax)
            elif chart_projection == '3d':
                ax = fig.add_subplot(2, 1, subplot_no, projection=chart_projection)
            else:
                ax = fig.add_subplot(2, 1, subplot_no)
        subplot_no = subplot_no + 1
        if style.x_title != '':
            ax.set_xlabel(style.x_title)
        if style.y_title != '':
            ax.set_ylabel(style.y_title)
        plt.xlabel(style.x_title)
        plt.ylabel(style.y_title)
        y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)
        ax2 = []
        ax.xaxis.grid(style.x_axis_showgrid)
        ax.yaxis.grid(style.y_axis_showgrid)
        if style.y_axis_2_series != []:
            ax2 = ax.twinx()
            ax2.yaxis.grid(style.y_axis_2_showgrid)
        return (ax, ax2, subplot_no, ordinal + 1)

    def _create_legend(self, ax, ax2, style):
        if style.display_source_label == True and style.source is not None:
            ax.annotate('Source: ' + style.source, xy=(1, 0), xycoords='axes fraction', fontsize=7 * abs(style.scale_factor), xytext=(
             -5 * abs(style.scale_factor), 10 * abs(style.scale_factor)), textcoords='offset points', ha='right', va='top', color=style.source_color)
        if style.display_brand_label == True:
            self._create_brand_label(ax, anno=style.brand_label, scale_factor=abs(style.scale_factor))
        leg = []
        leg2 = []
        loc = 'best'
        if ax2 != []:
            loc = 2
        try:
            leg = ax.legend(loc=loc, prop={'size': 10 * abs(style.scale_factor)})
            leg.get_frame().set_linewidth(0.0)
            leg.get_frame().set_alpha(0)
            if ax2 != []:
                leg2 = ax2.legend(loc=1, prop={'size': 10 * abs(style.scale_factor)})
                leg2.get_frame().set_linewidth(0.0)
                leg2.get_frame().set_alpha(0)
        except:
            pass

        try:
            if style.display_legend is False:
                if leg != []:
                    leg.remove()
                if leg2 != []:
                    leg.remove()
        except:
            pass

        return


cf = None
try:
    import plotly, plotly.offline as py_offline, cufflinks as cf
    plotly.tools.set_config_file(plotly_domain='https://type-here.com', world_readable=cc.plotly_world_readable, sharing=cc.plotly_sharing)
except:
    pass

try:
    from plotly.graph_objs import Figure
    import plotly.graph_objs as go, plotly.plotly as py_online
except:
    from plotly.graph_objects import Figure
    import plotly.graph_objects as go, chart_studio.plotly as py_online

try:
    import base64
except:
    pass

class EnginePlotly(EngineTemplate):

    def start_orca(self, path=None):
        if path is not None:
            plotly.io.orca.config.executable = path
        plotly.io.orca.ensure_server()
        return

    def plot_chart(self, data_frame, style, chart_type):
        if isinstance(data_frame, go.Figure):
            return self.publish_plot(data_frame, style)
        else:
            mode = 'lines'
            if style is None:
                style = Style()
            marker_size = 1
            x = ''
            y = ''
            z = ''
            scale = 1
            try:
                if style.plotly_plot_mode == 'offline_html' and style.scale_factor > 0:
                    scale = float(2.0 / 3.0)
            except:
                pass

            cm = ColorMaster()
            data_frame_list = self.split_data_frame_to_list(data_frame, style)
            fig_list = []
            cols = []
            for data_frame in data_frame_list:
                cols.append(data_frame.columns)

            cols = list(numpy.array(cols).flat)
            color_list = cm.create_color_list(style, [], cols=cols)
            color_spec = []
            if color_list == [None] * len(color_list):
                color_spec = [
                 None] * len(color_list)
                for i in range(0, len(color_list)):
                    if color_spec[i] is None:
                        color_spec[i] = self.get_color_list(i)
                    try:
                        color_spec[i] = matplotlib.colors.rgb2hex(color_spec[i])
                    except:
                        pass

            else:
                for color in color_list:
                    color = 'rgba' + str(color)
                    color_spec.append(color)

                start = 0
                for i in range(0, len(data_frame_list)):
                    data_frame = data_frame_list[i]
                    if isinstance(chart_type, list):
                        chart_type_ord = chart_type[i]
                    else:
                        chart_type_ord = chart_type
                    end = start + len(data_frame.columns)
                    color_spec1 = color_spec[start:start + end]
                    start = end
                    if chart_type_ord == 'choropleth':
                        for col in data_frame.columns:
                            try:
                                data_frame[col] = data_frame[col].astype(str)
                            except:
                                pass

                        if style.color != []:
                            color = style.color
                        else:
                            color = [
                             [
                              0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
                             [
                              0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
                        text = ''
                        if 'text' in data_frame.columns:
                            text = data_frame['Text']
                        data = [
                         dict(type='choropleth', colorscale=color, autocolorscale=False, locations=data_frame['Code'], z=data_frame[style.plotly_choropleth_field].astype(float), locationmode=style.plotly_location_mode, text=text, marker=dict(line=dict(color='rgb(255,255,255)', width=1)), colorbar=dict(title=style.units))]
                        layout = dict(title=style.title, geo=dict(scope=style.plotly_scope, projection=dict(type=style.plotly_projection), showlakes=True, lakecolor='rgb(255, 255, 255)'))
                        fig = dict(data=data, layout=layout)
                    elif style.plotly_helper == 'cufflinks':
                        if chart_type_ord == 'surface':
                            fig = data_frame.iplot(kind=chart_type, title=style.title, xTitle=style.x_title, yTitle=style.y_title, x=x, y=y, z=z, mode=mode, size=marker_size, sharing=style.plotly_sharing, theme=style.plotly_theme, bestfit=style.line_of_best_fit, legend=style.display_legend, colorscale=style.color, dimensions=(
                             style.width * abs(style.scale_factor) * scale,
                             style.height * abs(style.scale_factor) * scale), asFigure=True)
                        elif chart_type_ord == 'heatmap':
                            fig = data_frame.iplot(kind=chart_type, title=style.title, xTitle=style.x_title, yTitle=style.y_title, x=x, y=y, mode=mode, size=marker_size, sharing=style.plotly_sharing, theme=style.plotly_theme, bestfit=style.line_of_best_fit, legend=style.display_legend, colorscale=style.color, dimensions=(
                             style.width * abs(style.scale_factor) * scale,
                             style.height * abs(style.scale_factor) * scale), asFigure=True)
                        else:
                            full_line = style.connect_line_gaps
                            if chart_type_ord == 'line':
                                full_line = True
                                mode = 'lines'
                            else:
                                if chart_type_ord in ('dash', 'dashdot', 'dot'):
                                    chart_type_ord = 'scatter'
                                elif chart_type_ord == 'line+markers':
                                    full_line = True
                                    chart_type_ord = 'line'
                                    mode = 'lines+markers'
                                    marker_size = 5
                                elif chart_type_ord == 'scatter':
                                    mode = 'markers'
                                    marker_size = 5
                                elif chart_type_ord == 'bubble':
                                    chart_type_ord = 'scatter'
                                    mode = 'markers'
                                if style.plotly_theme is None:
                                    plotly_theme = 'pearl'
                                else:
                                    plotly_theme = style.plotly_theme
                                m = 0
                                while m < 10:
                                    try:
                                        fig = data_frame.iplot(kind=chart_type_ord, title=style.title, xTitle=style.x_title, yTitle=style.y_title, x=x, y=y, z=z, subplots=False, sharing=style.plotly_sharing, mode=mode, secondary_y=style.y_axis_2_series, size=marker_size, theme=plotly_theme, colorscale='dflt', bestfit=style.line_of_best_fit, legend=style.display_legend, width=style.linewidth, color=color_spec1, dimensions=(
                                         style.width * abs(style.scale_factor) * scale,
                                         style.height * abs(style.scale_factor) * scale), asFigure=True)
                                        m = 10
                                        break
                                    except Exception as e:
                                        print 'Will attempt to re-render: ' + str(e)
                                        import time
                                        time.sleep(0.3)

                                    m = m + 1

                            if full_line:
                                for z in range(0, len(fig['data'])):
                                    fig['data'][z].connectgaps = style.connect_line_gaps
                                    for k in range(0, len(fig['data'])):
                                        if full_line:
                                            fig['data'][k].connectgaps = style.connect_line_gaps

                            if style.line_shape != None:
                                if isinstance(style.line_shape, str):
                                    line_shape = [
                                     style.line_shape] * len(fig['data'])
                                else:
                                    line_shape = style.line_shape
                                for k in range(0, len(fig['data'])):
                                    fig['data'][k].line.shape = line_shape[k]

                            if style.plotly_webgl:
                                for k in range(0, len(fig['data'])):
                                    if fig['data'][k].type == 'scatter':
                                        fig['data'][k].type = 'scattergl'

                    elif style.plotly_helper == 'plotly_express':
                        pass
                    if style.y_axis_range is not None:
                        fig.update(dict(layout=dict(yaxis=dict(range=style.y_axis_range))))
                    if style.x_axis_range is not None:
                        fig.update(dict(layout=dict(xaxis=dict(range=style.x_axis_range))))
                    fig.update(dict(layout=dict(legend=dict(x=0.05, y=1))))
                    if style.thin_margin:
                        fig.update(dict(layout=dict(margin=go.layout.Margin(l=20, r=20, b=40, t=40, pad=0))))
                    fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
                    fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))
                    if not style.x_axis_showgrid:
                        fig.update(dict(layout=dict(xaxis=dict(showgrid=style.x_axis_showgrid))))
                    if not style.y_axis_showgrid:
                        fig.update(dict(layout=dict(yaxis=dict(showgrid=style.y_axis_showgrid))))
                    if not style.y_axis_2_showgrid:
                        fig.update(dict(layout=dict(yaxis2=dict(showgrid=style.y_axis_2_showgrid))))
                    fig_list.append(fig)

                if len(fig_list) > 1:
                    fig = cf.subplots(fig_list)
                    fig['layout'].update(title=style.title)
                else:
                    fig = fig_list[0]
                if style.subplots == False and isinstance(chart_type, list):
                    for j in range(0, len(fig['data'])):
                        mode = None
                        dash = None
                        line_shape = None
                        if chart_type[j] == 'line':
                            mode = 'lines'
                        elif chart_type[j] == 'line+markers':
                            mode = 'lines+markers'
                        elif chart_type[j] == 'scatter':
                            mode = 'markers'
                        elif chart_type[j] in ('dash', 'dashdot', 'dot'):
                            dash = chart_type[j]
                            mode = 'lines'
                        elif chart_type[j] in ('hv', 'vh', 'vhv', 'spline', 'linear'):
                            line_shape = chart_type[j]
                            mode = 'lines'
                        elif chart_type[j] == 'bubble':
                            mode = 'markers'
                            bubble_series = style.bubble_series[cols[j]]
                            bubble_series = bubble_series.fillna(0)
                            scale = float(bubble_series.max())
                            fig['data'][j].marker.size = (style.bubble_size_scalar * (bubble_series.values / scale)).tolist()
                        if mode is not None:
                            fig['data'][j].mode = mode
                        if dash is not None:
                            fig['data'][j].line.dash = dash
                        if line_shape is not None:
                            fig['data'][j].line.shape = line_shape

                if style.candlestick_series is not None and not style.plotly_webgl:
                    if isinstance(style.candlestick_series, Figure):
                        fig_candle = style.candlestick_series
                    else:
                        fig_candle = create_candlestick(style.candlestick_series['open'], style.candlestick_series['high'], style.candlestick_series['low'], style.candlestick_series['close'], dates=style.candlestick_series['close'].index)
                    if style.candlestick_increasing_color is not None:
                        fig_candle['data'][0].fillcolor = cm.get_color_code(style.candlestick_increasing_color)
                        fig_candle['data'][0].line.color = cm.get_color_code(style.candlestick_increasing_line_color)
                    if style.candlestick_decreasing_color is not None:
                        fig_candle['data'][1].fillcolor = cm.get_color_code(style.candlestick_decreasing_color)
                        fig_candle['data'][1].line.color = cm.get_color_code(style.candlestick_decreasing_line_color)
                    try:
                        fig.data.append(fig_candle.data[0])
                        fig.data.append(fig_candle.data[1])
                    except:
                        fig.add_trace(fig_candle.data[0])
                        fig.add_trace(fig_candle.data[1])

                x_y_line_list = []
                for x_y_line in style.x_y_line:
                    start = x_y_line[0]
                    finish = x_y_line[1]
                    x_y_line_list.append({'type': 'line', 
                       'x0': start[0], 
                       'y0': start[1], 
                       'x1': finish[0], 
                       'y1': finish[1], 
                       'line': {'color': 'black', 
                                'width': 0.5, 
                                'dash': 'dot'}})

            if len(x_y_line_list) > 0:
                fig.layout.shapes = x_y_line_list
            return self.publish_plot(fig, style)

    def publish_plot(self, fig, style):
        fig.update(dict(layout=dict(paper_bgcolor='rgba(0,0,0,0)')))
        fig.update(dict(layout=dict(plot_bgcolor='rgba(0,0,0,0)')))
        if style is None:
            style = Style()
        style = self.generate_file_names(style, 'plotly')
        if style.plotly_plot_mode == 'dash':
            pass
        else:
            if style.plotly_plot_mode == 'online':
                plotly.tools.set_credentials_file(username=style.plotly_username, api_key=style.plotly_api_key)
                py_online.plot(fig, filename=style.plotly_url, world_readable=style.plotly_world_readable, auto_open=not style.silent_display, asImage=style.plotly_as_image)
            else:
                if style.plotly_plot_mode == 'offline_html':
                    py_offline.plot(fig, filename=style.html_file_output, auto_open=not style.silent_display)
                elif style.plotly_plot_mode == 'offline_embed_js_div':
                    return py_offline.plot(fig, include_plotlyjs=True, output_type='div')
                if style.plotly_plot_mode == 'offline_div':
                    return py_offline.plot(fig, include_plotlyjs=False, output_type='div')
            if style.plotly_plot_mode == 'offline_image_png_bytes':
                return plotly.io.to_image(fig, format='png')
        if style.plotly_plot_mode == 'offline_image_png_in_html':
            return '<img src="data:image/png;base64,' + base64.b64encode(plotly.io.to_image(fig, format='png')).decode('utf8') + '">'
        else:
            if style.plotly_plot_mode == 'offline_jupyter':
                py_offline.init_notebook_mode()
                py_offline.iplot(fig)
            elif style.plotly_plot_mode != 'dash':
                try:
                    py_online.image.save_as(fig, filename=style.file_output, format='png', width=style.width * abs(style.scale_factor), height=style.height * abs(style.scale_factor))
                except:
                    pass

            return fig

    def get_color_list(self, i):
        color_palette = cc.plotly_palette
        return color_palette[(i % len(color_palette))]


class ColorMaster():

    def create_color_list(self, style, data_frame, cols=None):
        if cols is None:
            cols = data_frame.columns
        color = self.construct_color(style, 'color', len(cols) - len(style.color_2_series))
        color_2 = self.construct_color(style, 'color_2', len(style.color_2_series))
        return self.assign_color(cols, color, color_2, style.exclude_from_color, style.color_2_series)

    def construct_color(self, style, color_field_name, no_of_entries):
        color = []
        if hasattr(style, color_field_name):
            if isinstance(getattr(style, color_field_name), list):
                color = getattr(style, color_field_name, color)
            else:
                try:
                    color = self.create_colormap(no_of_entries, getattr(style, color_field_name))
                except:
                    pass

        return color

    def exclude_from_color(self, style):
        if not isinstance(style.exclude_from_color, list):
            style.exclude_from_color = [
             style.exclude_from_color]
        exclude_from_color = [ str(x) for x in style.exclude_from_color ]
        return exclude_from_color

    def assign_color(self, labels, color, color_2, exclude_from_color, color_2_series):
        color_list = []
        axis_1_color_index = 0
        axis_2_color_index = 0
        labels = [ str(x) for x in labels ]
        for label in labels:
            color_spec = None
            if label in exclude_from_color:
                color_spec = None
            else:
                if label in color_2_series:
                    if color_2 != []:
                        color_spec = self.get_color_code(color_2[axis_2_color_index])
                        axis_2_color_index = axis_2_color_index + 1
                elif color != []:
                    color_spec = self.get_color_code(color[axis_1_color_index])
                    axis_1_color_index = axis_1_color_index + 1
                try:
                    color_spec = matplotlib.colors.colorConverter.to_rgba(color_spec)
                except:
                    pass

            color_list.append(color_spec)

        return color_list

    def get_color_code(self, code):
        dict = cc.chartfactory_color_overwrites
        if code in dict:
            return dict[code]
        return code

    def create_colormap(self, num_colors, map_name):
        cm = matplotlib.cm.get_cmap(name=map_name)
        return [ cm(1.0 * i / num_colors) for i in range(num_colors) ]


from plotly.figure_factory import utils
from plotly.figure_factory._ohlc import _DEFAULT_INCREASING_COLOR, _DEFAULT_DECREASING_COLOR, validate_ohlc

def make_increasing_candle(open, high, low, close, dates, **kwargs):
    """
    Makes boxplot trace for increasing candlesticks

    _make_increasing_candle() and _make_decreasing_candle separate the
    increasing traces from the decreasing traces so kwargs (such as
    color) can be passed separately to increasing or decreasing traces
    when direction is set to 'increasing' or 'decreasing' in
    FigureFactory.create_candlestick()

    :param (list) open: opening values
    :param (list) high: high values
    :param (list) low: low values
    :param (list) close: closing values
    :param (list) dates: list of datetime objects. Default: None
    :param kwargs: kwargs to be passed to increasing trace via
        plotly.graph_objs.Scatter.

    :rtype (list) candle_incr_data: list of the box trace for
        increasing candlesticks.
    """
    increase_x, increase_y = _Candlestick(open, high, low, close, dates, **kwargs).get_candle_increase()
    if 'line' in kwargs:
        kwargs.setdefault('fillcolor', kwargs['line']['color'])
    else:
        kwargs.setdefault('fillcolor', _DEFAULT_INCREASING_COLOR)
    if 'name' in kwargs:
        kwargs.setdefault('showlegend', True)
    else:
        kwargs.setdefault('showlegend', False)
    kwargs.setdefault('name', 'Increasing')
    kwargs.setdefault('line', dict(color=_DEFAULT_INCREASING_COLOR))
    candle_incr_data = dict(type='box', x=increase_x, y=increase_y, whiskerwidth=0, boxpoints=False, **kwargs)
    return [
     candle_incr_data]


def make_decreasing_candle(open, high, low, close, dates, **kwargs):
    """
    Makes boxplot trace for decreasing candlesticks

    :param (list) open: opening values
    :param (list) high: high values
    :param (list) low: low values
    :param (list) close: closing values
    :param (list) dates: list of datetime objects. Default: None
    :param kwargs: kwargs to be passed to decreasing trace via
        plotly.graph_objs.Scatter.

    :rtype (list) candle_decr_data: list of the box trace for
        decreasing candlesticks.
    """
    decrease_x, decrease_y = _Candlestick(open, high, low, close, dates, **kwargs).get_candle_decrease()
    if 'line' in kwargs:
        kwargs.setdefault('fillcolor', kwargs['line']['color'])
    else:
        kwargs.setdefault('fillcolor', _DEFAULT_DECREASING_COLOR)
    kwargs.setdefault('showlegend', False)
    kwargs.setdefault('line', dict(color=_DEFAULT_DECREASING_COLOR))
    kwargs.setdefault('name', 'Decreasing')
    candle_decr_data = dict(type='box', x=decrease_x, y=decrease_y, whiskerwidth=0, boxpoints=False, **kwargs)
    return [
     candle_decr_data]


def create_candlestick(open, high, low, close, dates=None, direction='both', **kwargs):
    """
    BETA function that creates a candlestick chart

    :param (list) open: opening values
    :param (list) high: high values
    :param (list) low: low values
    :param (list) close: closing values
    :param (list) dates: list of datetime objects. Default: None
    :param (string) direction: direction can be 'increasing', 'decreasing',
        or 'both'. When the direction is 'increasing', the returned figure
        consists of all candlesticks where the close value is greater than
        the corresponding open value, and when the direction is
        'decreasing', the returned figure consists of all candlesticks
        where the close value is less than or equal to the corresponding
        open value. When the direction is 'both', both increasing and
        decreasing candlesticks are returned. Default: 'both'
    :param kwargs: kwargs passed through plotly.graph_objs.Scatter.
        These kwargs describe other attributes about the ohlc Scatter trace
        such as the color or the legend name. For more information on valid
        kwargs call help(plotly.graph_objs.Scatter)

    :rtype (dict): returns a representation of candlestick chart figure.

    Example 1: Simple candlestick chart from a Pandas DataFrame
    ```
    import plotly.plotly as py
    from plotly.figure_factory import create_candlestick
    from datetime import datetime

    import pandas.io.data as web

    df = web.DataReader("aapl", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))
    fig = create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
    py.plot(fig, filename='finance/aapl-candlestick', validate=False)
    ```

    Example 2: Add text and annotations to the candlestick chart
    ```
    fig = create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)
    # Update the fig - all options here: https://plot.ly/python/reference/#Layout
    fig['layout'].update({
        'title': 'The Great Recession',
        'yaxis': {'title': 'AAPL Stock'},
        'shapes': [{
            'x0': '2007-12-01', 'x1': '2007-12-01',
            'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
            'line': {'color': 'rgb(30,30,30)', 'width': 1}
        }],
        'annotations': [{
            'x': '2007-12-01', 'y': 0.05, 'xref': 'x', 'yref': 'paper',
            'showarrow': False, 'xanchor': 'left',
            'text': 'Official start of the recession'
        }]
    })
    py.plot(fig, filename='finance/aapl-recession-candlestick', validate=False)
    ```

    Example 3: Customize the candlestick colors
    ```
    import plotly.plotly as py
    from plotly.figure_factory import create_candlestick
    from plotly.graph_objs import Line, Marker
    from datetime import datetime

    import pandas.io.data as web

    df = web.DataReader("aapl", 'yahoo', datetime(2008, 1, 1), datetime(2009, 4, 1))

    # Make increasing candlesticks and customize their color and name
    fig_increasing = create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index,
        direction='increasing', name='AAPL',
        marker=Marker(color='rgb(150, 200, 250)'),
        line=Line(color='rgb(150, 200, 250)'))

    # Make decreasing candlesticks and customize their color and name
    fig_decreasing = create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index,
        direction='decreasing',
        marker=Marker(color='rgb(128, 128, 128)'),
        line=Line(color='rgb(128, 128, 128)'))

    # Initialize the figure
    fig = fig_increasing

    # Add decreasing data with .extend()
    fig['data'].extend(fig_decreasing['data'])

    py.iplot(fig, filename='finance/aapl-candlestick-custom', validate=False)
    ```

    Example 4: Candlestick chart with datetime objects
    ```
    import plotly.plotly as py
    from plotly.figure_factory import create_candlestick

    from datetime import datetime

    # Add data
    open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
    high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
    low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
    close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
    dates = [datetime(year=2013, month=10, day=10),
             datetime(year=2013, month=11, day=10),
             datetime(year=2013, month=12, day=10),
             datetime(year=2014, month=1, day=10),
             datetime(year=2014, month=2, day=10)]

    # Create ohlc
    fig = create_candlestick(open_data, high_data,
        low_data, close_data, dates=dates)

    py.iplot(fig, filename='finance/simple-candlestick', validate=False)
    ```
    """
    if direction is 'increasing':
        candle_incr_data = make_increasing_candle(open, high, low, close, dates, **kwargs)
        data = candle_incr_data
    elif direction is 'decreasing':
        candle_decr_data = make_decreasing_candle(open, high, low, close, dates, **kwargs)
        data = candle_decr_data
    else:
        candle_incr_data = make_increasing_candle(open, high, low, close, dates, **kwargs)
        candle_decr_data = make_decreasing_candle(open, high, low, close, dates, **kwargs)
        data = candle_incr_data + candle_decr_data
    layout = go.Layout()
    return go.Figure(data=data, layout=layout)


class _Candlestick(object):
    """
    Refer to FigureFactory.create_candlestick() for docstring.
    """

    def __init__(self, open, high, low, close, dates, **kwargs):
        self.open = open.values
        self.high = high.values
        self.low = low.values
        self.close = close.values
        if dates is not None:
            self.x = dates
        else:
            self.x = [ x for x in range(len(self.open)) ]
        self.get_candle_increase()
        return

    def get_candle_increase(self):
        """
        Separate increasing data from decreasing data.

        The data is increasing when close value > open value
        and decreasing when the close value <= open value.
        """
        increase_y = []
        increase_x = []
        for index in range(len(self.open)):
            if self.close[index] > self.open[index]:
                increase_y.append(self.low[index])
                increase_y.append(self.open[index])
                increase_y.append(self.close[index])
                increase_y.append(self.close[index])
                increase_y.append(self.close[index])
                increase_y.append(self.high[index])
                increase_x.append(self.x[index])

        increase_x = [ [x, x, x, x, x, x] for x in increase_x ]
        increase_x = utils.flatten(increase_x)
        return (
         increase_x, increase_y)

    def get_candle_decrease(self):
        """
        Separate increasing data from decreasing data.

        The data is increasing when close value > open value
        and decreasing when the close value <= open value.
        """
        decrease_y = []
        decrease_x = []
        for index in range(len(self.open)):
            if self.close[index] <= self.open[index]:
                decrease_y.append(self.low[index])
                decrease_y.append(self.open[index])
                decrease_y.append(self.close[index])
                decrease_y.append(self.close[index])
                decrease_y.append(self.close[index])
                decrease_y.append(self.high[index])
                decrease_x.append(self.x[index])

        decrease_x = [ [x, x, x, x, x, x] for x in decrease_x ]
        decrease_x = utils.flatten(decrease_x)
        return (
         decrease_x, decrease_y)