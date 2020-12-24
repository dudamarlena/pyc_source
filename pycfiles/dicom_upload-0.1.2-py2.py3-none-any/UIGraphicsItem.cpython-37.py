# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/UIGraphicsItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4668 bytes
from ..Qt import QtGui, QtCore, USE_PYSIDE
import weakref
from .GraphicsObject import GraphicsObject
if not USE_PYSIDE:
    import sip
__all__ = [
 'UIGraphicsItem']

class UIGraphicsItem(GraphicsObject):
    """UIGraphicsItem"""

    def __init__(self, bounds=None, parent=None):
        """
        ============== =============================================================================
        **Arguments:**
        bounds         QRectF with coordinates relative to view box. The default is QRectF(0,0,1,1),
                       which means the item will have the same bounds as the view.
        ============== =============================================================================
        """
        GraphicsObject.__init__(self, parent)
        self.setFlag(self.ItemSendsScenePositionChanges)
        if bounds is None:
            self._bounds = QtCore.QRectF(0, 0, 1, 1)
        else:
            self._bounds = bounds
        self._boundingRect = None
        self._updateView()

    def paint(self, *args):
        pass

    def itemChange(self, change, value):
        ret = GraphicsObject.itemChange(self, change, value)
        if not USE_PYSIDE:
            if change == self.ItemParentChange:
                if isinstance(ret, QtGui.QGraphicsItem):
                    ret = sip.cast(ret, QtGui.QGraphicsItem)
        if change == self.ItemScenePositionHasChanged:
            self.setNewBounds()
        return ret

    def boundingRect(self):
        if self._boundingRect is None:
            br = self.viewRect()
            if br is None:
                return QtCore.QRectF()
            self._boundingRect = br
        return QtCore.QRectF(self._boundingRect)

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        """Called by ViewBox for determining the auto-range bounds.
        By default, UIGraphicsItems are excluded from autoRange."""
        pass

    def viewRangeChanged(self):
        """Called when the view widget/viewbox is resized/rescaled"""
        self.setNewBounds()
        self.update()

    def setNewBounds(self):
        """Update the item's bounding rect to match the viewport"""
        self._boundingRect = None
        self.prepareGeometryChange()

    def setPos(self, *args):
        (GraphicsObject.setPos)(self, *args)
        self.setNewBounds()

    def mouseShape(self):
        """Return the shape of this item after expanding by 2 pixels"""
        shape = self.shape()
        ds = self.mapToDevice(shape)
        stroker = QtGui.QPainterPathStroker()
        stroker.setWidh(2)
        ds2 = stroker.createStroke(ds).united(ds)
        return self.mapFromDevice(ds2)