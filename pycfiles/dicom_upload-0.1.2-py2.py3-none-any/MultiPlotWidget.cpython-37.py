# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/MultiPlotWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2985 bytes
__doc__ = '\nMultiPlotWidget.py -  Convenience class--GraphicsView widget displaying a MultiPlotItem\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
from ..Qt import QtCore
from .GraphicsView import GraphicsView
from ..graphicsItems import MultiPlotItem
__all__ = [
 'MultiPlotWidget']

class MultiPlotWidget(GraphicsView):
    """MultiPlotWidget"""

    def __init__(self, parent=None):
        self.minPlotHeight = 50
        self.mPlotItem = MultiPlotItem.MultiPlotItem()
        GraphicsView.__init__(self, parent)
        self.enableMouse(False)
        self.setCentralItem(self.mPlotItem)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

    def __getattr__(self, attr):
        if hasattr(self.mPlotItem, attr):
            m = getattr(self.mPlotItem, attr)
            if hasattr(m, '__call__'):
                return m
        raise AttributeError(attr)

    def setMinimumPlotHeight(self, min):
        """Set the minimum height for each sub-plot displayed. 
        
        If the total height of all plots is greater than the height of the 
        widget, then a scroll bar will appear to provide access to the entire
        set of plots.
        
        Added in version 0.9.9
        """
        self.minPlotHeight = min
        self.resizeEvent(None)

    def widgetGroupInterface(self):
        return (
         None, MultiPlotWidget.saveState, MultiPlotWidget.restoreState)

    def saveState(self):
        return {}

    def restoreState(self, state):
        pass

    def close(self):
        self.mPlotItem.close()
        self.mPlotItem = None
        self.setParent(None)
        GraphicsView.close(self)

    def setRange(self, *args, **kwds):
        (GraphicsView.setRange)(self, *args, **kwds)
        if self.centralWidget is not None:
            r = self.range
            minHeight = len(self.mPlotItem.plots) * self.minPlotHeight
            if r.height() < minHeight:
                r.setHeight(minHeight)
                r.setWidth(r.width() - self.verticalScrollBar().width())
            self.centralWidget.setGeometry(r)

    def resizeEvent(self, ev):
        if self.closed:
            return
        if self.autoPixelRange:
            self.range = QtCore.QRectF(0, 0, self.size().width(), self.size().height())
        MultiPlotWidget.setRange(self, (self.range), padding=0, disableAutoPixel=False)
        self.updateMatrix()