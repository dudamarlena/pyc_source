# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/GraphicsScene/mouseEvents.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 14214 bytes
from ..Point import Point
from ..Qt import QtCore, QtGui
import weakref
from .. import ptime

class MouseDragEvent(object):
    """MouseDragEvent"""

    def __init__(self, moveEvent, pressEvent, lastEvent, start=False, finish=False):
        self.start = start
        self.finish = finish
        self.accepted = False
        self.currentItem = None
        self._buttonDownScenePos = {}
        self._buttonDownScreenPos = {}
        for btn in [QtCore.Qt.LeftButton, QtCore.Qt.MidButton, QtCore.Qt.RightButton]:
            self._buttonDownScenePos[int(btn)] = moveEvent.buttonDownScenePos(btn)
            self._buttonDownScreenPos[int(btn)] = moveEvent.buttonDownScreenPos(btn)

        self._scenePos = moveEvent.scenePos()
        self._screenPos = moveEvent.screenPos()
        if lastEvent is None:
            self._lastScenePos = pressEvent.scenePos()
            self._lastScreenPos = pressEvent.screenPos()
        else:
            self._lastScenePos = lastEvent.scenePos()
            self._lastScreenPos = lastEvent.screenPos()
        self._buttons = moveEvent.buttons()
        self._button = pressEvent.button()
        self._modifiers = moveEvent.modifiers()
        self.acceptedItem = None

    def accept(self):
        """An item should call this method if it can handle the event. This will prevent the event being delivered to any other items."""
        self.accepted = True
        self.acceptedItem = self.currentItem

    def ignore(self):
        """An item should call this method if it cannot handle the event. This will allow the event to be delivered to other items."""
        self.accepted = False

    def isAccepted(self):
        return self.accepted

    def scenePos(self):
        """Return the current scene position of the mouse."""
        return Point(self._scenePos)

    def screenPos(self):
        """Return the current screen position (pixels relative to widget) of the mouse."""
        return Point(self._screenPos)

    def buttonDownScenePos(self, btn=None):
        """
        Return the scene position of the mouse at the time *btn* was pressed.
        If *btn* is omitted, then the button that initiated the drag is assumed.
        """
        if btn is None:
            btn = self.button()
        return Point(self._buttonDownScenePos[int(btn)])

    def buttonDownScreenPos(self, btn=None):
        """
        Return the screen position (pixels relative to widget) of the mouse at the time *btn* was pressed.
        If *btn* is omitted, then the button that initiated the drag is assumed.
        """
        if btn is None:
            btn = self.button()
        return Point(self._buttonDownScreenPos[int(btn)])

    def lastScenePos(self):
        """
        Return the scene position of the mouse immediately prior to this event.
        """
        return Point(self._lastScenePos)

    def lastScreenPos(self):
        """
        Return the screen position of the mouse immediately prior to this event.
        """
        return Point(self._lastScreenPos)

    def buttons(self):
        """
        Return the buttons currently pressed on the mouse.
        (see QGraphicsSceneMouseEvent::buttons in the Qt documentation)
        """
        return self._buttons

    def button(self):
        """Return the button that initiated the drag (may be different from the buttons currently pressed)
        (see QGraphicsSceneMouseEvent::button in the Qt documentation)
        
        """
        return self._button

    def pos(self):
        """
        Return the current position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._scenePos))

    def lastPos(self):
        """
        Return the previous position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._lastScenePos))

    def buttonDownPos(self, btn=None):
        """
        Return the position of the mouse at the time the drag was initiated
        in the coordinate system of the item that the event was delivered to.
        """
        if btn is None:
            btn = self.button()
        return Point(self.currentItem.mapFromScene(self._buttonDownScenePos[int(btn)]))

    def isStart(self):
        """Returns True if this event is the first since a drag was initiated."""
        return self.start

    def isFinish(self):
        """Returns False if this is the last event in a drag. Note that this
        event will have the same position as the previous one."""
        return self.finish

    def __repr__(self):
        if self.currentItem is None:
            lp = self._lastScenePos
            p = self._scenePos
        else:
            lp = self.lastPos()
            p = self.pos()
        return '<MouseDragEvent (%g,%g)->(%g,%g) buttons=%d start=%s finish=%s>' % (lp.x(), lp.y(), p.x(), p.y(), int(self.buttons()), str(self.isStart()), str(self.isFinish()))

    def modifiers(self):
        """Return any keyboard modifiers currently pressed.
        (see QGraphicsSceneMouseEvent::modifiers in the Qt documentation)
        
        """
        return self._modifiers


class MouseClickEvent(object):
    """MouseClickEvent"""

    def __init__(self, pressEvent, double=False):
        self.accepted = False
        self.currentItem = None
        self._double = double
        self._scenePos = pressEvent.scenePos()
        self._screenPos = pressEvent.screenPos()
        self._button = pressEvent.button()
        self._buttons = pressEvent.buttons()
        self._modifiers = pressEvent.modifiers()
        self._time = ptime.time()
        self.acceptedItem = None

    def accept(self):
        """An item should call this method if it can handle the event. This will prevent the event being delivered to any other items."""
        self.accepted = True
        self.acceptedItem = self.currentItem

    def ignore(self):
        """An item should call this method if it cannot handle the event. This will allow the event to be delivered to other items."""
        self.accepted = False

    def isAccepted(self):
        return self.accepted

    def scenePos(self):
        """Return the current scene position of the mouse."""
        return Point(self._scenePos)

    def screenPos(self):
        """Return the current screen position (pixels relative to widget) of the mouse."""
        return Point(self._screenPos)

    def buttons(self):
        """
        Return the buttons currently pressed on the mouse.
        (see QGraphicsSceneMouseEvent::buttons in the Qt documentation)
        """
        return self._buttons

    def button(self):
        """Return the mouse button that generated the click event.
        (see QGraphicsSceneMouseEvent::button in the Qt documentation)
        """
        return self._button

    def double(self):
        """Return True if this is a double-click."""
        return self._double

    def pos(self):
        """
        Return the current position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._scenePos))

    def lastPos(self):
        """
        Return the previous position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._lastScenePos))

    def modifiers(self):
        """Return any keyboard modifiers currently pressed.
        (see QGraphicsSceneMouseEvent::modifiers in the Qt documentation)        
        """
        return self._modifiers

    def __repr__(self):
        try:
            if self.currentItem is None:
                p = self._scenePos
            else:
                p = self.pos()
            return '<MouseClickEvent (%g,%g) button=%d>' % (p.x(), p.y(), int(self.button()))
        except:
            return '<MouseClickEvent button=%d>' % int(self.button())

    def time(self):
        return self._time


class HoverEvent(object):
    """HoverEvent"""

    def __init__(self, moveEvent, acceptable):
        self.enter = False
        self.acceptable = acceptable
        self.exit = False
        self._HoverEvent__clickItems = weakref.WeakValueDictionary()
        self._HoverEvent__dragItems = weakref.WeakValueDictionary()
        self.currentItem = None
        if moveEvent is not None:
            self._scenePos = moveEvent.scenePos()
            self._screenPos = moveEvent.screenPos()
            self._lastScenePos = moveEvent.lastScenePos()
            self._lastScreenPos = moveEvent.lastScreenPos()
            self._buttons = moveEvent.buttons()
            self._modifiers = moveEvent.modifiers()
        else:
            self.exit = True

    def isEnter(self):
        """Returns True if the mouse has just entered the item's shape"""
        return self.enter

    def isExit(self):
        """Returns True if the mouse has just exited the item's shape"""
        return self.exit

    def acceptClicks(self, button):
        """Inform the scene that the item (that the event was delivered to)
        would accept a mouse click event if the user were to click before
        moving the mouse again.
        
        Returns True if the request is successful, otherwise returns False (indicating
        that some other item would receive an incoming click).
        """
        if not self.acceptable:
            return False
        if button not in self._HoverEvent__clickItems:
            self._HoverEvent__clickItems[button] = self.currentItem
            return True
        return False

    def acceptDrags(self, button):
        """Inform the scene that the item (that the event was delivered to)
        would accept a mouse drag event if the user were to drag before
        the next hover event.
        
        Returns True if the request is successful, otherwise returns False (indicating
        that some other item would receive an incoming drag event).
        """
        if not self.acceptable:
            return False
        if button not in self._HoverEvent__dragItems:
            self._HoverEvent__dragItems[button] = self.currentItem
            return True
        return False

    def scenePos(self):
        """Return the current scene position of the mouse."""
        return Point(self._scenePos)

    def screenPos(self):
        """Return the current screen position of the mouse."""
        return Point(self._screenPos)

    def lastScenePos(self):
        """Return the previous scene position of the mouse."""
        return Point(self._lastScenePos)

    def lastScreenPos(self):
        """Return the previous screen position of the mouse."""
        return Point(self._lastScreenPos)

    def buttons(self):
        """
        Return the buttons currently pressed on the mouse.
        (see QGraphicsSceneMouseEvent::buttons in the Qt documentation)
        """
        return self._buttons

    def pos(self):
        """
        Return the current position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._scenePos))

    def lastPos(self):
        """
        Return the previous position of the mouse in the coordinate system of the item
        that the event was delivered to.
        """
        return Point(self.currentItem.mapFromScene(self._lastScenePos))

    def __repr__(self):
        if self.exit:
            return '<HoverEvent exit=True>'
        if self.currentItem is None:
            lp = self._lastScenePos
            p = self._scenePos
        else:
            lp = self.lastPos()
            p = self.pos()
        return '<HoverEvent (%g,%g)->(%g,%g) buttons=%d enter=%s exit=%s>' % (lp.x(), lp.y(), p.x(), p.y(), int(self.buttons()), str(self.isEnter()), str(self.isExit()))

    def modifiers(self):
        """Return any keyboard modifiers currently pressed.
        (see QGraphicsSceneMouseEvent::modifiers in the Qt documentation)        
        """
        return self._modifiers

    def clickItems(self):
        return self._HoverEvent__clickItems

    def dragItems(self):
        return self._HoverEvent__dragItems