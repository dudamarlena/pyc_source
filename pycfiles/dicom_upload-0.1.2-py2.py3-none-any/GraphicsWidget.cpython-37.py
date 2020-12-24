# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/GraphicsWidget.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2151 bytes
from ..Qt import QtGui, QtCore
from ..GraphicsScene import GraphicsScene
from .GraphicsItem import GraphicsItem
__all__ = ['GraphicsWidget']

class GraphicsWidget(GraphicsItem, QtGui.QGraphicsWidget):
    _qtBaseClass = QtGui.QGraphicsWidget

    def __init__(self, *args, **kargs):
        """
        **Bases:** :class:`GraphicsItem <pyqtgraph.GraphicsItem>`, :class:`QtGui.QGraphicsWidget`
        
        Extends QGraphicsWidget with several helpful methods and workarounds for PyQt bugs. 
        Most of the extra functionality is inherited from :class:`GraphicsItem <pyqtgraph.GraphicsItem>`.
        """
        (QtGui.QGraphicsWidget.__init__)(self, *args, **kargs)
        GraphicsItem.__init__(self)

    def setFixedHeight(self, h):
        self.setMaximumHeight(h)
        self.setMinimumHeight(h)

    def setFixedWidth(self, h):
        self.setMaximumWidth(h)
        self.setMinimumWidth(h)

    def height(self):
        return self.geometry().height()

    def width(self):
        return self.geometry().width()

    def boundingRect(self):
        br = self.mapRectFromParent(self.geometry()).normalized()
        return br

    def shape(self):
        p = QtGui.QPainterPath()
        p.addRect(self.boundingRect())
        return p