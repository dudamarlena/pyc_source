# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/LinearRegionItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 11082 bytes
from ..Qt import QtGui, QtCore
from .UIGraphicsItem import UIGraphicsItem
from .InfiniteLine import InfiniteLine
from .. import functions as fn
from .. import debug
__all__ = ['LinearRegionItem']

class LinearRegionItem(UIGraphicsItem):
    __doc__ = '\n    **Bases:** :class:`UIGraphicsItem <pyqtgraph.UIGraphicsItem>`\n    \n    Used for marking a horizontal or vertical region in plots.\n    The region can be dragged and is bounded by lines which can be dragged individually.\n    \n    ===============================  =============================================================================\n    **Signals:**\n    sigRegionChangeFinished(self)    Emitted when the user has finished dragging the region (or one of its lines)\n                                     and when the region is changed programatically.\n    sigRegionChanged(self)           Emitted while the user is dragging the region (or one of its lines)\n                                     and when the region is changed programatically.\n    ===============================  =============================================================================\n    '
    sigRegionChangeFinished = QtCore.Signal(object)
    sigRegionChanged = QtCore.Signal(object)
    Vertical = 0
    Horizontal = 1

    def __init__(self, values=[
 0, 1], orientation=None, brush=None, movable=True, bounds=None):
        """Create a new LinearRegionItem.
        
        ==============  =====================================================================
        **Arguments:**
        values          A list of the positions of the lines in the region. These are not
                        limits; limits can be set by specifying bounds.
        orientation     Options are LinearRegionItem.Vertical or LinearRegionItem.Horizontal.
                        If not specified it will be vertical.
        brush           Defines the brush that fills the region. Can be any arguments that
                        are valid for :func:`mkBrush <pyqtgraph.mkBrush>`. Default is
                        transparent blue.
        movable         If True, the region and individual lines are movable by the user; if
                        False, they are static.
        bounds          Optional [min, max] bounding values for the region
        ==============  =====================================================================
        """
        UIGraphicsItem.__init__(self)
        if orientation is None:
            orientation = LinearRegionItem.Vertical
        else:
            self.orientation = orientation
            self.bounds = QtCore.QRectF()
            self.blockLineSignal = False
            self.moving = False
            self.mouseHovering = False
            if orientation == LinearRegionItem.Horizontal:
                self.lines = [InfiniteLine((QtCore.QPointF(0, values[0])), 0, movable=movable, bounds=bounds),
                 InfiniteLine((QtCore.QPointF(0, values[1])), 0, movable=movable, bounds=bounds)]
            else:
                if orientation == LinearRegionItem.Vertical:
                    self.lines = [InfiniteLine((QtCore.QPointF(values[1], 0)), 90, movable=movable, bounds=bounds),
                     InfiniteLine((QtCore.QPointF(values[0], 0)), 90, movable=movable, bounds=bounds)]
                else:
                    raise Exception('Orientation must be one of LinearRegionItem.Vertical or LinearRegionItem.Horizontal')
        for l in self.lines:
            l.setParentItem(self)
            l.sigPositionChangeFinished.connect(self.lineMoveFinished)
            l.sigPositionChanged.connect(self.lineMoved)

        if brush is None:
            brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 50))
        self.setBrush(brush)
        self.setMovable(movable)

    def getRegion(self):
        """Return the values at the edges of the region."""
        r = [
         self.lines[0].value(), self.lines[1].value()]
        return (min(r), max(r))

    def setRegion(self, rgn):
        """Set the values for the edges of the region.
        
        ==============   ==============================================
        **Arguments:**
        rgn              A list or tuple of the lower and upper values.
        ==============   ==============================================
        """
        if self.lines[0].value() == rgn[0]:
            if self.lines[1].value() == rgn[1]:
                return
        self.blockLineSignal = True
        self.lines[0].setValue(rgn[0])
        self.blockLineSignal = False
        self.lines[1].setValue(rgn[1])
        self.lineMoved()
        self.lineMoveFinished()

    def setBrush(self, *br, **kargs):
        """Set the brush that fills the region. Can have any arguments that are valid
        for :func:`mkBrush <pyqtgraph.mkBrush>`.
        """
        self.brush = (fn.mkBrush)(*br, **kargs)
        self.currentBrush = self.brush

    def setBounds(self, bounds):
        """Optional [min, max] bounding values for the region. To have no bounds on the
        region use [None, None].
        Does not affect the current position of the region unless it is outside the new bounds. 
        See :func:`setRegion <pyqtgraph.LinearRegionItem.setRegion>` to set the position 
        of the region."""
        for l in self.lines:
            l.setBounds(bounds)

    def setMovable(self, m):
        """Set lines to be movable by the user, or not. If lines are movable, they will 
        also accept HoverEvents."""
        for l in self.lines:
            l.setMovable(m)

        self.movable = m
        self.setAcceptHoverEvents(m)

    def boundingRect(self):
        br = UIGraphicsItem.boundingRect(self)
        rng = self.getRegion()
        if self.orientation == LinearRegionItem.Vertical:
            br.setLeft(rng[0])
            br.setRight(rng[1])
        else:
            br.setTop(rng[0])
            br.setBottom(rng[1])
        return br.normalized()

    def paint(self, p, *args):
        profiler = debug.Profiler()
        (UIGraphicsItem.paint)(self, p, *args)
        p.setBrush(self.currentBrush)
        p.setPen(fn.mkPen(None))
        p.drawRect(self.boundingRect())

    def dataBounds(self, axis, frac=1.0, orthoRange=None):
        if axis == self.orientation:
            return self.getRegion()
        return

    def lineMoved(self):
        if self.blockLineSignal:
            return
        self.prepareGeometryChange()
        self.sigRegionChanged.emit(self)

    def lineMoveFinished(self):
        self.sigRegionChangeFinished.emit(self)

    def mouseDragEvent(self, ev):
        if not self.movable or int(ev.button() & QtCore.Qt.LeftButton) == 0:
            return
        else:
            ev.accept()
            if ev.isStart():
                bdp = ev.buttonDownPos()
                self.cursorOffsets = [l.pos() - bdp for l in self.lines]
                self.startPositions = [l.pos() for l in self.lines]
                self.moving = True
            if not self.moving:
                return
                self.lines[0].blockSignals(True)
                for i, l in enumerate(self.lines):
                    l.setPos(self.cursorOffsets[i] + ev.pos())

                self.lines[0].blockSignals(False)
                self.prepareGeometryChange()
                if ev.isFinish():
                    self.moving = False
                    self.sigRegionChangeFinished.emit(self)
            else:
                self.sigRegionChanged.emit(self)

    def mouseClickEvent(self, ev):
        if self.moving:
            if ev.button() == QtCore.Qt.RightButton:
                ev.accept()
                for i, l in enumerate(self.lines):
                    l.setPos(self.startPositions[i])

                self.moving = False
                self.sigRegionChanged.emit(self)
                self.sigRegionChangeFinished.emit(self)

    def hoverEvent(self, ev):
        if self.movable and (ev.isExit() or ev.acceptDrags)(QtCore.Qt.LeftButton):
            self.setMouseHover(True)
        else:
            self.setMouseHover(False)

    def setMouseHover(self, hover):
        if self.mouseHovering == hover:
            return
        else:
            self.mouseHovering = hover
            if hover:
                c = self.brush.color()
                c.setAlpha(c.alpha() * 2)
                self.currentBrush = fn.mkBrush(c)
            else:
                self.currentBrush = self.brush
        self.update()