# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/TVarFigureAxisOnly.py
# Compiled at: 2020-04-30 01:29:24
# Size of source mod 2**32: 2237 bytes
import pyqtgraph as pg
from scipy import interpolate
import CustomAxis.NonLinearAxis as NonLinearAxis
import CustomViewBox.CustomVB as CustomVB
import pytplot

class TVarFigureAxisOnly(pg.GraphicsLayout):

    def __init__(self, tvar_name):
        self.tvar_name = tvar_name
        pg.GraphicsLayout.__init__(self)
        self.layout.setHorizontalSpacing(50)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if pytplot.tplot_opt_glob['black_background']:
            self.labelStyle = {'font-size':str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size']) + 'pt', 
             'color':'#FFF'}
        else:
            self.labelStyle = {'font-size':str(pytplot.data_quants[self.tvar_name].attrs['plot_options']['extras']['char_size']) + 'pt',  'color':'#000'}
        vb = CustomVB(enableMouse=False)
        yaxis = pg.AxisItem('left')
        (yaxis.setLabel)((pytplot.data_quants[self.tvar_name].attrs['plot_options']['yaxis_opt']['axis_label']), **self.labelStyle)
        yaxis.setWidth(100)
        yaxis.label.rotate(90)
        yaxis.label.translate(0, -40)
        mapping_function = interpolate.interp1d(pytplot.data_quants[self.tvar_name].coords['time'].values, pytplot.data_quants[self.tvar_name].values)
        xaxis = NonLinearAxis(orientation='bottom', mapping_function=mapping_function)
        self.plotwindow = self.addPlot(row=0, col=0, axisItems={'bottom':xaxis,  'left':yaxis}, viewBox=vb, colspan=1)
        self.plotwindow.buttonsHidden = True
        self.plotwindow.setMaximumHeight(20)
        self.legendvb = pg.ViewBox(enableMouse=False)
        self.legendvb.setMaximumWidth(100)
        self.addItem(self.legendvb, 0, 1)