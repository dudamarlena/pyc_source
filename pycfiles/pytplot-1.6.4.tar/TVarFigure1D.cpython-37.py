# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/TVarFigure1D.py
# Compiled at: 2020-04-30 01:29:24
# Size of source mod 2**32: 20433 bytes
import pyqtgraph as pg, numpy as np, pytplot
from collections import OrderedDict
import CustomAxis.DateAxis as DateAxis
from CustomLegend.CustomLegend import CustomLegendItem
import CustomAxis.AxisItem as AxisItem
import CustomViewBox.NoPaddingPlot as NoPaddingPlot
import CustomLinearRegionItem.CustomLinearRegionItem as CustomLinearRegionItem

class TVarFigure1D(pg.GraphicsLayout):

    def __init__(self, tvar_name, show_xaxis=False):
        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        if 'show_all_axes' in pytplot.tplot_opt_glob:
            if pytplot.tplot_opt_glob['show_all_axes']:
                self.show_xaxis = True
        else:
            self.crosshair = pytplot.tplot_opt_glob['crosshair']
            pg.GraphicsLayout.__init__(self)
            self.layout.setHorizontalSpacing(10)
            self.layout.setContentsMargins(0, 0, 0, 0)
            if self.show_xaxis:
                self.xaxis = DateAxis(orientation='bottom')
                self.xaxis.setHeight(35)
                self.xaxis.enableAutoSIPrefix(enable=False)
            else:
                self.xaxis = DateAxis(orientation='bottom', showValues=False)
                self.xaxis.setHeight(0)
                self.xaxis.enableAutoSIPrefix(enable=False)
            self.yaxis = AxisItem('left')
            self.yaxis.setWidth(100)
            vb = NoPaddingPlot()
            self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom':self.xaxis,  'left':self.yaxis}, viewBox=vb)
            self.legendvb = pg.ViewBox(enableMouse=False)
            self.legendvb.setMaximumWidth(100)
            self.legendvb.setXRange(0, 1, padding=0)
            self.legendvb.setYRange(0, 1, padding=0)
            self.addItem(self.legendvb, 0, 1)
            self.curves = []
            self.colors = self._setcolors()
            self.colormap = self._setcolormap()
            if pytplot.tplot_opt_glob['black_background']:
                self.labelStyle = {'font-size':str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size']) + 'pt', 
                 'color':'#FFF'}
            else:
                self.labelStyle = {'font-size':str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size']) + 'pt',  'color':'#000'}
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        self.hoverlegend.setItem('Date:', '0')
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', '0')
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', '0')
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def _set_crosshairs(self):
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=(pg.mkPen('k')))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=(pg.mkPen('k')))
        self.plotwindow.addItem((self.vLine), ignoreBounds=True)
        self.plotwindow.addItem((self.hLine), ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)

    def _set_roi_lines(self):
        if 'roi_lines' in pytplot.tplot_opt_glob.keys():
            roi_1 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][0])
            roi_2 = pytplot.tplot_utilities.str_to_int(pytplot.tplot_opt_glob['roi_lines'][1])
            x = pytplot.data_quants[self.tvar_name].coords['time']
            x_sub_1 = abs(x - roi_1 * np.ones(len(x)))
            x_sub_2 = abs(x - roi_2 * np.ones(len(x)))
            x_argmin_1 = np.nanargmin(x_sub_1)
            x_argmin_2 = np.nanargmin(x_sub_2)
            x_closest_1 = x[x_argmin_1]
            x_closest_2 = x[x_argmin_2]
            roi = CustomLinearRegionItem(orientation=(pg.LinearRegionItem.Vertical), values=[x_closest_1, x_closest_2])
            roi.setBrush([211, 211, 211, 130])
            roi.lines[0].setPen('r', width=2.5)
            roi.lines[1].setPen('r', width=2.5)
            self.plotwindow.addItem(roi)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._setxaxislabel()
        self._setyaxislabel()
        self._addlegend()
        self._addtimebars()
        if self.crosshair:
            self._set_crosshairs()
            self._addmouseevents()
        self._set_roi_lines()

    def _setxaxislabel(self):
        if self.show_xaxis:
            (self.xaxis.setLabel)((pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['axis_label']), **self.labelStyle)

    def _setyaxislabel(self):
        if 'axis_subtitle' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']
            sublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle']
            (self.yaxis.setLabel)(f"<center>{label} <br> {sublabel} <\\center>", **self.labelStyle)
        else:
            (self.yaxis.setLabel)((pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']), **self.labelStyle)

    def getfig(self):
        return self

    def _visdata(self):
        datasets = [
         pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        line_num = 0
        for dataset in datasets:
            plot_options = dataset.attrs['plot_options']
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe_lineplots(dataset.name)
            for i in range(len(dataset.columns)):
                if 'line_style' in plot_options['line_opt']:
                    if plot_options['line_opt']['line_style'] == 'scatter':
                        self.curves.append(self.plotwindow.scatterPlot(x=(dataset.index.tolist()), y=(dataset[i].tolist()),
                          pen=(self.colors[(line_num % len(self.colors))]),
                          symbol='+'))
                        line_num += 1
                        continue
                else:
                    limit = pytplot.tplot_opt_glob['data_gap']
                    if limit != 0:
                        nan_values = dataset[i][dataset[i].isnull().values].index.tolist()
                        nan_keys = [dataset[i].index.tolist().index(j) for j in nan_values]
                        count = 0
                        flag = False
                        consec_list = list()
                        overall_list = list()
                        for val, actual_value in enumerate(nan_keys):
                            if actual_value != nan_keys[(-1)]:
                                diff = abs(nan_keys[val] - nan_keys[(val + 1)])
                                t_now = nan_values[val]
                                t_next = nan_values[(val + 1)]
                                time_accum = abs(t_now - t_next)
                                if diff == 1:
                                    if count < limit:
                                        count += time_accum
                                        consec_list.append(nan_keys[val])
                                if diff == 1 and count >= limit:
                                    if not flag:
                                        count += time_accum
                                        if consec_list[0] != 0:
                                            consec_list.insert(0, consec_list[0] - 1)
                                        overall_list.append(consec_list)
                                        overall_list.append([nan_keys[val]])
                                        flag = True
                                if diff == 1:
                                    if count > limit:
                                        if flag:
                                            count += time_accum
                                            overall_list.append([nan_keys[val]])
                                if diff != 1:
                                    count = 0
                                    consec_list = []
                                    flag = False
                                    if nan_keys[(val - 1)] in [y for x in overall_list for y in x]:
                                        overall_list.append([nan_keys[val]])

                        overall_list = [y for x in overall_list for y in x]
                        time_filtered = np.array([1] * len(dataset.index.tolist()))
                        time_filtered[overall_list] = 0
                    if limit != 0:
                        self.curves.append(self.plotwindow.plot(x=(dataset.index.tolist()), y=(dataset[i].tolist()),
                          pen=(self.colors[(line_num % len(self.colors))]),
                          connect=time_filtered))
                    else:
                        self.curves.append(self.plotwindow.plot(x=(dataset.index.tolist()), y=(dataset[i].tolist()),
                          pen=(self.colors[(line_num % len(self.colors))])))
                line_num += 1

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)

    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            legend_names = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['legend_names']
            n_items = len(legend_names)
            bottom_bound = 0.5 + (n_items - 1) * 0.05
            top_bound = 0.5 - (n_items - 1) * 0.05
            if len(legend_names) != len(self.curves):
                print('Number of lines do not match length of legend names')
            elif len(legend_names) == 1:
                pos_array = [
                 0.5]
            else:
                pos_array = np.linspace(bottom_bound, top_bound, len(legend_names))
            i = 0
            for legend_name in legend_names:

                def rgb(red, green, blue):
                    return '#%02x%02x%02x' % (red, green, blue)

                r = self.colors[(i % len(self.colors))][0]
                g = self.colors[(i % len(self.colors))][1]
                b = self.colors[(i % len(self.colors))][2]
                hex_num = rgb(r, g, b)
                color_text = 'color: ' + hex_num
                font_size = 'font-size: ' + str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size']) + 'pt'
                opts = [color_text, font_size]
                full = "<span style='%s'>%s</span>" % ('; '.join(opts), legend_name)
                if i + 1 == len(legend_names):
                    text = pg.TextItem(anchor=(0, 0.5))
                    text.setHtml(full)
                else:
                    if i == 0:
                        text = pg.TextItem(anchor=(0, 0.5))
                        text.setHtml(full)
                    else:
                        text = pg.TextItem(anchor=(0, 0.5))
                        text.setHtml(full)
                self.legendvb.addItem(text)
                text.setPos(0, pos_array[i])
                i += 1

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def _mousemoved(self, evt):
        pos = evt
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousepoint = self.plotwindow.vb.mapSceneToView(pos)
            index_x = int(mousepoint.x())
            index_y = round(float(mousepoint.y()), 4)
            date = pytplot.tplot_utilities.int_to_str(index_x)[0:10]
            time = pytplot.tplot_utilities.int_to_str(index_x)[11:19]
            pytplot.hover_time.change_hover_time(int(mousepoint.x()), self.tvar_name)
            if self.crosshair:
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)
                self.hoverlegend.setVisible(True)
                self.hoverlegend.setItem('Date:', date)
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', time)
                self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', str(index_y))
        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        return 'linear'

    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'

    def _getzaxistype(self):
        pass

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.tplot_utilities.rgb_color(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color'])
        return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        pass

    @staticmethod
    def getaxistype():
        axis_type = 'time'
        link_y_axis = False
        return (axis_type, link_y_axis)

    def _setxrange(self):
        if 'x_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['x_range'][0], pytplot.tplot_opt_glob['x_range'][1])

    def _setyrange(self):
        if self._getyaxistype() == 'log' and not pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0] <= 0:
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1] <= 0:
                return
            self.plotwindow.vb.setYRange((np.log10(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0])), (np.log10(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1])),
              padding=0)
        else:
            self.plotwindow.vb.setYRange((pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][0]), (pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_range'][1]),
              padding=0)

    def _setzrange(self):
        pass

    def _addtimebars(self):
        dict_length = len(pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'])
        for i in range(dict_length):
            if pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['dimension'] == 'height':
                angle = 90
            else:
                angle = 0
            date_to_highlight = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['location']
            color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['line_color']
            thick = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['line_width']
            infline = pg.InfiniteLine(pos=date_to_highlight, pen=pg.mkPen(color, width=thick), angle=angle)
            self.plotwindow.addItem(infline)