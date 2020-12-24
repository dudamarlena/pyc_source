# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/displayobject.py
# Compiled at: 2014-03-13 10:09:15
import weakref
from flappy import _core
from flappy._core import _DisplayObject
from flappy.events import EventDispatcher, Event, EventPhase
from flappy.geom import Transform, ColorTransform, Matrix, Rectangle, Point
from flappy.display import Graphics, BitmapData

class DisplayObject(_DisplayObject, EventDispatcher):

    def __init__(self, name=None):
        self._native_init()
        EventDispatcher.__init__(self, None)
        self._parent = None
        if name is None:
            self.name = self.__class__.__name__ + ' #' + str(self.id)
        else:
            self.name = name
        self._graphics = None
        self._scroll_rect = None
        return

    def _native_init(self):
        _DisplayObject.__init__(self)

    def _dispatch_event(self, e):
        if e.target == None:
            e.target = self
        e.currentTarget = self
        return EventDispatcher.dispatchEvent(self, e)

    def _broadcast(self, e):
        self._dispatch_event(e)

    def dispatchEvent(self, e):
        ret = self._dispatch_event(e)
        if e.isCancelled:
            return True
        if e.bubbles and self.parent:
            self.parent.dispatchEvent(e)
        return ret

    def getBounds(self, coordinate_space):
        return self._getBounds(coordinate_space, True)

    def getRect(self, coordinate_space):
        return self._getBounds(coordinate_space, False)

    def globalToLocal(self, point):
        return _DisplayObject.globalToLocal(self, point)

    def localToGlobal(self, point):
        return _DisplayObject.localToGlobal(self, point)

    def hitTestObject(self, obj):
        if not (obj and obj.parent and self.parent):
            return False
        cur_mat = self.transform.concatenatedMatrix
        target_mat = obj.transform.concatenatedMatrix
        xpoint = Point(1.0, 0.0)
        ypoint = Point(0.0, 1.0)
        obj_width = self.width * cur_mat.deltaTransformPoint(xpoint).length
        obj_height = self.height * cur_mat.deltaTransformPoint(ypoint).length
        tgt_width = obj.width * target_mat.deltaTransformPoint(xpoint).length
        tgt_height = obj.height * target_mat.deltaTransformPoint(ypoint).length
        cur_rect = Rectangle(cur_mat.tx, cur_mat.ty, obj_width, obj_height)
        target_rect = Rectangle(target_mat.tx, target_mat.ty, tgt_width, tgt_height)
        return cur_rect.intersects(target_rect)

    def hitTestPoint(self, x, y, shape_flag=False):
        return self._hitTestPoint(x, y, shape_flag, True)

    def _find_by_id(self, obj_id):
        if self.id == obj_id:
            return self
        else:
            return

    def _get_interactive_object_stack(self, stack):
        from flappy.display import InteractiveObject
        if isinstance(self, InteractiveObject):
            stack.append(self)
        if self.parent:
            self.parent._get_interactive_object_stack(stack)

    def _fire_event(self, e):
        stack = []
        if self.parent:
            self.parent._get_interactive_object_stack(stack)
        ln = len(stack)
        if ln:
            e.eventPhase = EventPhase.CAPTURING_PHASE
            stack.reverse()
            for obj in stack:
                e.currentTarget = obj
                obj._dispatch_event(e)
                if e.isCancelled:
                    return

        e.eventPhase = EventPhase.AT_TARGET
        e.currentTarget = self
        self._dispatch_event(e)
        if e.isCancelled:
            return
        if e.bubbles:
            e.eventPhase = EventPhase.BUBBLING_PHASE
            stack.reverse()
            for obj in stack:
                e.currentTarget = obj
                obj._dispatch_event(e)
                if e.isCancelled:
                    return

    def _on_added(self, obj, is_on_stage):
        if obj == self:
            evt = Event(Event.ADDED, True, False)
            evt.target = obj
            self.dispatchEvent(evt)
        if is_on_stage:
            evt = Event(Event.ADDED_TO_STAGE, False, False)
            evt.target = obj
            self.dispatchEvent(evt)

    def _on_removed(self, obj, was_on_stage):
        if obj == self:
            evt = Event(Event.REMOVED, True, False)
            evt.target = obj
            self.dispatchEvent(evt)
        if was_on_stage:
            evt = Event(Event.REMOVED_FROM_STAGE, False, False)
            evt.target = obj
            self.dispatchEvent(evt)

    def _set_parent(self, parent):
        if self.parent == parent:
            return parent
        else:
            if self.parent is not None:
                self.parent._remove_child_from_array(self)
            if self.parent is None and parent is not None:
                self._parent = weakref.ref(parent)
                self._on_added(self, parent.stage is not None)
            elif self.parent and not parent:
                self._parent = None
                self._on_removed(self, self.stage is not None)
            else:
                self._parent = weakref.ref(parent) if parent != None else None
            return parent

    def _get_objects_under_point(self, p, result):
        if self._hitTestPoint(p.x, p.y, True, False):
            result.append(self)

    def rotateAroundPoint(self, x, y, deg):
        m = self.transform.matrix
        pt = Point(x, y)
        pt = m.transformPoint(pt)
        m.translate(-pt.x, -pt.y)
        m.rotate(deg)
        m.translate(pt.x, pt.y)
        self.transform.matrix = m

    def drawToBitmapData(self, bitmap_data, matrix=Matrix(), color_transform=ColorTransform(), blend_mode=0, clip_rect=None):
        _DisplayObject._draw_to_surface(self, bitmap_data, matrix, color_transform, blend_mode, clip_rect)

    @property
    def id(self):
        return self.getID()

    @property
    def name(self):
        return self.getName()

    @name.setter
    def name(self, value):
        self.setName(value)

    @property
    def alpha(self):
        return self.getAlpha()

    @alpha.setter
    def alpha(self, value):
        self.setAlpha(value)

    @property
    def x(self):
        return self.getX()

    @x.setter
    def x(self, value):
        self.setX(value)

    @property
    def y(self):
        return self.getY()

    @y.setter
    def y(self, value):
        self.setY(value)

    @property
    def globalX(self):
        if self.parent:
            return self.x + self.parent.globalX
        return 0.0

    @property
    def globalY(self):
        if self.parent:
            return self.y + self.parent.globalY
        return 0.0

    @property
    def width(self):
        return self.getWidth()

    @width.setter
    def width(self, value):
        self.setWidth(value)

    @property
    def height(self):
        return self.getHeight()

    @height.setter
    def height(self, value):
        self.setHeight(value)

    @property
    def scaleX(self):
        return self.getScaleX()

    @scaleX.setter
    def scaleX(self, value):
        self.setScaleX(float(value))

    @property
    def scaleY(self):
        return self.getScaleY()

    @scaleY.setter
    def scaleY(self, value):
        self.setScaleY(float(value))

    @property
    def visible(self):
        return self.getVisible()

    @visible.setter
    def visible(self, value):
        self.setVisible(value)

    @property
    def transform(self):
        return Transform(self)

    @transform.setter
    def transform(self, trans):
        self._setMatrix(trans.matrix)
        self._setColorTransform(trans.colorTransform)
        return trans

    @property
    def stage(self):
        if self.parent is not None:
            return self.parent.stage
        else:
            return

    @property
    def root(self):
        return self.stage

    @property
    def graphics(self):
        if not self._graphics:
            self._graphics = self.getGraphics()
        return self._graphics

    def getGraphics(self):
        return Graphics(self)

    @property
    def parent(self):
        if isinstance(self._parent, weakref.ref):
            return self._parent()
        else:
            return self._parent

    @property
    def opaqueBackground(self):
        return self.getOpaqueBackground()

    @opaqueBackground.setter
    def opaqueBackground(self, value):
        self.setOpaqueBackground(value)

    @property
    def scrollRect(self):
        return self._scroll_rect

    @scrollRect.setter
    def scrollRect(self, value):
        self._scroll_rect = value
        self.setScrollRect(value)

    @property
    def cacheAsBitmap(self):
        return self.getCacheAsBitmap()

    @cacheAsBitmap.setter
    def cacheAsBitmap(self, value):
        self.setCacheAsBitmap(value)

    @property
    def rotation(self):
        return self.getRotation()

    @rotation.setter
    def rotation(self, value):
        self.setRotation(value)