# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/GraphicsView.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 15354 bytes
__doc__ = '\nGraphicsView.py -   Extension of QGraphicsView\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
from ..Qt import QtCore, QtGui, USE_PYSIDE
try:
    from ..Qt import QtOpenGL
    HAVE_OPENGL = True
except ImportError:
    HAVE_OPENGL = False

from ..Point import Point
import sys, os
from .FileDialog import FileDialog
from ..GraphicsScene import GraphicsScene
import numpy as np
from .. import functions as fn
from .. import debug
from .. import getConfigOption
__all__ = [
 'GraphicsView']

class GraphicsView(QtGui.QGraphicsView):
    """GraphicsView"""
    sigDeviceRangeChanged = QtCore.Signal(object, object)
    sigDeviceTransformChanged = QtCore.Signal(object)
    sigMouseReleased = QtCore.Signal(object)
    sigSceneMouseMoved = QtCore.Signal(object)
    sigScaleChanged = QtCore.Signal(object)
    lastFileDir = None

    def __init__(self, parent=None, useOpenGL=None, background='default'):
        """
        ==============  ============================================================
        **Arguments:**
        parent          Optional parent widget
        useOpenGL       If True, the GraphicsView will use OpenGL to do all of its
                        rendering. This can improve performance on some systems,
                        but may also introduce bugs (the combination of 
                        QGraphicsView and QGLWidget is still an 'experimental' 
                        feature of Qt)
        background      Set the background color of the GraphicsView. Accepts any
                        single argument accepted by 
                        :func:`mkColor <pyqtgraph.mkColor>`. By 
                        default, the background color is determined using the
                        'backgroundColor' configuration option (see 
                        :func:`setConfigOption <pyqtgraph.setConfigOption>`.
        ==============  ============================================================
        """
        self.closed = False
        QtGui.QGraphicsView.__init__(self, parent)
        from .. import _connectCleanup
        _connectCleanup()
        if useOpenGL is None:
            useOpenGL = getConfigOption('useOpenGL')
        self.useOpenGL(useOpenGL)
        self.setCacheMode(self.CacheBackground)
        self.setBackgroundRole(QtGui.QPalette.NoRole)
        self.setBackground(background)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
        self.lockedViewports = []
        self.lastMousePos = None
        self.setMouseTracking(True)
        self.aspectLocked = False
        self.range = QtCore.QRectF(0, 0, 1, 1)
        self.autoPixelRange = True
        self.currentItem = None
        self.clearMouse()
        self.updateMatrix()
        self.sceneObj = GraphicsScene(parent=self)
        self.setScene(self.sceneObj)
        if USE_PYSIDE:
            self.sceneObj._view_ref_workaround = self
        self.centralWidget = None
        self.setCentralItem(QtGui.QGraphicsWidget())
        self.centralLayout = QtGui.QGraphicsGridLayout()
        self.centralWidget.setLayout(self.centralLayout)
        self.mouseEnabled = False
        self.scaleCenter = False
        self.clickAccepted = False

    def setAntialiasing(self, aa):
        """Enable or disable default antialiasing.
        Note that this will only affect items that do not specify their own antialiasing options."""
        if aa:
            self.setRenderHints(self.renderHints() | QtGui.QPainter.Antialiasing)
        else:
            self.setRenderHints(self.renderHints() & ~QtGui.QPainter.Antialiasing)

    def setBackground(self, background):
        """
        Set the background color of the GraphicsView.
        To use the defaults specified py pyqtgraph.setConfigOption, use background='default'.
        To make the background transparent, use background=None.
        """
        self._background = background
        if background == 'default':
            background = getConfigOption('background')
        brush = fn.mkBrush(background)
        self.setBackgroundBrush(brush)

    def paintEvent(self, ev):
        self.scene().prepareForPaint()
        return QtGui.QGraphicsView.paintEvent(self, ev)

    def render(self, *args, **kwds):
        self.scene().prepareForPaint()
        return (QtGui.QGraphicsView.render)(self, *args, **kwds)

    def close(self):
        self.centralWidget = None
        self.scene().clear()
        self.currentItem = None
        self.sceneObj = None
        self.closed = True
        self.setViewport(None)

    def useOpenGL(self, b=True):
        if b:
            if not HAVE_OPENGL:
                raise Exception('Requested to use OpenGL with QGraphicsView, but QtOpenGL module is not available.')
            v = QtOpenGL.QGLWidget()
        else:
            v = QtGui.QWidget()
        self.setViewport(v)

    def keyPressEvent(self, ev):
        self.scene().keyPressEvent(ev)

    def setCentralItem(self, item):
        return self.setCentralWidget(item)

    def setCentralWidget(self, item):
        """Sets a QGraphicsWidget to automatically fill the entire view (the item will be automatically
        resize whenever the GraphicsView is resized)."""
        if self.centralWidget is not None:
            self.scene().removeItem(self.centralWidget)
        self.centralWidget = item
        if item is not None:
            self.sceneObj.addItem(item)
            self.resizeEvent(None)

    def addItem(self, *args):
        return (self.scene().addItem)(*args)

    def removeItem(self, *args):
        return (self.scene().removeItem)(*args)

    def enableMouse(self, b=True):
        self.mouseEnabled = b
        self.autoPixelRange = not b

    def clearMouse(self):
        self.mouseTrail = []
        self.lastButtonReleased = None

    def resizeEvent(self, ev):
        if self.closed:
            return
        if self.autoPixelRange:
            self.range = QtCore.QRectF(0, 0, self.size().width(), self.size().height())
        GraphicsView.setRange(self, (self.range), padding=0, disableAutoPixel=False)
        self.updateMatrix()

    def updateMatrix(self, propagate=True):
        self.setSceneRect(self.range)
        if self.autoPixelRange:
            self.resetTransform()
        elif self.aspectLocked:
            self.fitInView(self.range, QtCore.Qt.KeepAspectRatio)
        else:
            self.fitInView(self.range, QtCore.Qt.IgnoreAspectRatio)
        self.sigDeviceRangeChanged.emit(self, self.range)
        self.sigDeviceTransformChanged.emit(self)
        if propagate:
            for v in self.lockedViewports:
                v.setXRange((self.range), padding=0)

    def viewRect(self):
        """Return the boundaries of the view in scene coordinates"""
        r = QtCore.QRectF(self.rect())
        return self.viewportTransform().inverted()[0].mapRect(r)

    def visibleRange(self):
        return self.viewRect()

    def translate(self, dx, dy):
        self.range.adjust(dx, dy, dx, dy)
        self.updateMatrix()

    def scale(self, sx, sy, center=None):
        scale = [
         sx, sy]
        if self.aspectLocked:
            scale[0] = scale[1]
        if self.scaleCenter:
            center = None
        if center is None:
            center = self.range.center()
        w = self.range.width() / scale[0]
        h = self.range.height() / scale[1]
        self.range = QtCore.QRectF(center.x() - (center.x() - self.range.left()) / scale[0], center.y() - (center.y() - self.range.top()) / scale[1], w, h)
        self.updateMatrix()
        self.sigScaleChanged.emit(self)

    def setRange(self, newRect=None, padding=0.05, lockAspect=None, propagate=True, disableAutoPixel=True):
        if disableAutoPixel:
            self.autoPixelRange = False
        if newRect is None:
            newRect = self.visibleRange()
            padding = 0
        padding = Point(padding)
        newRect = QtCore.QRectF(newRect)
        pw = newRect.width() * padding[0]
        ph = newRect.height() * padding[1]
        newRect = newRect.adjusted(-pw, -ph, pw, ph)
        scaleChanged = False
        if self.range.width() != newRect.width() or self.range.height() != newRect.height():
            scaleChanged = True
        self.range = newRect
        if self.centralWidget is not None:
            self.centralWidget.setGeometry(self.range)
        self.updateMatrix(propagate)
        if scaleChanged:
            self.sigScaleChanged.emit(self)

    def scaleToImage(self, image):
        """Scales such that pixels in image are the same size as screen pixels. This may result in a significant performance increase."""
        pxSize = image.pixelSize()
        image.setPxMode(True)
        try:
            self.sigScaleChanged.disconnect(image.setScaledMode)
        except (TypeError, RuntimeError):
            pass

        tl = image.sceneBoundingRect().topLeft()
        w = self.size().width() * pxSize[0]
        h = self.size().height() * pxSize[1]
        range = QtCore.QRectF(tl.x(), tl.y(), w, h)
        GraphicsView.setRange(self, range, padding=0)
        self.sigScaleChanged.connect(image.setScaledMode)

    def lockXRange(self, v1):
        if v1 not in self.lockedViewports:
            self.lockedViewports.append(v1)

    def setXRange(self, r, padding=0.05):
        r1 = QtCore.QRectF(self.range)
        r1.setLeft(r.left())
        r1.setRight(r.right())
        GraphicsView.setRange(self, r1, padding=[padding, 0], propagate=False)

    def setYRange(self, r, padding=0.05):
        r1 = QtCore.QRectF(self.range)
        r1.setTop(r.top())
        r1.setBottom(r.bottom())
        GraphicsView.setRange(self, r1, padding=[0, padding], propagate=False)

    def wheelEvent(self, ev):
        QtGui.QGraphicsView.wheelEvent(self, ev)
        if not self.mouseEnabled:
            return
        sc = 1.001 ** ev.delta()
        self.scale(sc, sc)

    def setAspectLocked(self, s):
        self.aspectLocked = s

    def leaveEvent(self, ev):
        self.scene().leaveEvent(ev)

    def mousePressEvent(self, ev):
        QtGui.QGraphicsView.mousePressEvent(self, ev)
        if not self.mouseEnabled:
            return
        self.lastMousePos = Point(ev.pos())
        self.mousePressPos = ev.pos()
        self.clickAccepted = ev.isAccepted()
        if not self.clickAccepted:
            self.scene().clearSelection()

    def mouseReleaseEvent(self, ev):
        QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
        if not self.mouseEnabled:
            return
        self.sigMouseReleased.emit(ev)
        self.lastButtonReleased = ev.button()

    def mouseMoveEvent(self, ev):
        if self.lastMousePos is None:
            self.lastMousePos = Point(ev.pos())
        else:
            delta = Point(ev.pos() - self.lastMousePos)
            self.lastMousePos = Point(ev.pos())
            QtGui.QGraphicsView.mouseMoveEvent(self, ev)
            if not self.mouseEnabled:
                return
                self.sigSceneMouseMoved.emit(self.mapToScene(ev.pos()))
                if self.clickAccepted:
                    return
                if ev.buttons() == QtCore.Qt.RightButton:
                    delta = Point(np.clip(delta[0], -50, 50), np.clip(-delta[1], -50, 50))
                    scale = 1.01 ** delta
                    self.scale((scale[0]), (scale[1]), center=(self.mapToScene(self.mousePressPos)))
                    self.sigDeviceRangeChanged.emit(self, self.range)
            elif ev.buttons() in [QtCore.Qt.MidButton, QtCore.Qt.LeftButton]:
                px = self.pixelSize()
                tr = -delta * px
                self.translate(tr[0], tr[1])
                self.sigDeviceRangeChanged.emit(self, self.range)

    def pixelSize(self):
        """Return vector with the length and width of one view pixel in scene coordinates"""
        p0 = Point(0, 0)
        p1 = Point(1, 1)
        tr = self.transform().inverted()[0]
        p01 = tr.map(p0)
        p11 = tr.map(p1)
        return Point(p11 - p01)

    def dragEnterEvent(self, ev):
        ev.ignore()