# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ScaleBar.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2287 bytes
from ..Qt import QtGui, QtCore
from .GraphicsObject import *
from .GraphicsWidgetAnchor import *
from .TextItem import TextItem
import numpy as np
from .. import functions as fn
from .. import getConfigOption
from ..Point import Point
__all__ = ['ScaleBar']

class ScaleBar(GraphicsObject, GraphicsWidgetAnchor):
    """ScaleBar"""

    def __init__(self, size, width=5, brush=None, pen=None, suffix='m', offset=None):
        GraphicsObject.__init__(self)
        GraphicsWidgetAnchor.__init__(self)
        self.setFlag(self.ItemHasNoContents)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        if brush is None:
            brush = getConfigOption('foreground')
        self.brush = fn.mkBrush(brush)
        self.pen = fn.mkPen(pen)
        self._width = width
        self.size = size
        if offset == None:
            offset = (0, 0)
        self.offset = offset
        self.bar = QtGui.QGraphicsRectItem()
        self.bar.setPen(self.pen)
        self.bar.setBrush(self.brush)
        self.bar.setParentItem(self)
        self.text = TextItem(text=fn.siFormat(size, suffix=suffix), anchor=(0.5, 1))
        self.text.setParentItem(self)

    def parentChanged(self):
        view = self.parentItem()
        if view is None:
            return
        view.sigRangeChanged.connect(self.updateBar)
        self.updateBar()

    def updateBar(self):
        view = self.parentItem()
        if view is None:
            return
        p1 = view.mapFromViewToItem(self, QtCore.QPointF(0, 0))
        p2 = view.mapFromViewToItem(self, QtCore.QPointF(self.size, 0))
        w = (p2 - p1).x()
        self.bar.setRect(QtCore.QRectF(-w, 0, w, self._width))
        self.text.setPos(-w / 2.0, 0)

    def boundingRect(self):
        return QtCore.QRectF()

    def setParentItem(self, p):
        ret = GraphicsObject.setParentItem(self, p)
        if self.offset is not None:
            offset = Point(self.offset)
            anchorx = 1 if offset[0] <= 0 else 0
            anchory = 1 if offset[1] <= 0 else 0
            anchor = (anchorx, anchory)
            self.anchor(itemPos=anchor, parentPos=anchor, offset=offset)
        return ret