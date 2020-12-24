# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/dockarea/DockDrop.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4087 bytes
from ..Qt import QtCore, QtGui

class DockDrop(object):
    """DockDrop"""

    def __init__(self, allowedAreas=None):
        object.__init__(self)
        if allowedAreas is None:
            allowedAreas = [
             'center', 'right', 'left', 'top', 'bottom']
        self.allowedAreas = set(allowedAreas)
        self.setAcceptDrops(True)
        self.dropArea = None
        self.overlay = DropAreaOverlay(self)
        self.overlay.raise_()

    def resizeOverlay(self, size):
        self.overlay.resize(size)

    def raiseOverlay(self):
        self.overlay.raise_()

    def dragEnterEvent(self, ev):
        src = ev.source()
        if hasattr(src, 'implements') and src.implements('dock'):
            ev.accept()
        else:
            ev.ignore()

    def dragMoveEvent(self, ev):
        ld = ev.pos().x()
        rd = self.width() - ld
        td = ev.pos().y()
        bd = self.height() - td
        mn = min(ld, rd, td, bd)
        if mn > 30:
            self.dropArea = 'center'
        elif ld == mn or td == mn:
            if mn > self.height() / 3.0:
                self.dropArea = 'center'
        elif rd == mn or ld == mn:
            if mn > self.width() / 3.0:
                self.dropArea = 'center'
        elif rd == mn:
            self.dropArea = 'right'
        elif ld == mn:
            self.dropArea = 'left'
        elif td == mn:
            self.dropArea = 'top'
        elif bd == mn:
            self.dropArea = 'bottom'
        if ev.source() is self and self.dropArea == 'center':
            self.dropArea = None
            ev.ignore()
        elif self.dropArea not in self.allowedAreas:
            self.dropArea = None
            ev.ignore()
        else:
            ev.accept()
        self.overlay.setDropArea(self.dropArea)

    def dragLeaveEvent(self, ev):
        self.dropArea = None
        self.overlay.setDropArea(self.dropArea)

    def dropEvent(self, ev):
        area = self.dropArea
        if area is None:
            return
        if area == 'center':
            area = 'above'
        self.area.moveDock(ev.source(), area, self)
        self.dropArea = None
        self.overlay.setDropArea(self.dropArea)


class DropAreaOverlay(QtGui.QWidget):
    """DropAreaOverlay"""

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.dropArea = None
        self.hide()
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def setDropArea(self, area):
        self.dropArea = area
        if area is None:
            self.hide()
        else:
            prgn = self.parent().rect()
            rgn = QtCore.QRect(prgn)
            w = min(30, prgn.width() / 3.0)
            h = min(30, prgn.height() / 3.0)
            if self.dropArea == 'left':
                rgn.setWidth(w)
            elif self.dropArea == 'right':
                rgn.setLeft(rgn.left() + prgn.width() - w)
            elif self.dropArea == 'top':
                rgn.setHeight(h)
            elif self.dropArea == 'bottom':
                rgn.setTop(rgn.top() + prgn.height() - h)
            elif self.dropArea == 'center':
                rgn.adjust(w, h, -w, -h)
            self.setGeometry(rgn)
            self.show()
        self.update()

    def paintEvent(self, ev):
        if self.dropArea is None:
            return
        p = QtGui.QPainter(self)
        rgn = self.rect()
        p.setBrush(QtGui.QBrush(QtGui.QColor(100, 100, 255, 50)))
        p.setPen(QtGui.QPen(QtGui.QColor(50, 50, 150), 3))
        p.drawRect(rgn)