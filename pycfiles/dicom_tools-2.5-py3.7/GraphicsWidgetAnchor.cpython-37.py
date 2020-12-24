# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/GraphicsWidgetAnchor.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4080 bytes
from ..Qt import QtGui, QtCore
from ..Point import Point

class GraphicsWidgetAnchor(object):
    __doc__ = '\n    Class used to allow GraphicsWidgets to anchor to a specific position on their\n    parent. The item will be automatically repositioned if the parent is resized. \n    This is used, for example, to anchor a LegendItem to a corner of its parent \n    PlotItem.\n\n    '

    def __init__(self):
        self._GraphicsWidgetAnchor__parent = None
        self._GraphicsWidgetAnchor__parentAnchor = None
        self._GraphicsWidgetAnchor__itemAnchor = None
        self._GraphicsWidgetAnchor__offset = (0, 0)
        if hasattr(self, 'geometryChanged'):
            self.geometryChanged.connect(self._GraphicsWidgetAnchor__geometryChanged)

    def anchor(self, itemPos, parentPos, offset=(0, 0)):
        """
        Anchors the item at its local itemPos to the item's parent at parentPos.
        Both positions are expressed in values relative to the size of the item or parent;
        a value of 0 indicates left or top edge, while 1 indicates right or bottom edge.
        
        Optionally, offset may be specified to introduce an absolute offset. 
        
        Example: anchor a box such that its upper-right corner is fixed 10px left
        and 10px down from its parent's upper-right corner::
        
            box.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))
        """
        parent = self.parentItem()
        if parent is None:
            raise Exception('Cannot anchor; parent is not set.')
        if self._GraphicsWidgetAnchor__parent is not parent:
            if self._GraphicsWidgetAnchor__parent is not None:
                self._GraphicsWidgetAnchor__parent.geometryChanged.disconnect(self._GraphicsWidgetAnchor__geometryChanged)
            self._GraphicsWidgetAnchor__parent = parent
            parent.geometryChanged.connect(self._GraphicsWidgetAnchor__geometryChanged)
        self._GraphicsWidgetAnchor__itemAnchor = itemPos
        self._GraphicsWidgetAnchor__parentAnchor = parentPos
        self._GraphicsWidgetAnchor__offset = offset
        self._GraphicsWidgetAnchor__geometryChanged()

    def autoAnchor(self, pos, relative=True):
        """
        Set the position of this item relative to its parent by automatically 
        choosing appropriate anchor settings.
        
        If relative is True, one corner of the item will be anchored to 
        the appropriate location on the parent with no offset. The anchored
        corner will be whichever is closest to the parent's boundary.
        
        If relative is False, one corner of the item will be anchored to the same
        corner of the parent, with an absolute offset to achieve the correct
        position. 
        """
        pos = Point(pos)
        br = self.mapRectToParent(self.boundingRect()).translated(pos - self.pos())
        pbr = self.parentItem().boundingRect()
        anchorPos = [0, 0]
        parentPos = Point()
        itemPos = Point()
        if abs(br.left() - pbr.left()) < abs(br.right() - pbr.right()):
            anchorPos[0] = 0
            parentPos[0] = pbr.left()
            itemPos[0] = br.left()
        else:
            anchorPos[0] = 1
            parentPos[0] = pbr.right()
            itemPos[0] = br.right()
        if abs(br.top() - pbr.top()) < abs(br.bottom() - pbr.bottom()):
            anchorPos[1] = 0
            parentPos[1] = pbr.top()
            itemPos[1] = br.top()
        else:
            anchorPos[1] = 1
            parentPos[1] = pbr.bottom()
            itemPos[1] = br.bottom()
        if relative:
            relPos = [
             (itemPos[0] - pbr.left()) / pbr.width(), (itemPos[1] - pbr.top()) / pbr.height()]
            self.anchor(anchorPos, relPos)
        else:
            offset = itemPos - parentPos
            self.anchor(anchorPos, anchorPos, offset)

    def __geometryChanged(self):
        if self._GraphicsWidgetAnchor__parent is None:
            return
        if self._GraphicsWidgetAnchor__itemAnchor is None:
            return
        o = self.mapToParent(Point(0, 0))
        a = self.boundingRect().bottomRight() * Point(self._GraphicsWidgetAnchor__itemAnchor)
        a = self.mapToParent(a)
        p = self._GraphicsWidgetAnchor__parent.boundingRect().bottomRight() * Point(self._GraphicsWidgetAnchor__parentAnchor)
        off = Point(self._GraphicsWidgetAnchor__offset)
        pos = p + (o - a) + off
        self.setPos(pos)