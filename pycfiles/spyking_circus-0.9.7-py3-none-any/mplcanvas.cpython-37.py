# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/shared/mplcanvas.py
# Compiled at: 2020-03-11 05:17:13
# Size of source mod 2**32: 1436 bytes
try:
    from PyQt5 import QtGui, uic, QtCore
    import matplotlib.backends.backend_qt5agg as FigureCanvas
except ImportError:
    from PyQt4 import QtGui, uic, QtCore
    import matplotlib.backends.backend_qt4agg as FigureCanvas

from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

class MplCanvas(FigureCanvas):
    __doc__ = 'Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).'

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        rcParams['axes.labelsize'] = 'small'
        rcParams['xtick.labelsize'] = 'small'
        rcParams['ytick.labelsize'] = 'small'
        self.axes = fig.add_axes([0.15, 0.15, 0.85, 0.85])
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        fig.patch.set_alpha(0)

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()
        padding = 7.5 * FontProperties(size=(rcParams['axes.labelsize'])).get_size_in_points()
        posx = padding / w
        posy = padding / h
        self.axes.set_position([posx, posy, 0.97 - posx, 0.97 - posy])
        super(MplCanvas, self).resizeEvent(event)