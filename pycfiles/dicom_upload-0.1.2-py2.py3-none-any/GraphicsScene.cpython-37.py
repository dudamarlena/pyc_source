# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/GraphicsScene/GraphicsScene.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 24739 bytes
from ..Qt import QtCore, QtGui
from ..python2_3 import sortList
import weakref
from ..Point import Point
from .. import functions as fn
from .. import ptime
from .mouseEvents import *
from .. import debug
if hasattr(QtCore, 'PYQT_VERSION'):
    try:
        import sip
        HAVE_SIP = True
    except ImportError:
        HAVE_SIP = False

else:
    HAVE_SIP = False
__all__ = [
 'GraphicsScene']

class GraphicsScene(QtGui.QGraphicsScene):
    """GraphicsScene"""
    sigMouseHover = QtCore.Signal(object)
    sigMouseMoved = QtCore.Signal(object)
    sigMouseClicked = QtCore.Signal(object)
    sigPrepareForPaint = QtCore.Signal()
    _addressCache = weakref.WeakValueDictionary()
    ExportDirectory = None

    @classmethod
    def registerObject(cls, obj):
        """
        Workaround for PyQt bug in qgraphicsscene.items()
        All subclasses of QGraphicsObject must register themselves with this function.
        (otherwise, mouse interaction with those objects will likely fail)
        """
        if HAVE_SIP:
            if isinstance(obj, sip.wrapper):
                cls._addressCache[sip.unwrapinstance(sip.cast(obj, QtGui.QGraphicsItem))] = obj

    def __init__(self, clickRadius=2, moveDistance=5, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)
        self.setClickRadius(clickRadius)
        self.setMoveDistance(moveDistance)
        self.exportDirectory = None
        self.clickEvents = []
        self.dragButtons = []
        self.mouseGrabber = None
        self.dragItem = None
        self.lastDrag = None
        self.hoverItems = weakref.WeakKeyDictionary()
        self.lastHoverEvent = None
        self.contextMenu = [
         QtGui.QAction('Export...', self)]
        self.contextMenu[0].triggered.connect(self.showExportDialog)
        self.exportDialog = None

    def render(self, *args):
        self.prepareForPaint()
        return (QtGui.QGraphicsScene.render)(self, *args)

    def prepareForPaint(self):
        """Called before every render. This method will inform items that the scene is about to
        be rendered by emitting sigPrepareForPaint.
        
        This allows items to delay expensive processing until they know a paint will be required."""
        self.sigPrepareForPaint.emit()

    def setClickRadius(self, r):
        """
        Set the distance away from mouse clicks to search for interacting items.
        When clicking, the scene searches first for items that directly intersect the click position
        followed by any other items that are within a rectangle that extends r pixels away from the 
        click position. 
        """
        self._clickRadius = r

    def setMoveDistance(self, d):
        """
        Set the distance the mouse must move after a press before mouseMoveEvents will be delivered.
        This ensures that clicks with a small amount of movement are recognized as clicks instead of
        drags.
        """
        self._moveDistance = d

    def mousePressEvent(self, ev):
        QtGui.QGraphicsScene.mousePressEvent(self, ev)
        if self.mouseGrabberItem() is None:
            if self.lastHoverEvent is not None:
                if ev.scenePos() != self.lastHoverEvent.scenePos():
                    self.sendHoverEvents(ev)
            self.clickEvents.append(MouseClickEvent(ev))
            items = self.items(ev.scenePos())
            for i in items:
                if i.isEnabled() and i.isVisible() and int(i.flags() & i.ItemIsFocusable) > 0:
                    i.setFocus(QtCore.Qt.MouseFocusReason)
                    break

    def mouseMoveEvent(self, ev):
        self.sigMouseMoved.emit(ev.scenePos())
        QtGui.QGraphicsScene.mouseMoveEvent(self, ev)
        self.sendHoverEvents(ev)
        if int(ev.buttons()) != 0:
            QtGui.QGraphicsScene.mouseMoveEvent(self, ev)
            if self.mouseGrabberItem() is None:
                now = ptime.time()
                init = False
                for btn in [QtCore.Qt.LeftButton, QtCore.Qt.MidButton, QtCore.Qt.RightButton]:
                    if int(ev.buttons() & btn) == 0:
                        continue
                    if int(btn) not in self.dragButtons:
                        cev = [e for e in self.clickEvents if int(e.button()) == int(btn)][0]
                        dist = Point(ev.screenPos() - cev.screenPos())
                        if dist.length() < self._moveDistance:
                            if now - cev.time() < 0.5:
                                continue
                        init = init or 
                        self.dragButtons.append(int(btn))

                if len(self.dragButtons) > 0:
                    if self.sendDragEvent(ev, init=init):
                        ev.accept()

    def leaveEvent(self, ev):
        if len(self.dragButtons) == 0:
            self.sendHoverEvents(ev, exitOnly=True)

    def mouseReleaseEvent(self, ev):
        if self.mouseGrabberItem() is None:
            if ev.button() in self.dragButtons:
                if self.sendDragEvent(ev, final=True):
                    ev.accept()
                self.dragButtons.remove(ev.button())
            else:
                cev = [e for e in self.clickEvents if int(e.button()) == int(ev.button())]
                if self.sendClickEvent(cev[0]):
                    ev.accept()
                self.clickEvents.remove(cev[0])
        if int(ev.buttons()) == 0:
            self.dragItem = None
            self.dragButtons = []
            self.clickEvents = []
            self.lastDrag = None
        QtGui.QGraphicsScene.mouseReleaseEvent(self, ev)
        self.sendHoverEvents(ev)

    def mouseDoubleClickEvent(self, ev):
        QtGui.QGraphicsScene.mouseDoubleClickEvent(self, ev)
        if self.mouseGrabberItem() is None:
            self.clickEvents.append(MouseClickEvent(ev, double=True))

    def sendHoverEvents(self, ev, exitOnly=False):
        if exitOnly:
            acceptable = False
            items = []
            event = HoverEvent(None, acceptable)
        else:
            acceptable = int(ev.buttons()) == 0
            event = HoverEvent(ev, acceptable)
            items = self.itemsNearEvent(event, hoverable=True)
            self.sigMouseHover.emit(items)
        prevItems = list(self.hoverItems.keys())
        for item in items:
            if hasattr(item, 'hoverEvent'):
                event.currentItem = item
                if item not in self.hoverItems:
                    self.hoverItems[item] = None
                    event.enter = True
                else:
                    prevItems.remove(item)
                    event.enter = False
                try:
                    item.hoverEvent(event)
                except:
                    debug.printExc('Error sending hover event:')

        event.enter = False
        event.exit = True
        for item in prevItems:
            event.currentItem = item
            try:
                try:
                    item.hoverEvent(event)
                except:
                    debug.printExc('Error sending hover exit event:')

            finally:
                del self.hoverItems[item]

        if (ev.type() == ev.GraphicsSceneMousePress or ev.type()) == ev.GraphicsSceneMouseMove:
            if int(ev.buttons()) == 0:
                self.lastHoverEvent = event

    def sendDragEvent(self, ev, init=False, final=False):
        event = MouseDragEvent(ev, (self.clickEvents[0]), (self.lastDrag), start=init, finish=final)
        if init and self.dragItem is None:
            if self.lastHoverEvent is not None:
                acceptedItem = self.lastHoverEvent.dragItems().get(event.button(), None)
            else:
                acceptedItem = None
            if acceptedItem is not None:
                self.dragItem = acceptedItem
                event.currentItem = self.dragItem
                try:
                    self.dragItem.mouseDragEvent(event)
                except:
                    debug.printExc('Error sending drag event:')

            else:
                for item in self.itemsNearEvent(event):
                    if item.isVisible():
                        if not item.isEnabled():
                            continue
                        if hasattr(item, 'mouseDragEvent'):
                            event.currentItem = item
                            try:
                                item.mouseDragEvent(event)
                            except:
                                debug.printExc('Error sending drag event:')

                            if event.isAccepted():
                                self.dragItem = item
                                if int(item.flags() & item.ItemIsFocusable) > 0:
                                    item.setFocus(QtCore.Qt.MouseFocusReason)
                                break

        elif self.dragItem is not None:
            event.currentItem = self.dragItem
            try:
                self.dragItem.mouseDragEvent(event)
            except:
                debug.printExc('Error sending hover exit event:')

        self.lastDrag = event
        return event.isAccepted()

    def sendClickEvent(self, ev):
        if self.dragItem is not None and hasattr(self.dragItem, 'mouseClickEvent'):
            ev.currentItem = self.dragItem
            self.dragItem.mouseClickEvent(ev)
        else:
            if self.lastHoverEvent is not None:
                acceptedItem = self.lastHoverEvent.clickItems().get(ev.button(), None)
            else:
                acceptedItem = None
            if acceptedItem is not None:
                ev.currentItem = acceptedItem
                try:
                    acceptedItem.mouseClickEvent(ev)
                except:
                    debug.printExc('Error sending click event:')

            else:
                for item in self.itemsNearEvent(ev):
                    if item.isVisible():
                        if not item.isEnabled():
                            continue
                        if hasattr(item, 'mouseClickEvent'):
                            ev.currentItem = item
                            try:
                                item.mouseClickEvent(ev)
                            except:
                                debug.printExc('Error sending click event:')

                            if ev.isAccepted():
                                if int(item.flags() & item.ItemIsFocusable) > 0:
                                    item.setFocus(QtCore.Qt.MouseFocusReason)
                                break

        self.sigMouseClicked.emit(ev)
        return ev.isAccepted()

    def items(self, *args):
        items = (QtGui.QGraphicsScene.items)(self, *args)
        items2 = list(map(self.translateGraphicsItem, items))
        return items2

    def selectedItems(self, *args):
        items = (QtGui.QGraphicsScene.selectedItems)(self, *args)
        items2 = list(map(self.translateGraphicsItem, items))
        return items2

    def itemAt(self, *args):
        item = (QtGui.QGraphicsScene.itemAt)(self, *args)
        return self.translateGraphicsItem(item)

    def itemsNearEvent(self, event, selMode=QtCore.Qt.IntersectsItemShape, sortOrder=QtCore.Qt.DescendingOrder, hoverable=False):
        """
        Return an iterator that iterates first through the items that directly intersect point (in Z order)
        followed by any other items that are within the scene's click radius.
        """
        view = self.views()[0]
        tr = view.viewportTransform()
        r = self._clickRadius
        rect = view.mapToScene(QtCore.QRect(0, 0, 2 * r, 2 * r)).boundingRect()
        seen = set()
        if hasattr(event, 'buttonDownScenePos'):
            point = event.buttonDownScenePos()
        else:
            point = event.scenePos()
        w = rect.width()
        h = rect.height()
        rgn = QtCore.QRectF(point.x() - w, point.y() - h, 2 * w, 2 * h)
        items = self.items(point, selMode, sortOrder, tr)
        items2 = []
        for item in items:
            if hoverable:
                if not hasattr(item, 'hoverEvent'):
                    continue
            shape = item.shape()
            if shape is None:
                continue
            if shape.contains(item.mapFromScene(point)):
                items2.append(item)

        def absZValue(item):
            if item is None:
                return 0
            return item.zValue() + absZValue(item.parentItem())

        sortList(items2, lambda a, b: cmp(absZValue(b), absZValue(a)))
        return items2

    def getViewWidget(self):
        return self.views()[0]

    def addParentContextMenus(self, item, menu, event):
        """
        Can be called by any item in the scene to expand its context menu to include parent context menus.
        Parents may implement getContextMenus to add new menus / actions to the existing menu.
        getContextMenus must accept 1 argument (the event that generated the original menu) and
        return a single QMenu or a list of QMenus.
        
        The final menu will look like:
        
            |    Original Item 1
            |    Original Item 2
            |    ...
            |    Original Item N
            |    ------------------
            |    Parent Item 1
            |    Parent Item 2
            |    ...
            |    Grandparent Item 1
            |    ...
            
        
        ==============  ==================================================
        **Arguments:**
        item            The item that initially created the context menu 
                        (This is probably the item making the call to this function)
        menu            The context menu being shown by the item
        event           The original event that triggered the menu to appear.
        ==============  ==================================================
        """
        menusToAdd = []
        while item is not self:
            item = item.parentItem()
            if item is None:
                item = self
            if not hasattr(item, 'getContextMenus'):
                continue
            subMenus = item.getContextMenus(event) or 
            if isinstance(subMenus, list):
                menusToAdd.extend(subMenus)
            else:
                menusToAdd.append(subMenus)

        if menusToAdd:
            menu.addSeparator()
        for m in menusToAdd:
            if isinstance(m, QtGui.QMenu):
                menu.addMenu(m)
            elif isinstance(m, QtGui.QAction):
                menu.addAction(m)
            else:
                raise Exception('Cannot add object %s (type=%s) to QMenu.' % (str(m), str(type(m))))

        return menu

    def getContextMenus(self, event):
        self.contextMenuItem = event.acceptedItem
        return self.contextMenu

    def showExportDialog(self):
        if self.exportDialog is None:
            from . import exportDialog
            self.exportDialog = exportDialog.ExportDialog(self)
        self.exportDialog.show(self.contextMenuItem)

    @staticmethod
    def translateGraphicsItem(item):
        if HAVE_SIP:
            if isinstance(item, sip.wrapper):
                addr = sip.unwrapinstance(sip.cast(item, QtGui.QGraphicsItem))
                item = GraphicsScene._addressCache.get(addr, item)
        return item

    @staticmethod
    def translateGraphicsItems(items):
        return list(map(GraphicsScene.translateGraphicsItem, items))