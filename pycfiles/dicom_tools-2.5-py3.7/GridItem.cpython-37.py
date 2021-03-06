# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/GridItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4550 bytes
from ..Qt import QtGui, QtCore
from .UIGraphicsItem import *
import numpy as np
from ..Point import Point
from .. import functions as fn
__all__ = ['GridItem']

class GridItem(UIGraphicsItem):
    __doc__ = '\n    **Bases:** :class:`UIGraphicsItem <pyqtgraph.UIGraphicsItem>`\n    \n    Displays a rectangular grid of lines indicating major divisions within a coordinate system.\n    Automatically determines what divisions to use.\n    '

    def __init__(self):
        UIGraphicsItem.__init__(self)
        self.picture = None

    def viewRangeChanged(self):
        UIGraphicsItem.viewRangeChanged(self)
        self.picture = None

    def paint(self, p, opt, widget):
        if self.picture is None:
            self.generatePicture()
        p.drawPicture(QtCore.QPointF(0, 0), self.picture)

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter()
        p.begin(self.picture)
        dt = fn.invertQTransform(self.viewTransform())
        vr = self.getViewWidget().rect()
        unit = (self.pixelWidth(), self.pixelHeight())
        dim = [vr.width(), vr.height()]
        lvr = self.boundingRect()
        ul = np.array([lvr.left(), lvr.top()])
        br = np.array([lvr.right(), lvr.bottom()])
        texts = []
        if ul[1] > br[1]:
            x = ul[1]
            ul[1] = br[1]
            br[1] = x
        for i in (2, 1, 0):
            dist = br - ul
            nlTarget = 10.0 ** i
            d = 10.0 ** np.floor(np.log10(abs(dist / nlTarget)) + 0.5)
            ul1 = np.floor(ul / d) * d
            br1 = np.ceil(br / d) * d
            dist = br1 - ul1
            nl = dist / d + 0.5
            for ax in range(0, 2):
                ppl = dim[ax] / nl[ax]
                c = np.clip(3.0 * (ppl - 3), 0.0, 30.0)
                linePen = QtGui.QPen(QtGui.QColor(255, 255, 255, c))
                textPen = QtGui.QPen(QtGui.QColor(255, 255, 255, c * 2))
                bx = (ax + 1) % 2
                for x in range(0, int(nl[ax])):
                    linePen.setCosmetic(False)
                    if ax == 0:
                        linePen.setWidthF(self.pixelWidth())
                    else:
                        linePen.setWidthF(self.pixelHeight())
                    p.setPen(linePen)
                    p1 = np.array([0.0, 0.0])
                    p2 = np.array([0.0, 0.0])
                    p1[ax] = ul1[ax] + x * d[ax]
                    p2[ax] = p1[ax]
                    p1[bx] = ul[bx]
                    p2[bx] = br[bx]
                    if p1[ax] < min(ul[ax], br[ax]) or p1[ax] > max(ul[ax], br[ax]):
                        continue
                    p.drawLine(QtCore.QPointF(p1[0], p1[1]), QtCore.QPointF(p2[0], p2[1]))
                    if i < 2:
                        p.setPen(textPen)
                        if ax == 0:
                            x = p1[0] + unit[0]
                            y = ul[1] + unit[1] * 8.0
                        else:
                            x = ul[0] + unit[0] * 3
                            y = p1[1] + unit[1]
                        texts.append((QtCore.QPointF(x, y), '%g' % p1[ax]))

        tr = self.deviceTransform()
        p.setWorldTransform(fn.invertQTransform(tr))
        for t in texts:
            x = tr.map(t[0]) + Point(0.5, 0.5)
            p.drawText(x, t[1])

        p.end()