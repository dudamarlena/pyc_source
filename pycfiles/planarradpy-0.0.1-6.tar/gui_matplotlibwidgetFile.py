# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marrabld/Projects/planarradpy/gui/gui_matplotlibwidgetFile.py
# Compiled at: 2015-05-31 03:41:10
import sys
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import scipy
from matplotlib.figure import Figure
import matplotlib.pyplot
from pylab import *
import seaborn as sns, sys
sys.path.append('..')
sys.path.append('../gui')

class MplCanvas(FigureCanvas):
    """
    This function initializes the figure.
    Inputs : FigureCanvas : The canvas for the figure.
    """

    def __init__(self):
        self.fig = Figure()
        self.picture = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.x_data = []
        self.y_data = [[]]
        self.num_plot = 0

    def update_fields(self, x_data, y_data, num_plot):
        """
        This function updates data that we need to display curves, from "data_processing" of  "gui_mainLayout" file.
        Inputs : x_data : An array with wavelengths.
                 y_data : An array with curve's data.
                 num_plot : The line, curve to plot.
        """
        self.x_data = x_data
        self.y_data = y_data
        self.num_plot = num_plot

    def display_graphic(self, flag_curves, ui, grid):
        """
        This function plots results of a file into the canvas.
        Inputs : flag_curves : A boolean to know if we have to plot all curves or not.
                ui : The main_Window.
        """
        matplotlib.patches.Patch(linewidth=100)
        ui.graphic_widget.canvas.picture.clear()
        x = scipy.linspace(self.x_data[0], self.x_data[(-1)], len(self.x_data))
        if grid:
            ui.graphic_widget.canvas.picture.grid(True)
        curve_wanted = 0
        for curve in self.y_data:
            if flag_curves:
                if curve_wanted == self.num_plot:
                    ui.graphic_widget.canvas.picture.plot(x, curve, '-r', label=('Case : {0}/{1}').format(str(curve_wanted + 1), str(len(self.y_data))), linewidth=4)
                else:
                    ui.graphic_widget.canvas.picture.plot(x, curve, '0.75')
            elif curve_wanted == self.num_plot:
                ui.graphic_widget.canvas.picture.plot(x, curve, '-r', label=('Case : {0}/{1}').format(str(curve_wanted + 1), str(len(self.y_data))))
            curve_wanted += 1

        ui.graphic_widget.canvas.picture.set_xlabel('Wavelength (${nm}$)')
        ui.graphic_widget.canvas.picture.set_ylabel('Reflectance ($Sr^{-1}$)')
        self.legend = ui.graphic_widget.canvas.picture.legend()
        ui.graphic_widget.canvas.picture.legend(bbox_to_anchor=(1.1, 1.05))
        ui.graphic_widget.canvas.draw()


class matplotlibWidget(QtGui.QWidget):
    """
    This function initializes the place where the figure will be display.
    """

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)