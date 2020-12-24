# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/pyqt5backend/mplwidget_nav.py
# Compiled at: 2019-05-29 07:32:29
# Size of source mod 2**32: 1671 bytes
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    __doc__ = 'Class to represent the FigureCanvas widget'

    def __init__(self):
        self.fig = Figure(figsize=(30, 50), dpi=300)
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MplWidget(QtWidgets.QWidget):
    __doc__ = 'Widget defined in Qt Designer'

    def __init__(self, parent=None):
        self.win = QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.ntb.move(235, 48)
        self.vbl.addWidget(self.canvas)
        self.ntb.addWidget(self.win)
        self.setLayout(self.vbl)