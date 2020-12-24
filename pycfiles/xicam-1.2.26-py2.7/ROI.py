# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\ROI.py
# Compiled at: 2018-08-27 17:21:07
import pyqtgraph as pg
from PySide import QtGui, QtCore
import numpy as np

class QCircRectF(QtCore.QRectF):

    def __init__(self, center=(0, 0), radius=1, rect=None):
        self._scale = 1.0
        if rect is not None:
            self.center = rect.center()
            super(QCircRectF, self).__init__(rect)
        else:
            self.center = QtCore.QPointF(*center)
            left = self.center.x() - radius
            top = self.center.y() - radius
            bottom = self.center.y() + radius
            right = self.center.x() + radius
            super(QCircRectF, self).__init__(QtCore.QPointF(left, top), QtCore.QPointF(right, bottom))
        return

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.radius *= value
        self.setLeft(self.center.x() - self._radius)
        self.setTop(self.center.y() - self._radius)
        self.setBottom(self.center.y() + self._radius)
        self.setRight(self.center.x() + self._radius)

    @property
    def radius(self):
        return (self.right() - self.left()) * 0.5

    @radius.setter
    def radius(self, radius):
        self.setLeft(self.center.x() - radius)
        self.setTop(self.center.y() - radius)
        self.setBottom(self.center.y() + radius)
        self.setRight(self.center.x() + radius)


class QRectF(QtCore.QRectF):

    def scale(self, ratio):
        coords = [ coord * ratio for coord in self.getCoords() ]
        self.setCoords(*coords)


class LinearRegionItem(pg.LinearRegionItem):
    sigRemoveRequested = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(LinearRegionItem, self).__init__(*args, **kwargs)
        self.menu = None
        self.isdeleting = False
        return

    def getArrayRegion(self, data, item):
        cut = np.zeros_like(data)
        if self.orientation is pg.LinearRegionItem.Horizontal:
            regionbounds = self.getRegion()
            cut[:, int(regionbounds[0]):int(regionbounds[1])] = 1
        elif self.orientation is pg.LinearRegionItem.Vertical:
            regionbounds = self.getRegion()
            cut[int(regionbounds[0]):int(regionbounds[1]), :] = 1
        return (cut * data).T

    def hoverEvent(self, ev):
        hover = False
        if not ev.isExit():
            if ev.acceptDrags(QtCore.Qt.LeftButton):
                hover = True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True

            ev.acceptClicks(QtCore.Qt.RightButton)
        if hover:
            self.setMouseHover(True)
            ev.acceptClicks(QtCore.Qt.LeftButton)
            ev.acceptClicks(QtCore.Qt.RightButton)
            ev.acceptClicks(QtCore.Qt.MidButton)
        else:
            self.setMouseHover(False)

    def raiseContextMenu(self, ev):
        menu = self.getMenu()
        menu = self.scene().addParentContextMenus(self, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.raiseContextMenu(ev)
            ev.accept()
        elif int(ev.button() & self.acceptedMouseButtons()) > 0:
            ev.accept()
            self.sigClicked.emit(self, ev)
        else:
            ev.ignore()

    def getMenu(self):
        if self.menu is None:
            self.menu = QtGui.QMenu()
            self.menu.setTitle('ROI')
            remAct = QtGui.QAction('Remove ROI', self.menu)
            remAct.triggered.connect(self.removeClicked)
            self.menu.addAction(remAct)
            self.menu.remAct = remAct
        return self.menu

    def removeClicked(self):
        self.isdeleting = True
        QtCore.QTimer.singleShot(0, lambda : self.sigRemoveRequested.emit(self))


class LineROI(pg.LineROI):

    def __init__(self, *args, **kwargs):
        super(LineROI, self).__init__(*args, **kwargs)
        self.isdeleting = False
        self.sigRemoveRequested.connect(self.delete)

    def getArrayRegion(self, data, img, axes=(0, 1), returnMappedCoords=False, **kwds):
        from skimage.draw import polygon
        shape, v, origin = self.getAffineSliceParams(data, img, axes)
        br = np.add(origin, np.multiply(v[0], shape[0]))
        tl = np.add(origin, np.multiply(v[1], shape[1]))
        bl = origin
        tr = np.sum([origin, np.multiply(v[1], shape[1]), np.multiply(v[0], shape[0])], axis=0)
        vecs = np.vstack([bl, br, tr, tl]).T
        rr, cc = polygon(vecs[0], vecs[1])
        mask = np.zeros_like(data)
        rrcc = [ [r, c] for r, c in zip(rr, cc) if r < mask.shape[0] and c < mask.shape[1] ]
        rr, cc = zip(*rrcc)
        mask[(rr, cc)] = 1
        return (data * mask).T.copy()

    def delete(self):
        self.isdeleting = True


class ArcROI(pg.ROI):
    r"""
    Elliptical ROI subclass with one scale handle and one rotation handle.

    ============== =============================================================
    **Arguments**
    pos            (length-2 sequence) The position of the ROI's origin.
    size           (length-2 sequence) The size of the ROI's bounding rectangle.
    \**args        All extra keyword arguments are passed to ROI()
    ============== =============================================================

    """

    def __init__(self, center, radius, **args):
        r = QCircRectF(center, radius)
        super(ArcROI, self).__init__(r.center, r.size(), removable=True, **args)
        self.innerhandle = self.addFreeHandle([0.0, 0.25])
        self.outerhandle = self.addFreeHandle([0.0, 0.5])
        self.lefthandle = self.addFreeHandle([0.433, 0.25])
        self.righthandle = self.addFreeHandle([-0.433, 0.25])
        self.startangle = 30
        self.arclength = 120
        self.aspectLocked = True
        self.translatable = False
        self.translateSnap = False
        self.removable = True
        self.cacheinner = self.innerhandle.pos()
        self.cacheouter = self.outerhandle.pos()
        self.startradius = radius
        self.startcenter = center
        self.isdeleting = False
        self.sigRemoveRequested.connect(self.delete)

    def getRadius(self):
        radius = pg.Point(self.outerhandle.pos()).length()
        return radius

    def getInnerRadius(self):
        radius = pg.Point(self.innerhandle.pos()).length()
        return radius / self.getRadius() * 0.5

    def boundingRect(self):
        r = self.getRadius()
        return QtCore.QRectF(-r * 1.0, -r * 1.0, 2.0 * r, 2.0 * r)

    def getCenter(self):
        r = self.boundingRect()
        r = QCircRectF(rect=r)
        return r.center

    def paint(self, p, opt, widget):
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 255, 255))
        p.setPen(pen)
        r = self.boundingRect()
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.scale(r.width(), r.height())
        r = QCircRectF(radius=0.5)
        self.arclength = np.degrees(np.arctan2(self.lefthandle.pos().x(), self.lefthandle.pos().y()) - np.arctan2(self.righthandle.pos().x(), self.righthandle.pos().y()))
        self.startangle = np.degrees(np.arctan2(self.lefthandle.pos().y(), self.lefthandle.pos().x()))
        p.drawArc(r, -self.startangle * 16, -self.arclength * 16)
        radius = self.getInnerRadius()
        r = QCircRectF()
        r.radius = radius
        p.drawArc(r, -self.startangle * 16, -self.arclength * 16)
        pen.setStyle(QtCore.Qt.DashLine)
        p.setPen(pen)
        p.drawLine(QtCore.QPointF(0.0, 0.0), self.lefthandle.pos() * 100)
        p.drawLine(QtCore.QPointF(0.0, 0.0), self.righthandle.pos() * 100)

    def getArrayRegion(self, arr, img=None):
        """
        Return the result of ROI.getArrayRegion() masked by the elliptical shape
        of the ROI. Regions outside the ellipse are set to 0.
        """
        w = arr.shape[0]
        h = arr.shape[1]
        mask = np.fromfunction(lambda x, y: (self.innerhandle.pos().length() < ((x - self.startcenter[0]) ** 2.0 + (y - self.startcenter[1]) ** 2.0) ** 0.5) & (((x - self.startcenter[0]) ** 2.0 + (y - self.startcenter[1]) ** 2.0) ** 0.5 < self.outerhandle.pos().length()) & ((np.degrees(np.arctan2(y - self.startcenter[1], x - self.startcenter[0])) - self.startangle) % 360 > 0) & ((np.degrees(np.arctan2(y - self.startcenter[1], x - self.startcenter[0])) - self.startangle) % 360 < self.arclength), (
         w, h))
        return (arr * mask).T

    def shape(self):
        self.path = QtGui.QPainterPath()
        self.path.addEllipse(self.boundingRect())
        return self.path

    def delete(self):
        self.isdeleting = True