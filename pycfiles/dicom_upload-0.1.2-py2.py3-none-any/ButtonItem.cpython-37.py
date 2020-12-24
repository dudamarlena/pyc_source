# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ButtonItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1637 bytes
from ..Qt import QtGui, QtCore
from .GraphicsObject import GraphicsObject
__all__ = ['ButtonItem']

class ButtonItem(GraphicsObject):
    """ButtonItem"""
    clicked = QtCore.Signal(object)

    def __init__(self, imageFile=None, width=None, parentItem=None, pixmap=None):
        self.enabled = True
        GraphicsObject.__init__(self)
        if imageFile is not None:
            self.setImageFile(imageFile)
        elif pixmap is not None:
            self.setPixmap(pixmap)
        if width is not None:
            s = float(width) / self.pixmap.width()
            self.scale(s, s)
        if parentItem is not None:
            self.setParentItem(parentItem)
        self.setOpacity(0.7)

    def setImageFile(self, imageFile):
        self.setPixmap(QtGui.QPixmap(imageFile))

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def mouseClickEvent(self, ev):
        if self.enabled:
            self.clicked.emit(self)

    def mouseHoverEvent(self, ev):
        if not self.enabled:
            return
        elif ev.isEnter():
            self.setOpacity(1.0)
        else:
            self.setOpacity(0.7)

    def disable(self):
        self.enabled = False
        self.setOpacity(0.4)

    def enable(self):
        self.enabled = True
        self.setOpacity(0.7)

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        p.drawPixmap(0, 0, self.pixmap)

    def boundingRect(self):
        return QtCore.QRectF(self.pixmap.rect())