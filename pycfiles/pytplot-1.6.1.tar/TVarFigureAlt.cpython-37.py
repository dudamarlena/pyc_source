# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/TVarFigureAlt.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 13162 bytes
import pyqtgraph as pg, numpy as np, pytplot
from CustomLegend.CustomLegend import CustomLegendItem
import CustomAxis.AxisItem as AxisItem
import CustomViewBox.NoPaddingPlot as NoPaddingPlot

class TVarFigureAlt(pg.GraphicsLayout):

    def __init__(self, tvar_name, show_xaxis=False, mouse_function=None):
        self.tvar_name = tvar_name
        self.show_xaxis = show_xaxis
        self.crosshair = pytplot.tplot_opt_glob['crosshair']
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.xaxis = pg.AxisItem(orientation='bottom')
        self.xaxis.setHeight(35)
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
        if show_xaxis:
            self.plotwindow.showAxis('bottom')
        else:
            self.plotwindow.hideAxis('bottom')
        self._mouseMovedFunction = mouse_function
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=(pg.mkPen('k')))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=(pg.mkPen('k')))
        self.plotwindow.addItem((self.vLine), ignoreBounds=True)
        self.plotwindow.addItem((self.hLine), ignoreBounds=True)
        self.vLine.setVisible(False)
        self.hLine.setVisible(False)
        self.label = pg.LabelItem(justify='left')
        self.addItem((self.label), row=1, col=0)
        self.hoverlegend = CustomLegendItem(offset=(0, 0))
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', '0')
        self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', '0')
        self.hoverlegend.setVisible(False)
        self.hoverlegend.setParentItem(self.plotwindow.vb)

    def buildfigure(self):
        self._setxrange()
        self._setyrange()
        self._setyaxistype()
        self._setzaxistype()
        self._setzrange()
        self._visdata()
        self._addtimebars()
        self._setxaxislabel()
        self._setyaxislabel()
        if self.crosshair:
            self._addmouseevents()
        self._addlegend()

    def getfig(self):
        return self

    def _setxaxislabel(self):
        (self.xaxis.setLabel)(*('Altitude', ), **self.labelStyle)

    def _setyaxislabel(self):
        if 'axis_subtitle' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            label = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']
            sublabel = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_subtitle']
            (self.yaxis.setLabel)(f"<center>{label} <br> {sublabel} <\\center>", **self.labelStyle)
        else:
            (self.yaxis.setLabel)((pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']), **self.labelStyle)

    def _setyaxistype(self):
        if self._getyaxistype() == 'log':
            self.plotwindow.setLogMode(y=True)
        else:
            self.plotwindow.setLogMode(y=False)

    def _getyaxistype(self):
        if 'y_axis_type' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['y_axis_type']
        return 'linear'

    def _setxrange(self):
        if 'alt_range' in pytplot.tplot_opt_glob:
            self.plotwindow.setXRange(pytplot.tplot_opt_glob['alt_range'][0], pytplot.tplot_opt_glob['alt_range'][1])
        else:
            return

    @staticmethod
    def getaxistype():
        axis_type = 'altitude'
        link_y_axis = False
        return (axis_type, link_y_axis)

    def _addmouseevents(self):
        if self.plotwindow.scene() is not None:
            self.plotwindow.scene().sigMouseMoved.connect(self._mousemoved)

    def _mousemoved(self, evt):
        pos = evt
        if self.plotwindow.sceneBoundingRect().contains(pos):
            mousepoint = self.plotwindow.vb.mapSceneToView(pos)
            index_x = int(mousepoint.x())
            index_y = int(mousepoint.y())
            if self._mouseMovedFunction is not None:
                self._mouseMovedFunction(int(mousepoint.x()))
                self.vLine.setPos(mousepoint.x())
                self.hLine.setPos(mousepoint.y())
                self.vLine.setVisible(True)
                self.hLine.setVisible(True)
            self.hoverlegend.setVisible(True)
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['xaxis_opt']['crosshair'] + ':', index_x)
            self.hoverlegend.setItem(pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['crosshair'] + ':', index_y)
        else:
            self.hoverlegend.setVisible(False)
            self.vLine.setVisible(False)
            self.hLine.setVisible(False)

    def _addlegend(self):
        if 'legend_names' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']:
            legend_names = pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['legend_names']
            if len(legend_names) != len(self.curves):
                print('Number of lines do not match length of legend names')
            elif len(legend_names) == 1:
                pos_array = [
                 0.5]
            else:
                pos_array = np.linspace(1, 0, len(legend_names))
            i = 0
            for legend_name in legend_names:
                if i + 1 == len(legend_names):
                    text = pg.TextItem(text=legend_name, anchor=(0, 1.5), color=(self.colors[(i % len(self.colors))]))
                else:
                    if i == 0:
                        text = pg.TextItem(text=legend_name, anchor=(0, -0.5), color=(self.colors[(i % len(self.colors))]))
                    else:
                        text = pg.TextItem(text=legend_name, anchor=(0, 0.5), color=(self.colors[(i % len(self.colors))]))
                self.legendvb.addItem(text)
                text.setPos(0, pos_array[i])
                i += 1

    def _setzaxistype(self):
        if self._getzaxistype() == 'log':
            self.zscale = 'log'
        else:
            self.zscale = 'linear'

    def _getzaxistype(self):
        pass

    def _setcolors(self):
        if 'line_color' in pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']:
            return pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['line_color']
        return pytplot.tplot_utilities.rgb_color(['k', 'r', 'seagreen', 'b', 'darkturquoise', 'm', 'goldenrod'])

    def _setcolormap(self):
        pass

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
        datasets = []
        tbardict = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar']
        ltbar = len(tbardict)
        datasets = [
         pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        for dataset in datasets:
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset.name)
            for i in range(ltbar):
                test_time = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['location']
                color = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['line_color']
                pointsize = pytplot.data_quants[self.tvar_name].attrs['plot_options']['time_bar'][i]['line_width']
                time = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['alt']].coords['time'].values
                altitude = pytplot.data_quants[pytplot.data_quants[self.tvar_name].attrs['plot_options']['links']['alt']].values
                nearest_time_index = np.abs(time - test_time).argmin()
                data_point = dataset.iloc[nearest_time_index][0]
                alt_point = altitude[nearest_time_index]
                self.plotwindow.scatterPlot([alt_point], [data_point], size=pointsize, pen=(pg.mkPen(None)), brush=color)

    def _visdata(self):
        datasets = [
         pytplot.data_quants[self.tvar_name]]
        for oplot_name in pytplot.data_quants[self.tvar_name].attrs['plot_options']['overplots']:
            datasets.append(pytplot.data_quants[oplot_name])

        line_num = 0
        for dataset_xr in datasets:
            dataset = pytplot.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(dataset_xr.name)
            coords = pytplot.tplot_utilities.return_interpolated_link_dict(dataset_xr, ['alt'])
            for i in range(0, len(dataset.columns)):
                t_link = coords['alt'].coords['time'].values
                x = coords['alt'].values
                t_tvar = dataset.index.values
                data = dataset[i].values
                while t_tvar[(-1)] > t_link[(-1)]:
                    t_tvar = np.delete(t_tvar, -1)
                    data = np.delete(data, -1)

                while t_tvar[0] < t_link[0]:
                    t_tvar = np.delete(t_tvar, 0)
                    data = np.delete(data, 0)

                self.curves.append(self.plotwindow.scatterPlot((x.tolist()), (data.tolist()), pen=(pg.mkPen(None)),
                  brush=(self.colors[(line_num % len(self.colors))])))
                line_num += 1