# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/LegendItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 6755 bytes
from .GraphicsWidget import GraphicsWidget
from .LabelItem import LabelItem
from ..Qt import QtGui, QtCore
from .. import functions as fn
from ..Point import Point
from .ScatterPlotItem import ScatterPlotItem, drawSymbol
from .PlotDataItem import PlotDataItem
from .GraphicsWidgetAnchor import GraphicsWidgetAnchor
__all__ = [
 'LegendItem']

class LegendItem(GraphicsWidget, GraphicsWidgetAnchor):
    """LegendItem"""

    def __init__(self, size=None, offset=None):
        """
        ==============  ===============================================================
        **Arguments:**
        size            Specifies the fixed size (width, height) of the legend. If
                        this argument is omitted, the legend will autimatically resize
                        to fit its contents.
        offset          Specifies the offset position relative to the legend's parent.
                        Positive values offset from the left or top; negative values
                        offset from the right or bottom. If offset is None, the
                        legend must be anchored manually by calling anchor() or
                        positioned by calling setPos().
        ==============  ===============================================================
        
        """
        GraphicsWidget.__init__(self)
        GraphicsWidgetAnchor.__init__(self)
        self.setFlag(self.ItemIgnoresTransformations)
        self.layout = QtGui.QGraphicsGridLayout()
        self.setLayout(self.layout)
        self.items = []
        self.size = size
        self.offset = offset
        if size is not None:
            self.setGeometry(QtCore.QRectF(0, 0, self.size[0], self.size[1]))

    def setParentItem(self, p):
        ret = GraphicsWidget.setParentItem(self, p)
        if self.offset is not None:
            offset = Point(self.offset)
            anchorx = 1 if offset[0] <= 0 else 0
            anchory = 1 if offset[1] <= 0 else 0
            anchor = (anchorx, anchory)
            self.anchor(itemPos=anchor, parentPos=anchor, offset=offset)
        return ret

    def addItem(self, item, name):
        """
        Add a new entry to the legend. 

        ==============  ========================================================
        **Arguments:**
        item            A PlotDataItem from which the line and point style
                        of the item will be determined or an instance of
                        ItemSample (or a subclass), allowing the item display
                        to be customized.
        title           The title to display for this item. Simple HTML allowed.
        ==============  ========================================================
        """
        label = LabelItem(name)
        if isinstance(item, ItemSample):
            sample = item
        else:
            sample = ItemSample(item)
        row = self.layout.rowCount()
        self.items.append((sample, label))
        self.layout.addItem(sample, row, 0)
        self.layout.addItem(label, row, 1)
        self.updateSize()

    def removeItem(self, name):
        """
        Removes one item from the legend. 

        ==============  ========================================================
        **Arguments:**
        title           The title displayed for this item.
        ==============  ========================================================
        """
        for sample, label in self.items:
            if label.text == name:
                self.items.remove((sample, label))
                self.layout.removeItem(sample)
                sample.close()
                self.layout.removeItem(label)
                label.close()
                self.updateSize()

    def updateSize(self):
        if self.size is not None:
            return
        height = 0
        width = 0
        for sample, label in self.items:
            height += max(sample.height(), label.height()) + 3
            width = max(width, sample.width() + label.width())

        self.setGeometry(0, 0, width + 25, height)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width(), self.height())

    def paint(self, p, *args):
        p.setPen(fn.mkPen(255, 255, 255, 100))
        p.setBrush(fn.mkBrush(100, 100, 100, 50))
        p.drawRect(self.boundingRect())

    def hoverEvent(self, ev):
        ev.acceptDrags(QtCore.Qt.LeftButton)

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            dpos = ev.pos() - ev.lastPos()
            self.autoAnchor(self.pos() + dpos)


class ItemSample(GraphicsWidget):
    """ItemSample"""

    def __init__(self, item):
        GraphicsWidget.__init__(self)
        self.item = item

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 20, 20)

    def paint(self, p, *args):
        opts = self.item.opts
        if opts.get('fillLevel', None) is not None:
            if opts.get('fillBrush', None) is not None:
                p.setBrush(fn.mkBrush(opts['fillBrush']))
                p.setPen(fn.mkPen(None))
                p.drawPolygon(QtGui.QPolygonF([QtCore.QPointF(2, 18), QtCore.QPointF(18, 2), QtCore.QPointF(18, 18)]))
        if not isinstance(self.item, ScatterPlotItem):
            p.setPen(fn.mkPen(opts['pen']))
            p.drawLine(2, 18, 18, 2)
        symbol = opts.get('symbol', None)
        if symbol is not None:
            if isinstance(self.item, PlotDataItem):
                opts = self.item.scatter.opts
            pen = fn.mkPen(opts['pen'])
            brush = fn.mkBrush(opts['brush'])
            size = opts['size']
            p.translate(10, 10)
            path = drawSymbol(p, symbol, size, pen, brush)