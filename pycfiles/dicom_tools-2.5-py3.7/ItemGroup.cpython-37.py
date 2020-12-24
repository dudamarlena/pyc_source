# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ItemGroup.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 546 bytes
from ..Qt import QtGui, QtCore
from .GraphicsObject import GraphicsObject
__all__ = ['ItemGroup']

class ItemGroup(GraphicsObject):
    __doc__ = '\n    Replacement for QGraphicsItemGroup\n    '

    def __init__(self, *args):
        (GraphicsObject.__init__)(self, *args)
        if hasattr(self, 'ItemHasNoContents'):
            self.setFlag(self.ItemHasNoContents)

    def boundingRect(self):
        return QtCore.QRectF()

    def paint(self, *args):
        pass

    def addItem(self, item):
        item.setParentItem(self)