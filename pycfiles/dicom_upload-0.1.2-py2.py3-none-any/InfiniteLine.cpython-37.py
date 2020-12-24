# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/InfiniteLine.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 8816 bytes
from ..Qt import QtGui, QtCore
from ..Point import Point
from .GraphicsObject import GraphicsObject
from .. import functions as fn
import numpy as np, weakref
__all__ = [
 'InfiniteLine']

class InfiniteLine(GraphicsObject):
    """InfiniteLine"""
    sigDragged = QtCore.Signal(object)
    sigPositionChangeFinished = QtCore.Signal(object)
    sigPositionChanged = QtCore.Signal(object)

    def __init__(self, pos=None, angle=90, pen=None, movable=False, bounds=None):
        """
        =============== ==================================================================
        **Arguments:**
        pos             Position of the line. This can be a QPointF or a single value for
                        vertical/horizontal lines.
        angle           Angle of line in degrees. 0 is horizontal, 90 is vertical.
        pen             Pen to use when drawing line. Can be any arguments that are valid
                        for :func:`mkPen <pyqtgraph.mkPen>`. Default pen is transparent
                        yellow.
        movable         If True, the line can be dragged to a new position by the user.
        bounds          Optional [min, max] bounding values. Bounds are only valid if the
                        line is vertical or horizontal.
        =============== ==================================================================
        """
        GraphicsObject.__init__(self)
        if bounds is None:
            self.maxRange = [
             None, None]
        else:
            self.maxRange = bounds
        self.moving = False
        self.setMovable(movable)
        self.mouseHovering = False
        self.p = [0, 0]
        self.setAngle(angle)
        if pos is None:
            pos = Point(0, 0)
        self.setPos(pos)
        if pen is None:
            pen = (200, 200, 100)
        self.setPen(pen)
        self.setHoverPen(color=(255, 0, 0), width=(self.pen.width()))
        self.currentPen = self.pen

    def setMovable(self, m):
        """Set whether the line is movable by the user."""
        self.movable = m
        self.setAcceptHoverEvents(m)

    def setBounds(self, bounds):
        """Set the (minimum, maximum) allowable values when dragging."""
        self.maxRange = bounds
        self.setValue(self.value())

    def setPen(self, *args, **kwargs):
        """Set the pen for drawing the line. Allowable arguments are any that are valid 
        for :func:`mkPen <pyqtgraph.mkPen>`."""
        self.pen = (fn.mkPen)(*args, **kwargs)
        if not self.mouseHovering:
            self.currentPen = self.pen
            self.update()

    def setHoverPen(self, *args, **kwargs):
        """Set the pen for drawing the line while the mouse hovers over it. 
        Allowable arguments are any that are valid 
        for :func:`mkPen <pyqtgraph.mkPen>`.
        
        If the line is not movable, then hovering is also disabled.
        
        Added in version 0.9.9."""
        self.hoverPen = (fn.mkPen)(*args, **kwargs)
        if self.mouseHovering:
            self.currentPen = self.hoverPen
            self.update()

    def setAngle(self, angle):
        """
        Takes angle argument in degrees.
        0 is horizontal; 90 is vertical.
        
        Note that the use of value() and setValue() changes if the line is 
        not vertical or horizontal.
        """
        self.angle = (angle + 45) % 180 - 45
        self.resetTransform()
        self.rotate(self.angle)
        self.update()

    def setPos(self, pos):
        if type(pos) in [list, tuple]:
            newPos = pos
        elif isinstance(pos, QtCore.QPointF):
            newPos = [
             pos.x(), pos.y()]
        elif self.angle == 90:
            newPos = [
             pos, 0]
        elif self.angle == 0:
            newPos = [
             0, pos]
        else:
            raise Exception('Must specify 2D coordinate for non-orthogonal lines.')
        if self.angle == 90:
            if self.maxRange[0] is not None:
                newPos[0] = max(newPos[0], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[0] = min(newPos[0], self.maxRange[1])
        elif self.angle == 0:
            if self.maxRange[0] is not None:
                newPos[1] = max(newPos[1], self.maxRange[0])
            if self.maxRange[1] is not None:
                newPos[1] = min(newPos[1], self.maxRange[1])
        if self.p != newPos:
            self.p = newPos
            GraphicsObject.setPos(self, Point(self.p))
            self.update()
            self.sigPositionChanged.emit(self)

    def getXPos(self):
        return self.p[0]

    def getYPos(self):
        return self.p[1]

    def getPos(self):
        return self.p

    def value(self):
        """Return the value of the line. Will be a single number for horizontal and 
        vertical lines, and a list of [x,y] values for diagonal lines."""
        if self.angle % 180 == 0:
            return self.getYPos()
        if self.angle % 180 == 90:
            return self.getXPos()
        return self.getPos()

    def setValue(self, v):
        """Set the position of the line. If line is horizontal or vertical, v can be 
        a single value. Otherwise, a 2D coordinate must be specified (list, tuple and 
        QPointF are all acceptable)."""
        self.setPos(v)

    def boundingRect(self):
        br = self.viewRect()
        px = self.pixelLength(direction=(Point(1, 0)), ortho=True)
        if px is None:
            px = 0
        w = (max(4, self.pen.width() / 2, self.hoverPen.width() / 2) + 1) * px
        br.setBottom(-w)
        br.setTop(w)
        return br.normalized()

    def paint(self, p, *args):
        br = self.boundingRect()
        p.setPen(self.currentPen)
        p.drawLine(Point(br.right(), 0), Point(br.left(), 0))

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == 0:
            return
        return (0, 0)

    def mouseDragEvent(self, ev):
        if self.movable:
            if ev.button() == QtCore.Qt.LeftButton:
                if ev.isStart():
                    self.moving = True
                    self.cursorOffset = self.pos() - self.mapToParent(ev.buttonDownPos())
                    self.startPosition = self.pos()
                else:
                    ev.accept()
                    return self.moving or None
                self.setPos(self.cursorOffset + self.mapToParent(ev.pos()))
                self.sigDragged.emit(self)
                if ev.isFinish():
                    self.moving = False
                    self.sigPositionChangeFinished.emit(self)

    def mouseClickEvent(self, ev):
        if self.moving:
            if ev.button() == QtCore.Qt.RightButton:
                ev.accept()
                self.setPos(self.startPosition)
                self.moving = False
                self.sigDragged.emit(self)
                self.sigPositionChangeFinished.emit(self)

    def hoverEvent(self, ev):
        if not ev.isExit():
            if self.movable and ev.acceptDrags(QtCore.Qt.LeftButton):
                self.setMouseHover(True)
        else:
            self.setMouseHover(False)

    def setMouseHover(self, hover):
        if self.mouseHovering == hover:
            return
        else:
            self.mouseHovering = hover
            if hover:
                self.currentPen = self.hoverPen
            else:
                self.currentPen = self.pen
        self.update()