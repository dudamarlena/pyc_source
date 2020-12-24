# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/GraphicsObject.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1720 bytes
from ..Qt import QtGui, QtCore, USE_PYSIDE
if not USE_PYSIDE:
    import sip
from .GraphicsItem import GraphicsItem
__all__ = [
 'GraphicsObject']

class GraphicsObject(GraphicsItem, QtGui.QGraphicsObject):
    """GraphicsObject"""
    _qtBaseClass = QtGui.QGraphicsObject

    def __init__(self, *args):
        self._GraphicsObject__inform_view_on_changes = True
        (QtGui.QGraphicsObject.__init__)(self, *args)
        self.setFlag(self.ItemSendsGeometryChanges)
        GraphicsItem.__init__(self)

    def itemChange(self, change, value):
        ret = QtGui.QGraphicsObject.itemChange(self, change, value)
        if change in [self.ItemParentHasChanged, self.ItemSceneHasChanged]:
            self.parentChanged()
        try:
            inform_view_on_change = self._GraphicsObject__inform_view_on_changes
        except AttributeError:
            pass
        else:
            if inform_view_on_change:
                if change in [self.ItemPositionHasChanged, self.ItemTransformHasChanged]:
                    self.informViewBoundsChanged()
            elif (USE_PYSIDE or change) == self.ItemParentChange:
                if isinstance(ret, QtGui.QGraphicsItem):
                    ret = sip.cast(ret, QtGui.QGraphicsItem)
            return ret