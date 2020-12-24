# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/MatplotlibWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1442 bytes
from ..Qt import QtGui, QtCore, USE_PYSIDE, USE_PYQT5
import matplotlib
if not USE_PYQT5:
    if USE_PYSIDE:
        matplotlib.rcParams['backend.qt4'] = 'PySide'
    import matplotlib.backends.backend_qt4agg as FigureCanvas
    import matplotlib.backends.backend_qt4agg as NavigationToolbar
else:
    import matplotlib.backends.backend_qt5agg as FigureCanvas
    import matplotlib.backends.backend_qt5agg as NavigationToolbar
from matplotlib.figure import Figure

class MatplotlibWidget(QtGui.QWidget):
    """MatplotlibWidget"""

    def __init__(self, size=(5.0, 4.0), dpi=100):
        QtGui.QWidget.__init__(self)
        self.fig = Figure(size, dpi=dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.toolbar)
        self.vbox.addWidget(self.canvas)
        self.setLayout(self.vbox)

    def getFigure(self):
        return self.fig

    def draw(self):
        self.canvas.draw()