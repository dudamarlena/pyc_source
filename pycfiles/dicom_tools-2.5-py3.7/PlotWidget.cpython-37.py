# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/PlotWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4077 bytes
"""
PlotWidget.py -  Convenience class--GraphicsView widget displaying a single PlotItem
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""
from ..Qt import QtCore, QtGui
from .GraphicsView import *
from ..graphicsItems.PlotItem import *
__all__ = [
 'PlotWidget']

class PlotWidget(GraphicsView):
    sigRangeChanged = QtCore.Signal(object, object)
    sigTransformChanged = QtCore.Signal(object)

    def __init__(self, parent=None, background='default', **kargs):
        """When initializing PlotWidget, *parent* and *background* are passed to 
        :func:`GraphicsWidget.__init__() <pyqtgraph.GraphicsWidget.__init__>`
        and all others are passed
        to :func:`PlotItem.__init__() <pyqtgraph.PlotItem.__init__>`."""
        GraphicsView.__init__(self, parent, background=background)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.enableMouse(False)
        self.plotItem = PlotItem(**kargs)
        self.setCentralItem(self.plotItem)
        for m in ('addItem', 'removeItem', 'autoRange', 'clear', 'setXRange', 'setYRange',
                  'setRange', 'setAspectLocked', 'setMouseEnabled', 'setXLink', 'setYLink',
                  'enableAutoRange', 'disableAutoRange', 'setLimits', 'register',
                  'unregister', 'viewRect'):
            setattr(self, m, getattr(self.plotItem, m))

        self.plotItem.sigRangeChanged.connect(self.viewRangeChanged)

    def close(self):
        self.plotItem.close()
        self.plotItem = None
        self.setParent(None)
        GraphicsView.close(self)

    def __getattr__(self, attr):
        if hasattr(self.plotItem, attr):
            m = getattr(self.plotItem, attr)
            if hasattr(m, '__call__'):
                return m
        raise NameError(attr)

    def viewRangeChanged(self, view, range):
        self.sigRangeChanged.emit(self, range)

    def widgetGroupInterface(self):
        return (
         None, PlotWidget.saveState, PlotWidget.restoreState)

    def saveState(self):
        return self.plotItem.saveState()

    def restoreState(self, state):
        return self.plotItem.restoreState(state)

    def getPlotItem(self):
        """Return the PlotItem contained within."""
        return self.plotItem