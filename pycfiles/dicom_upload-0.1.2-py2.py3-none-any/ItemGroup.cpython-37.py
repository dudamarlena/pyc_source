# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ItemGroup.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 546 bytes
from ..Qt import QtGui, QtCore
from .GraphicsObject import GraphicsObject
__all__ = ['ItemGroup']

class ItemGroup(GraphicsObject):
    """ItemGroup"""

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