# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\mplwidget.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 1105 bytes
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QSize
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.mlab as mlab, matplotlib.gridspec as gridspec

class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.mpl_toolbar)
        layout.addWidget(self.canvas)