# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsWindows.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2663 bytes
__doc__ = '\ngraphicsWindows.py -  Convenience classes which create a new window with PlotWidget or ImageView.\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
from .Qt import QtCore, QtGui
from .widgets.PlotWidget import *
from .imageview import *
import widgets.GraphicsLayoutWidget as GraphicsLayoutWidget
import widgets.GraphicsView as GraphicsView
QAPP = None

def mkQApp():
    global QAPP
    if QtGui.QApplication.instance() is None:
        QAPP = QtGui.QApplication([])


class GraphicsWindow(GraphicsLayoutWidget):
    """GraphicsWindow"""

    def __init__(self, title=None, size=(800, 600), **kargs):
        mkQApp()
        (GraphicsLayoutWidget.__init__)(self, **kargs)
        (self.resize)(*size)
        if title is not None:
            self.setWindowTitle(title)
        self.show()


class TabWindow(QtGui.QMainWindow):

    def __init__(self, title=None, size=(800, 600)):
        mkQApp()
        QtGui.QMainWindow.__init__(self)
        (self.resize)(*size)
        self.cw = QtGui.QTabWidget()
        self.setCentralWidget(self.cw)
        if title is not None:
            self.setWindowTitle(title)
        self.show()

    def __getattr__(self, attr):
        if hasattr(self.cw, attr):
            return getattr(self.cw, attr)
        raise NameError(attr)


class PlotWindow(PlotWidget):

    def __init__(self, title=None, **kargs):
        mkQApp()
        self.win = QtGui.QMainWindow()
        (PlotWidget.__init__)(self, **kargs)
        self.win.setCentralWidget(self)
        for m in ('resize', ):
            setattr(self, m, getattr(self.win, m))

        if title is not None:
            self.win.setWindowTitle(title)
        self.win.show()


class ImageWindow(ImageView):

    def __init__(self, *args, **kargs):
        mkQApp()
        self.win = QtGui.QMainWindow()
        self.win.resize(800, 600)
        if 'title' in kargs:
            self.win.setWindowTitle(kargs['title'])
            del kargs['title']
        ImageView.__init__(self, self.win)
        if len(args) > 0 or len(kargs) > 0:
            (self.setImage)(*args, **kargs)
        self.win.setCentralWidget(self)
        for m in ('resize', ):
            setattr(self, m, getattr(self.win, m))

        self.win.show()