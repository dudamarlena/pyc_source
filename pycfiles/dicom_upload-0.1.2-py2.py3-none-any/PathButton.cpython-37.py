# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/PathButton.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1556 bytes
from ..Qt import QtGui, QtCore
from .. import functions as fn
__all__ = ['PathButton']

class PathButton(QtGui.QPushButton):
    """PathButton"""

    def __init__(self, parent=None, path=None, pen='default', brush=None, size=(30, 30)):
        QtGui.QPushButton.__init__(self, parent)
        self.path = None
        if pen == 'default':
            pen = 'k'
        self.setPen(pen)
        self.setBrush(brush)
        if path is not None:
            self.setPath(path)
        if size is not None:
            self.setFixedWidth(size[0])
            self.setFixedHeight(size[1])

    def setBrush(self, brush):
        self.brush = fn.mkBrush(brush)

    def setPen(self, *args, **kwargs):
        self.pen = (fn.mkPen)(*args, **kwargs)

    def setPath(self, path):
        self.path = path
        self.update()

    def paintEvent(self, ev):
        QtGui.QPushButton.paintEvent(self, ev)
        margin = 7
        geom = QtCore.QRectF(0, 0, self.width(), self.height()).adjusted(margin, margin, -margin, -margin)
        rect = self.path.boundingRect()
        scale = min(geom.width() / float(rect.width()), geom.height() / float(rect.height()))
        p = QtGui.QPainter(self)
        p.setRenderHint(p.Antialiasing)
        p.translate(geom.center())
        p.scale(scale, scale)
        p.translate(-rect.center())
        p.setPen(self.pen)
        p.setBrush(self.brush)
        p.drawPath(self.path)
        p.end()