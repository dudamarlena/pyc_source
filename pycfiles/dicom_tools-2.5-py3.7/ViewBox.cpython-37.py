# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ViewBox/ViewBox.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 72774 bytes
from ...Qt import QtGui, QtCore
from ...python2_3 import sortList
import numpy as np
from ...Point import Point
from ... import functions as fn
from ..ItemGroup import ItemGroup
from ..GraphicsWidget import GraphicsWidget
import weakref
from copy import deepcopy
from ... import debug
from ... import getConfigOption
import sys
from ...Qt import isQObjectAlive
__all__ = ['ViewBox']

class WeakList(object):

    def __init__(self):
        self._items = []

    def append(self, obj):
        self._items.insert(0, weakref.ref(obj))

    def __iter__(self):
        i = len(self._items) - 1
        while i >= 0:
            ref = self._items[i]
            d = ref()
            if d is None:
                del self._items[i]
            else:
                yield d
            i -= 1


class ChildGroup(ItemGroup):

    def __init__(self, parent):
        ItemGroup.__init__(self, parent)
        self.itemsChangedListeners = WeakList()
        self._GraphicsObject__inform_view_on_change = False

    def itemChange(self, change, value):
        ret = ItemGroup.itemChange(self, change, value)
        if change == self.ItemChildAddedChange or change == self.ItemChildRemovedChange:
            try:
                itemsChangedListeners = self.itemsChangedListeners
            except AttributeError:
                pass

        else:
            for listener in itemsChangedListeners:
                listener.itemsChanged()

        return ret


class ViewBox(GraphicsWidget):
    __doc__ = '\n    **Bases:** :class:`GraphicsWidget <pyqtgraph.GraphicsWidget>`\n    \n    Box that allows internal scaling/panning of children by mouse drag. \n    This class is usually created automatically as part of a :class:`PlotItem <pyqtgraph.PlotItem>` or :class:`Canvas <pyqtgraph.canvas.Canvas>` or with :func:`GraphicsLayout.addViewBox() <pyqtgraph.GraphicsLayout.addViewBox>`.\n    \n    Features:\n    \n    * Scaling contents by mouse or auto-scale when contents change\n    * View linking--multiple views display the same data ranges\n    * Configurable by context menu\n    * Item coordinate mapping methods\n    \n    '
    sigYRangeChanged = QtCore.Signal(object, object)
    sigXRangeChanged = QtCore.Signal(object, object)
    sigRangeChangedManually = QtCore.Signal(object)
    sigRangeChanged = QtCore.Signal(object, object)
    sigStateChanged = QtCore.Signal(object)
    sigTransformChanged = QtCore.Signal(object)
    sigResized = QtCore.Signal(object)
    PanMode = 3
    RectMode = 1
    XAxis = 0
    YAxis = 1
    XYAxes = 2
    NamedViews = weakref.WeakValueDictionary()
    AllViews = weakref.WeakKeyDictionary()

    def __init__(self, parent=None, border=None, lockAspect=False, enableMouse=True, invertY=False, enableMenu=True, name=None, invertX=False):
        """
        ==============  =============================================================
        **Arguments:**
        *parent*        (QGraphicsWidget) Optional parent widget
        *border*        (QPen) Do draw a border around the view, give any
                        single argument accepted by :func:`mkPen <pyqtgraph.mkPen>`
        *lockAspect*    (False or float) The aspect ratio to lock the view
                        coorinates to. (or False to allow the ratio to change)
        *enableMouse*   (bool) Whether mouse can be used to scale/pan the view
        *invertY*       (bool) See :func:`invertY <pyqtgraph.ViewBox.invertY>`
        *invertX*       (bool) See :func:`invertX <pyqtgraph.ViewBox.invertX>`
        *enableMenu*    (bool) Whether to display a context menu when 
                        right-clicking on the ViewBox background.
        *name*          (str) Used to register this ViewBox so that it appears
                        in the "Link axis" dropdown inside other ViewBox
                        context menus. This allows the user to manually link
                        the axes of any other view to this one. 
        ==============  =============================================================
        """
        GraphicsWidget.__init__(self, parent)
        self.name = None
        self.linksBlocked = False
        self.addedItems = []
        self._matrixNeedsUpdate = True
        self._autoRangeNeedsUpdate = True
        self._lastScene = None
        self.state = {'targetRange':[
          [
           0, 1], [0, 1]], 
         'viewRange':[
          [
           0, 1], [0, 1]], 
         'yInverted':invertY, 
         'xInverted':invertX, 
         'aspectLocked':False, 
         'autoRange':[
          True, True], 
         'autoPan':[
          False, False], 
         'autoVisibleOnly':[
          False, False], 
         'linkedViews':[
          None, None], 
         'mouseEnabled':[
          enableMouse, enableMouse], 
         'mouseMode':ViewBox.PanMode if getConfigOption('leftButtonPan') else ViewBox.RectMode, 
         'enableMenu':enableMenu, 
         'wheelScaleFactor':-0.125, 
         'background':None, 
         'limits':{'xLimits':[
           None, None], 
          'yLimits':[
           None, None], 
          'xRange':[
           None, None], 
          'yRange':[
           None, None]}}
        self._updatingRange = False
        self._itemBoundsCache = weakref.WeakKeyDictionary()
        self.locateGroup = None
        self.setFlag(self.ItemClipsChildrenToShape)
        self.setFlag(self.ItemIsFocusable, True)
        self.childGroup = ChildGroup(self)
        self.childGroup.itemsChangedListeners.append(self)
        self.background = QtGui.QGraphicsRectItem(self.rect())
        self.background.setParentItem(self)
        self.background.setZValue(-1000000.0)
        self.background.setPen(fn.mkPen(None))
        self.updateBackground()
        self.rbScaleBox = QtGui.QGraphicsRectItem(0, 0, 1, 1)
        self.rbScaleBox.setPen(fn.mkPen((255, 255, 100), width=1))
        self.rbScaleBox.setBrush(fn.mkBrush(255, 255, 0, 100))
        self.rbScaleBox.setZValue(1000000000.0)
        self.rbScaleBox.hide()
        self.addItem((self.rbScaleBox), ignoreBounds=True)
        self.target = QtGui.QGraphicsRectItem(0, 0, 1, 1)
        self.target.setPen(fn.mkPen('r'))
        self.target.setParentItem(self)
        self.target.hide()
        self.axHistory = []
        self.axHistoryPointer = -1
        self.setZValue(-100)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setAspectLocked(lockAspect)
        self.border = fn.mkPen(border)
        self.menu = ViewBoxMenu(self)
        self.register(name)
        if name is None:
            self.updateViewLists()

    def register(self, name):
        """
        Add this ViewBox to the registered list of views. 
        
        This allows users to manually link the axes of any other ViewBox to
        this one. The specified *name* will appear in the drop-down lists for 
        axis linking in the context menus of all other views.
        
        The same can be accomplished by initializing the ViewBox with the *name* attribute.
        """
        ViewBox.AllViews[self] = None
        if self.name is not None:
            del ViewBox.NamedViews[self.name]
        self.name = name
        if name is not None:
            ViewBox.NamedViews[name] = self
            ViewBox.updateAllViewLists()
            sid = id(self)
            self.destroyed.connect(lambda :             if ViewBox is not None:
                if 'sid' in locals():
                    if 'name' in locals():
ViewBox.forgetView(sid, name) # Avoid dead code: None)

    def unregister(self):
        """
        Remove this ViewBox from the list of linkable views. (see :func:`register() <pyqtgraph.ViewBox.register>`)
        """
        del ViewBox.AllViews[self]
        if self.name is not None:
            del ViewBox.NamedViews[self.name]

    def close(self):
        self.clear()
        self.unregister()

    def implements(self, interface):
        return interface == 'ViewBox'

    def checkSceneChange(self):
        scene = self.scene()
        if scene == self._lastScene:
            return
        if self._lastScene is not None:
            if hasattr(self.lastScene, 'sigPrepareForPaint'):
                self._lastScene.sigPrepareForPaint.disconnect(self.prepareForPaint)
        if scene is not None:
            if hasattr(scene, 'sigPrepareForPaint'):
                scene.sigPrepareForPaint.connect(self.prepareForPaint)
        self.prepareForPaint()
        self._lastScene = scene

    def prepareForPaint(self):
        if self._autoRangeNeedsUpdate:
            self.updateAutoRange()
        if self._matrixNeedsUpdate:
            self.updateMatrix()

    def getState(self, copy=True):
        """Return the current state of the ViewBox. 
        Linked views are always converted to view names in the returned state."""
        state = self.state.copy()
        views = []
        for v in state['linkedViews']:
            if isinstance(v, weakref.ref):
                v = v()
            if v is None or isinstance(v, basestring):
                views.append(v)
            else:
                views.append(v.name)

        state['linkedViews'] = views
        if copy:
            return deepcopy(state)
        return state

    def setState(self, state):
        """Restore the state of this ViewBox.
        (see also getState)"""
        state = state.copy()
        self.setXLink(state['linkedViews'][0])
        self.setYLink(state['linkedViews'][1])
        del state['linkedViews']
        self.state.update(state)
        self.updateViewRange()
        self.sigStateChanged.emit(self)

    def setBackgroundColor(self, color):
        """
        Set the background color of the ViewBox.
        
        If color is None, then no background will be drawn.
        
        Added in version 0.9.9
        """
        self.background.setVisible(color is not None)
        self.state['background'] = color
        self.updateBackground()

    def setMouseMode(self, mode):
        """
        Set the mouse interaction mode. *mode* must be either ViewBox.PanMode or ViewBox.RectMode.
        In PanMode, the left mouse button pans the view and the right button scales.
        In RectMode, the left button draws a rectangle which updates the visible region (this mode is more suitable for single-button mice)
        """
        if mode not in [ViewBox.PanMode, ViewBox.RectMode]:
            raise Exception('Mode must be ViewBox.PanMode or ViewBox.RectMode')
        self.state['mouseMode'] = mode
        self.sigStateChanged.emit(self)

    def setLeftButtonAction(self, mode='rect'):
        if mode.lower() == 'rect':
            self.setMouseMode(ViewBox.RectMode)
        else:
            if mode.lower() == 'pan':
                self.setMouseMode(ViewBox.PanMode)
            else:
                raise Exception('graphicsItems:ViewBox:setLeftButtonAction: unknown mode = %s (Options are "pan" and "rect")' % mode)

    def innerSceneItem(self):
        return self.childGroup

    def setMouseEnabled(self, x=None, y=None):
        """
        Set whether each axis is enabled for mouse interaction. *x*, *y* arguments must be True or False.
        This allows the user to pan/scale one axis of the view while leaving the other axis unchanged.
        """
        if x is not None:
            self.state['mouseEnabled'][0] = x
        if y is not None:
            self.state['mouseEnabled'][1] = y
        self.sigStateChanged.emit(self)

    def mouseEnabled(self):
        return self.state['mouseEnabled'][:]

    def setMenuEnabled(self, enableMenu=True):
        self.state['enableMenu'] = enableMenu
        self.sigStateChanged.emit(self)

    def menuEnabled(self):
        return self.state.get('enableMenu', True)

    def addItem(self, item, ignoreBounds=False):
        """
        Add a QGraphicsItem to this view. The view will include this item when determining how to set its range
        automatically unless *ignoreBounds* is True.
        """
        if item.zValue() < self.zValue():
            item.setZValue(self.zValue() + 1)
        else:
            scene = self.scene()
            if scene is not None:
                if scene is not item.scene():
                    scene.addItem(item)
            item.setParentItem(self.childGroup)
            ignoreBounds or self.addedItems.append(item)
        self.updateAutoRange()

    def removeItem(self, item):
        """Remove an item from this view."""
        try:
            self.addedItems.remove(item)
        except:
            pass

        self.scene().removeItem(item)
        self.updateAutoRange()

    def clear(self):
        for i in self.addedItems[:]:
            self.removeItem(i)

        for ch in self.childGroup.childItems():
            ch.setParentItem(None)

    def resizeEvent(self, ev):
        self.linkedXChanged()
        self.linkedYChanged()
        self.updateAutoRange()
        self.updateViewRange()
        self._matrixNeedsUpdate = True
        self.sigStateChanged.emit(self)
        self.background.setRect(self.rect())
        self.sigResized.emit(self)

    def viewRange(self):
        """Return a the view's visible range as a list: [[xmin, xmax], [ymin, ymax]]"""
        return [x[:] for x in self.state['viewRange']]

    def viewRect(self):
        """Return a QRectF bounding the region visible within the ViewBox"""
        try:
            vr0 = self.state['viewRange'][0]
            vr1 = self.state['viewRange'][1]
            return QtCore.QRectF(vr0[0], vr1[0], vr0[1] - vr0[0], vr1[1] - vr1[0])
        except:
            print('make qrectf failed:', self.state['viewRange'])
            raise

    def targetRange(self):
        return [x[:] for x in self.state['targetRange']]

    def targetRect(self):
        """
        Return the region which has been requested to be visible. 
        (this is not necessarily the same as the region that is *actually* visible--
        resizing and aspect ratio constraints can cause targetRect() and viewRect() to differ)
        """
        try:
            tr0 = self.state['targetRange'][0]
            tr1 = self.state['targetRange'][1]
            return QtCore.QRectF(tr0[0], tr1[0], tr0[1] - tr0[0], tr1[1] - tr1[0])
        except:
            print('make qrectf failed:', self.state['targetRange'])
            raise

    def _resetTarget(self):
        if self.state['aspectLocked'] is False:
            self.state['targetRange'] = [
             self.state['viewRange'][0][:], self.state['viewRange'][1][:]]

    def setRange(self, rect=None, xRange=None, yRange=None, padding=None, update=True, disableAutoRange=True):
        """
        Set the visible range of the ViewBox.
        Must specify at least one of *rect*, *xRange*, or *yRange*. 
        
        ================== =====================================================================
        **Arguments:**
        *rect*             (QRectF) The full range that should be visible in the view box.
        *xRange*           (min,max) The range that should be visible along the x-axis.
        *yRange*           (min,max) The range that should be visible along the y-axis.
        *padding*          (float) Expand the view by a fraction of the requested range. 
                           By default, this value is set between 0.02 and 0.1 depending on
                           the size of the ViewBox.
        *update*           (bool) If True, update the range of the ViewBox immediately. 
                           Otherwise, the update is deferred until before the next render.
        *disableAutoRange* (bool) If True, auto-ranging is diabled. Otherwise, it is left
                           unchanged.
        ================== =====================================================================
        
        """
        changes = {}
        setRequested = [
         False, False]
        if rect is not None:
            changes = {0:[
              rect.left(), rect.right()], 
             1:[rect.top(), rect.bottom()]}
            setRequested = [True, True]
        if xRange is not None:
            changes[0] = xRange
            setRequested[0] = True
        if yRange is not None:
            changes[1] = yRange
            setRequested[1] = True
        if len(changes) == 0:
            print(rect)
            raise Exception('Must specify at least one of rect, xRange, or yRange. (gave rect=%s)' % str(type(rect)))
        changed = [
         False, False]
        for ax, range in changes.items():
            mn = min(range)
            mx = max(range)
            if mn == mx:
                dy = self.state['viewRange'][ax][1] - self.state['viewRange'][ax][0]
                if dy == 0:
                    dy = 1
                mn -= dy * 0.5
                mx += dy * 0.5
                xpad = 0.0
            else:
                if not all(np.isfinite([mn, mx])):
                    raise Exception('Cannot set range [%s, %s]' % (str(mn), str(mx)))
                if padding is None:
                    xpad = self.suggestPadding(ax)
                else:
                    xpad = padding
            p = (mx - mn) * xpad
            mn -= p
            mx += p
            if self.state['targetRange'][ax] != [mn, mx]:
                self.state['targetRange'][ax] = [
                 mn, mx]
                changed[ax] = True

        lockX, lockY = setRequested
        if lockX:
            if lockY:
                lockX = False
                lockY = False
        self.updateViewRange(lockX, lockY)
        if disableAutoRange:
            xOff = False if setRequested[0] else None
            yOff = False if setRequested[1] else None
            self.enableAutoRange(x=xOff, y=yOff)
            changed.append(True)
        if any(changed):
            self.sigStateChanged.emit(self)
            if self.target.isVisible():
                self.target.setRect(self.mapRectFromItem(self.childGroup, self.targetRect()))
        if changed[0] and self.state['autoVisibleOnly'][1] and self.state['autoRange'][0] is not False:
            self._autoRangeNeedsUpdate = True
        else:
            if changed[1]:
                if self.state['autoVisibleOnly'][0]:
                    if self.state['autoRange'][1] is not False:
                        self._autoRangeNeedsUpdate = True

    def setYRange(self, min, max, padding=None, update=True):
        """
        Set the visible Y range of the view to [*min*, *max*]. 
        The *padding* argument causes the range to be set larger by the fraction specified.
        (by default, this value is between 0.02 and 0.1 depending on the size of the ViewBox)
        """
        self.setRange(yRange=[min, max], update=update, padding=padding)

    def setXRange(self, min, max, padding=None, update=True):
        """
        Set the visible X range of the view to [*min*, *max*]. 
        The *padding* argument causes the range to be set larger by the fraction specified.
        (by default, this value is between 0.02 and 0.1 depending on the size of the ViewBox)
        """
        self.setRange(xRange=[min, max], update=update, padding=padding)

    def autoRange(self, padding=None, items=None, item=None):
        """
        Set the range of the view box to make all children visible.
        Note that this is not the same as enableAutoRange, which causes the view to 
        automatically auto-range whenever its contents are changed.
        
        ==============  ============================================================
        **Arguments:**
        padding         The fraction of the total data range to add on to the final
                        visible range. By default, this value is set between 0.02
                        and 0.1 depending on the size of the ViewBox.
        items           If specified, this is a list of items to consider when
                        determining the visible range.
        ==============  ============================================================
        """
        if item is None:
            bounds = self.childrenBoundingRect(items=items)
        else:
            print("Warning: ViewBox.autoRange(item=__) is deprecated. Use 'items' argument instead.")
            bounds = self.mapFromItemToView(item, item.boundingRect()).boundingRect()
        if bounds is not None:
            self.setRange(bounds, padding=padding)

    def suggestPadding(self, axis):
        l = self.width() if axis == 0 else self.height()
        if l > 0:
            padding = np.clip(1.0 / l ** 0.5, 0.02, 0.1)
        else:
            padding = 0.02
        return padding

    def setLimits(self, **kwds):
        """
        Set limits that constrain the possible view ranges.
        
        **Panning limits**. The following arguments define the region within the 
        viewbox coordinate system that may be accessed by panning the view.
        
        =========== ============================================================
        xMin        Minimum allowed x-axis value
        xMax        Maximum allowed x-axis value
        yMin        Minimum allowed y-axis value
        yMax        Maximum allowed y-axis value
        =========== ============================================================        
        
        **Scaling limits**. These arguments prevent the view being zoomed in or
        out too far.
        
        =========== ============================================================
        minXRange   Minimum allowed left-to-right span across the view.
        maxXRange   Maximum allowed left-to-right span across the view.
        minYRange   Minimum allowed top-to-bottom span across the view.
        maxYRange   Maximum allowed top-to-bottom span across the view.
        =========== ============================================================
        
        Added in version 0.9.9
        """
        update = False
        allowed = ['xMin', 'xMax', 'yMin', 'yMax', 'minXRange', 'maxXRange', 'minYRange', 'maxYRange']
        for kwd in kwds:
            if kwd not in allowed:
                raise ValueError("Invalid keyword argument '%s'." % kwd)

        for axis in (0, 1):
            for mnmx in (0, 1):
                kwd = [['xMin', 'xMax'], ['yMin', 'yMax']][axis][mnmx]
                lname = ['xLimits', 'yLimits'][axis]
                if kwd in kwds:
                    if self.state['limits'][lname][mnmx] != kwds[kwd]:
                        self.state['limits'][lname][mnmx] = kwds[kwd]
                        update = True
                kwd = [
                 [
                  'minXRange', 'maxXRange'], ['minYRange', 'maxYRange']][axis][mnmx]
                lname = ['xRange', 'yRange'][axis]
                if kwd in kwds and self.state['limits'][lname][mnmx] != kwds[kwd]:
                    self.state['limits'][lname][mnmx] = kwds[kwd]
                    update = True

        if update:
            self.updateViewRange()

    def scaleBy(self, s=None, center=None, x=None, y=None):
        """
        Scale by *s* around given center point (or center of view).
        *s* may be a Point or tuple (x, y).
        
        Optionally, x or y may be specified individually. This allows the other 
        axis to be left unaffected (note that using a scale factor of 1.0 may
        cause slight changes due to floating-point error).
        """
        if s is not None:
            scale = Point(s)
        else:
            scale = [
             x, y]
        affect = [True, True]
        if scale[0] is None:
            if scale[1] is None:
                return
        if scale[0] is None:
            affect[0] = False
            scale[0] = 1.0
        else:
            if scale[1] is None:
                affect[1] = False
                scale[1] = 1.0
            else:
                scale = Point(scale)
                if self.state['aspectLocked'] is not False:
                    scale[0] = scale[1]
                else:
                    vr = self.targetRect()
                    if center is None:
                        center = Point(vr.center())
                    else:
                        center = Point(center)
                    tl = center + (vr.topLeft() - center) * scale
                    br = center + (vr.bottomRight() - center) * scale
                    if not affect[0]:
                        self.setYRange((tl.y()), (br.y()), padding=0)
                    else:
                        if not affect[1]:
                            self.setXRange((tl.x()), (br.x()), padding=0)
                        else:
                            self.setRange((QtCore.QRectF(tl, br)), padding=0)

    def translateBy(self, t=None, x=None, y=None):
        """
        Translate the view by *t*, which may be a Point or tuple (x, y).
        
        Alternately, x or y may be specified independently, leaving the other
        axis unchanged (note that using a translation of 0 may still cause
        small changes due to floating-point error).
        """
        vr = self.targetRect()
        if t is not None:
            t = Point(t)
            self.setRange((vr.translated(t)), padding=0)
        else:
            if x is not None:
                x = (
                 vr.left() + x, vr.right() + x)
            if y is not None:
                y = (
                 vr.top() + y, vr.bottom() + y)
            if x is not None or y is not None:
                self.setRange(xRange=x, yRange=y, padding=0)

    def enableAutoRange(self, axis=None, enable=True, x=None, y=None):
        """
        Enable (or disable) auto-range for *axis*, which may be ViewBox.XAxis, ViewBox.YAxis, or ViewBox.XYAxes for both
        (if *axis* is omitted, both axes will be changed).
        When enabled, the axis will automatically rescale when items are added/removed or change their shape.
        The argument *enable* may optionally be a float (0.0-1.0) which indicates the fraction of the data that should
        be visible (this only works with items implementing a dataRange method, such as PlotDataItem).
        """
        if x is not None or y is not None:
            if x is not None:
                self.enableAutoRange(ViewBox.XAxis, x)
            if y is not None:
                self.enableAutoRange(ViewBox.YAxis, y)
            return
        if enable is True:
            enable = 1.0
        if axis is None:
            axis = ViewBox.XYAxes
        else:
            needAutoRangeUpdate = False
            if axis == ViewBox.XYAxes or axis == 'xy':
                axes = [
                 0, 1]
            else:
                if axis == ViewBox.XAxis or axis == 'x':
                    axes = [
                     0]
                else:
                    if axis == ViewBox.YAxis or axis == 'y':
                        axes = [
                         1]
                    else:
                        raise Exception('axis argument must be ViewBox.XAxis, ViewBox.YAxis, or ViewBox.XYAxes.')
        for ax in axes:
            if self.state['autoRange'][ax] != enable:
                if enable is False:
                    if self._autoRangeNeedsUpdate:
                        self.updateAutoRange()
                self.state['autoRange'][ax] = enable
                self._autoRangeNeedsUpdate |= enable is not False
                self.update()

        self.sigStateChanged.emit(self)

    def disableAutoRange(self, axis=None):
        """Disables auto-range. (See enableAutoRange)"""
        self.enableAutoRange(axis, enable=False)

    def autoRangeEnabled(self):
        return self.state['autoRange'][:]

    def setAutoPan(self, x=None, y=None):
        if x is not None:
            self.state['autoPan'][0] = x
        if y is not None:
            self.state['autoPan'][1] = y
        if None not in [x, y]:
            self.updateAutoRange()

    def setAutoVisible(self, x=None, y=None):
        if x is not None:
            self.state['autoVisibleOnly'][0] = x
            if x is True:
                self.state['autoVisibleOnly'][1] = False
        if y is not None:
            self.state['autoVisibleOnly'][1] = y
            if y is True:
                self.state['autoVisibleOnly'][0] = False
        if x is not None or y is not None:
            self.updateAutoRange()

    def updateAutoRange(self):
        if self._updatingRange:
            return
        self._updatingRange = True
        try:
            targetRect = self.viewRange()
            if not any(self.state['autoRange']):
                return
            fractionVisible = self.state['autoRange'][:]
            for i in (0, 1):
                if type(fractionVisible[i]) is bool:
                    fractionVisible[i] = 1.0

            childRange = None
            order = [
             0, 1]
            if self.state['autoVisibleOnly'][0] is True:
                order = [
                 1, 0]
            args = {}
            for ax in order:
                if self.state['autoRange'][ax] is False:
                    continue
                elif self.state['autoVisibleOnly'][ax]:
                    oRange = [
                     None, None]
                    oRange[ax] = targetRect[(1 - ax)]
                    childRange = self.childrenBounds(frac=fractionVisible, orthoRange=oRange)
                else:
                    if childRange is None:
                        childRange = self.childrenBounds(frac=fractionVisible)
                xr = childRange[ax]
                if xr is not None:
                    if self.state['autoPan'][ax]:
                        x = sum(xr) * 0.5
                        w2 = (targetRect[ax][1] - targetRect[ax][0]) / 2.0
                        childRange[ax] = [x - w2, x + w2]
                    else:
                        padding = self.suggestPadding(ax)
                        wp = (xr[1] - xr[0]) * padding
                        childRange[ax][0] -= wp
                        childRange[ax][1] += wp
                    targetRect[ax] = childRange[ax]
                    args['xRange' if ax == 0 else 'yRange'] = targetRect[ax]

            if len(args) == 0:
                return
            args['padding'] = 0
            args['disableAutoRange'] = False
            for k in ('xRange', 'yRange'):
                if k in args:
                    r = np.all(np.isfinite(args[k])) or args.pop(k)

            (self.setRange)(**args)
        finally:
            self._autoRangeNeedsUpdate = False
            self._updatingRange = False

    def setXLink(self, view):
        """Link this view's X axis to another view. (see LinkView)"""
        self.linkView(self.XAxis, view)

    def setYLink(self, view):
        """Link this view's Y axis to another view. (see LinkView)"""
        self.linkView(self.YAxis, view)

    def linkView(self, axis, view):
        """
        Link X or Y axes of two views and unlink any previously connected axes. *axis* must be ViewBox.XAxis or ViewBox.YAxis.
        If view is None, the axis is left unlinked.
        """
        if isinstance(view, basestring):
            if view == '':
                view = None
            else:
                view = ViewBox.NamedViews.get(view, view)
        else:
            if hasattr(view, 'implements'):
                if view.implements('ViewBoxWrapper'):
                    view = view.getViewBox()
            elif axis == ViewBox.XAxis:
                signal = 'sigXRangeChanged'
                slot = self.linkedXChanged
            else:
                signal = 'sigYRangeChanged'
                slot = self.linkedYChanged
            oldLink = self.linkedView(axis)
            if oldLink is not None:
                try:
                    getattr(oldLink, signal).disconnect(slot)
                    oldLink.sigResized.disconnect(slot)
                except (TypeError, RuntimeError):
                    pass

        if view is None or isinstance(view, basestring):
            self.state['linkedViews'][axis] = view
        else:
            self.state['linkedViews'][axis] = weakref.ref(view)
            getattr(view, signal).connect(slot)
            view.sigResized.connect(slot)
            if view.autoRangeEnabled()[axis] is not False:
                self.enableAutoRange(axis, False)
                slot()
            else:
                if self.autoRangeEnabled()[axis] is False:
                    slot()
                self.sigStateChanged.emit(self)

    def blockLink(self, b):
        self.linksBlocked = b

    def linkedXChanged(self):
        view = self.linkedView(0)
        self.linkedViewChanged(view, ViewBox.XAxis)

    def linkedYChanged(self):
        view = self.linkedView(1)
        self.linkedViewChanged(view, ViewBox.YAxis)

    def linkedView(self, ax):
        v = self.state['linkedViews'][ax]
        if v is None or isinstance(v, basestring):
            return
        return v()

    def linkedViewChanged(self, view, axis):
        if self.linksBlocked or view is None:
            return
        vr = view.viewRect()
        vg = view.screenGeometry()
        sg = self.screenGeometry()
        if vg is None or sg is None:
            return
        view.blockLink(True)
        try:
            if axis == ViewBox.XAxis:
                overlap = min(sg.right(), vg.right()) - max(sg.left(), vg.left())
                if overlap < min(vg.width() / 3, sg.width() / 3):
                    x1 = vr.left()
                    x2 = vr.right()
                else:
                    upp = float(vr.width()) / vg.width()
                    if self.xInverted():
                        x1 = vr.left() + (sg.right() - vg.right()) * upp
                    else:
                        x1 = vr.left() + (sg.x() - vg.x()) * upp
                    x2 = x1 + sg.width() * upp
                self.enableAutoRange(ViewBox.XAxis, False)
                self.setXRange(x1, x2, padding=0)
            else:
                overlap = min(sg.bottom(), vg.bottom()) - max(sg.top(), vg.top())
                if overlap < min(vg.height() / 3, sg.height() / 3):
                    y1 = vr.top()
                    y2 = vr.bottom()
                else:
                    upp = float(vr.height()) / vg.height()
                    if self.yInverted():
                        y2 = vr.bottom() + (sg.bottom() - vg.bottom()) * upp
                    else:
                        y2 = vr.bottom() + (sg.top() - vg.top()) * upp
                    y1 = y2 - sg.height() * upp
                self.enableAutoRange(ViewBox.YAxis, False)
                self.setYRange(y1, y2, padding=0)
        finally:
            view.blockLink(False)

    def screenGeometry(self):
        """return the screen geometry of the viewbox"""
        v = self.getViewWidget()
        if v is None:
            return
        b = self.sceneBoundingRect()
        wr = v.mapFromScene(b).boundingRect()
        pos = v.mapToGlobal(v.pos())
        wr.adjust(pos.x(), pos.y(), pos.x(), pos.y())
        return wr

    def itemsChanged(self):
        self.updateAutoRange()

    def itemBoundsChanged(self, item):
        self._itemBoundsCache.pop(item, None)
        if self.state['autoRange'][0] is not False or self.state['autoRange'][1] is not False:
            self._autoRangeNeedsUpdate = True
            self.update()

    def invertY(self, b=True):
        """
        By default, the positive y-axis points upward on the screen. Use invertY(True) to reverse the y-axis.
        """
        if self.state['yInverted'] == b:
            return
        self.state['yInverted'] = b
        self._matrixNeedsUpdate = True
        self.updateViewRange()
        self.sigStateChanged.emit(self)
        self.sigYRangeChanged.emit(self, tuple(self.state['viewRange'][1]))

    def yInverted(self):
        return self.state['yInverted']

    def invertX(self, b=True):
        """
        By default, the positive x-axis points rightward on the screen. Use invertX(True) to reverse the x-axis.
        """
        if self.state['xInverted'] == b:
            return
        self.state['xInverted'] = b
        self.updateViewRange()
        self.sigStateChanged.emit(self)
        self.sigXRangeChanged.emit(self, tuple(self.state['viewRange'][0]))

    def xInverted(self):
        return self.state['xInverted']

    def setAspectLocked(self, lock=True, ratio=1):
        """
        If the aspect ratio is locked, view scaling must always preserve the aspect ratio.
        By default, the ratio is set to 1; x and y both have the same scaling.
        This ratio can be overridden (xScale/yScale), or use None to lock in the current ratio.
        """
        if not lock:
            if self.state['aspectLocked'] == False:
                return
            self.state['aspectLocked'] = False
        else:
            rect = self.rect()
            vr = self.viewRect()
            if not rect.height() == 0:
                if vr.width() == 0 or vr.height() == 0:
                    currentRatio = 1.0
            else:
                currentRatio = rect.width() / float(rect.height()) / (vr.width() / vr.height())
            if ratio is None:
                ratio = currentRatio
            if self.state['aspectLocked'] == ratio:
                return
            self.state['aspectLocked'] = ratio
            if ratio != currentRatio:
                self.updateViewRange()
        self.updateAutoRange()
        self.updateViewRange()
        self.sigStateChanged.emit(self)

    def childTransform(self):
        """
        Return the transform that maps from child(item in the childGroup) coordinates to local coordinates.
        (This maps from inside the viewbox to outside)
        """
        if self._matrixNeedsUpdate:
            self.updateMatrix()
        m = self.childGroup.transform()
        return m

    def mapToView(self, obj):
        """Maps from the local coordinates of the ViewBox to the coordinate system displayed inside the ViewBox"""
        m = fn.invertQTransform(self.childTransform())
        return m.map(obj)

    def mapFromView(self, obj):
        """Maps from the coordinate system displayed inside the ViewBox to the local coordinates of the ViewBox"""
        m = self.childTransform()
        return m.map(obj)

    def mapSceneToView(self, obj):
        """Maps from scene coordinates to the coordinate system displayed inside the ViewBox"""
        return self.mapToView(self.mapFromScene(obj))

    def mapViewToScene(self, obj):
        """Maps from the coordinate system displayed inside the ViewBox to scene coordinates"""
        return self.mapToScene(self.mapFromView(obj))

    def mapFromItemToView(self, item, obj):
        """Maps *obj* from the local coordinate system of *item* to the view coordinates"""
        return self.childGroup.mapFromItem(item, obj)

    def mapFromViewToItem(self, item, obj):
        """Maps *obj* from view coordinates to the local coordinate system of *item*."""
        return self.childGroup.mapToItem(item, obj)

    def mapViewToDevice(self, obj):
        return self.mapToDevice(self.mapFromView(obj))

    def mapDeviceToView(self, obj):
        return self.mapToView(self.mapFromDevice(obj))

    def viewPixelSize(self):
        """Return the (width, height) of a screen pixel in view coordinates."""
        o = self.mapToView(Point(0, 0))
        px, py = [Point(self.mapToView(v) - o) for v in self.pixelVectors()]
        return (px.length(), py.length())

    def itemBoundingRect(self, item):
        """Return the bounding rect of the item in view coordinates"""
        return self.mapSceneToView(item.sceneBoundingRect()).boundingRect()

    def wheelEvent(self, ev, axis=None):
        mask = np.array((self.state['mouseEnabled']), dtype=(np.float))
        if axis is not None:
            if axis >= 0:
                if axis < len(mask):
                    mv = mask[axis]
                    mask[:] = 0
                    mask[axis] = mv
        s = (mask * 0.02 + 1) ** (ev.delta() * self.state['wheelScaleFactor'])
        center = Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos()))
        self._resetTarget()
        self.scaleBy(s, center)
        self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        ev.accept()

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            if self.menuEnabled():
                ev.accept()
                self.raiseContextMenu(ev)

    def raiseContextMenu(self, ev):
        menu = self.getMenu(ev)
        self.scene().addParentContextMenus(self, menu, ev)
        menu.popup(ev.screenPos().toPoint())

    def getMenu(self, ev):
        return self.menu

    def getContextMenus(self, event):
        if self.menuEnabled():
            return self.menu.actions()
        return []

    def mouseDragEvent(self, ev, axis=None):
        ev.accept()
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1
        mouseEnabled = np.array((self.state['mouseEnabled']), dtype=(np.float))
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0
        elif ev.button() & (QtCore.Qt.LeftButton | QtCore.Qt.MidButton):
            if self.state['mouseMode'] == ViewBox.RectMode:
                if ev.isFinish():
                    self.rbScaleBox.hide()
                    ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                    ax = self.childGroup.mapRectFromParent(ax)
                    self.showAxRect(ax)
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else:
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())
            else:
                tr = dif * mask
                tr = self.mapToView(tr) - self.mapToView(Point(0, 0))
                x = tr.x() if mask[0] == 1 else None
                y = tr.y() if mask[1] == 1 else None
                self._resetTarget()
                if x is not None or y is not None:
                    self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        else:
            if ev.button() & QtCore.Qt.RightButton:
                if self.state['aspectLocked'] is not False:
                    mask[0] = 0
                dif = ev.screenPos() - ev.lastScreenPos()
                dif = np.array([dif.x(), dif.y()])
                dif[0] *= -1
                s = (mask * 0.02 + 1) ** dif
                tr = self.childGroup.transform()
                tr = fn.invertQTransform(tr)
                x = s[0] if mouseEnabled[0] == 1 else None
                y = s[1] if mouseEnabled[1] == 1 else None
                center = Point(tr.map(ev.buttonDownPos(QtCore.Qt.RightButton)))
                self._resetTarget()
                self.scaleBy(x=x, y=y, center=center)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])

    def keyPressEvent(self, ev):
        """
        This routine should capture key presses in the current view box.
        Key presses are used only when mouse mode is RectMode
        The following events are implemented:
        ctrl-A : zooms out to the default "full" view of the plot
        ctrl-+ : moves forward in the zooming stack (if it exists)
        ctrl-- : moves backward in the zooming stack (if it exists)
         
        """
        ev.accept()
        if ev.text() == '-':
            self.scaleHistory(-1)
        else:
            if ev.text() in ('+', '='):
                self.scaleHistory(1)
            else:
                if ev.key() == QtCore.Qt.Key_Backspace:
                    self.scaleHistory(len(self.axHistory))
                else:
                    ev.ignore()

    def scaleHistory(self, d):
        if len(self.axHistory) == 0:
            return
        ptr = max(0, min(len(self.axHistory) - 1, self.axHistoryPointer + d))
        if ptr != self.axHistoryPointer:
            self.axHistoryPointer = ptr
            self.showAxRect(self.axHistory[ptr])

    def updateScaleBox(self, p1, p2):
        r = QtCore.QRectF(p1, p2)
        r = self.childGroup.mapRectFromParent(r)
        self.rbScaleBox.setPos(r.topLeft())
        self.rbScaleBox.resetTransform()
        self.rbScaleBox.scale(r.width(), r.height())
        self.rbScaleBox.show()

    def showAxRect(self, ax):
        self.setRange(ax.normalized())
        self.sigRangeChangedManually.emit(self.state['mouseEnabled'])

    def allChildren(self, item=None):
        """Return a list of all children and grandchildren of this ViewBox"""
        if item is None:
            item = self.childGroup
        children = [item]
        for ch in item.childItems():
            children.extend(self.allChildren(ch))

        return children

    def childrenBounds--- This code section failed: ---

 L.1371         0  LOAD_GLOBAL              debug
                2  LOAD_METHOD              Profiler
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  STORE_FAST               'profiler'

 L.1372         8  LOAD_FAST                'items'
               10  LOAD_CONST               None
               12  COMPARE_OP               is
               14  POP_JUMP_IF_FALSE    22  'to 22'

 L.1373        16  LOAD_FAST                'self'
               18  LOAD_ATTR                addedItems
               20  STORE_FAST               'items'
             22_0  COME_FROM            14  '14'

 L.1376        22  LOAD_LISTCOMP            '<code_object <listcomp>>'
               24  LOAD_STR                 'ViewBox.childrenBounds.<locals>.<listcomp>'
               26  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                childGroup
               32  LOAD_METHOD              pixelVectors
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  GET_ITER         
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'px'
               44  STORE_FAST               'py'

 L.1379        46  BUILD_LIST_0          0 
               48  STORE_FAST               'itemBounds'

 L.1380     50_52  SETUP_LOOP          572  'to 572'
               54  LOAD_FAST                'items'
               56  GET_ITER         
             58_0  COME_FROM           462  '462'
            58_60  FOR_ITER            570  'to 570'
               62  STORE_FAST               'item'

 L.1381        64  LOAD_FAST                'item'
               66  LOAD_METHOD              isVisible
               68  CALL_METHOD_0         0  '0 positional arguments'
               70  POP_JUMP_IF_TRUE     74  'to 74'

 L.1382        72  CONTINUE             58  'to 58'
             74_0  COME_FROM            70  '70'

 L.1384        74  LOAD_CONST               True
               76  STORE_FAST               'useX'

 L.1385        78  LOAD_CONST               True
               80  STORE_FAST               'useY'

 L.1387        82  LOAD_GLOBAL              hasattr
               84  LOAD_FAST                'item'
               86  LOAD_STR                 'dataBounds'
               88  CALL_FUNCTION_2       2  '2 positional arguments'
            90_92  POP_JUMP_IF_FALSE   498  'to 498'

 L.1390        94  LOAD_FAST                'frac'
               96  LOAD_CONST               None
               98  COMPARE_OP               is
              100  POP_JUMP_IF_FALSE   106  'to 106'

 L.1391       102  LOAD_CONST               (1.0, 1.0)
              104  STORE_FAST               'frac'
            106_0  COME_FROM           100  '100'

 L.1392       106  LOAD_FAST                'item'
              108  LOAD_ATTR                dataBounds
              110  LOAD_CONST               0
              112  LOAD_FAST                'frac'
              114  LOAD_CONST               0
              116  BINARY_SUBSCR    
              118  LOAD_FAST                'orthoRange'
              120  LOAD_CONST               0
              122  BINARY_SUBSCR    
              124  LOAD_CONST               ('frac', 'orthoRange')
              126  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              128  STORE_FAST               'xr'

 L.1393       130  LOAD_FAST                'item'
              132  LOAD_ATTR                dataBounds
              134  LOAD_CONST               1
              136  LOAD_FAST                'frac'
              138  LOAD_CONST               1
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'orthoRange'
              144  LOAD_CONST               1
              146  BINARY_SUBSCR    
              148  LOAD_CONST               ('frac', 'orthoRange')
              150  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              152  STORE_FAST               'yr'

 L.1394       154  LOAD_GLOBAL              hasattr
              156  LOAD_FAST                'item'
              158  LOAD_STR                 'pixelPadding'
              160  CALL_FUNCTION_2       2  '2 positional arguments'
              162  POP_JUMP_IF_TRUE    168  'to 168'
              164  LOAD_CONST               0
              166  JUMP_FORWARD        174  'to 174'
            168_0  COME_FROM           162  '162'
              168  LOAD_FAST                'item'
              170  LOAD_METHOD              pixelPadding
              172  CALL_METHOD_0         0  '0 positional arguments'
            174_0  COME_FROM           166  '166'
              174  STORE_FAST               'pxPad'

 L.1395       176  LOAD_FAST                'xr'
              178  LOAD_CONST               None
              180  COMPARE_OP               is
              182  POP_JUMP_IF_TRUE    236  'to 236'
              184  LOAD_FAST                'xr'
              186  LOAD_CONST               0
              188  BINARY_SUBSCR    
              190  LOAD_CONST               None
              192  COMPARE_OP               is
              194  POP_JUMP_IF_FALSE   208  'to 208'
              196  LOAD_FAST                'xr'
              198  LOAD_CONST               1
              200  BINARY_SUBSCR    
              202  LOAD_CONST               None
              204  COMPARE_OP               is
              206  POP_JUMP_IF_TRUE    236  'to 236'
            208_0  COME_FROM           194  '194'
              208  LOAD_GLOBAL              np
              210  LOAD_METHOD              isnan
              212  LOAD_FAST                'xr'
              214  CALL_METHOD_1         1  '1 positional argument'
              216  LOAD_METHOD              any
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  POP_JUMP_IF_TRUE    236  'to 236'
              222  LOAD_GLOBAL              np
              224  LOAD_METHOD              isinf
              226  LOAD_FAST                'xr'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  LOAD_METHOD              any
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  POP_JUMP_IF_FALSE   244  'to 244'
            236_0  COME_FROM           220  '220'
            236_1  COME_FROM           206  '206'
            236_2  COME_FROM           182  '182'

 L.1396       236  LOAD_CONST               False
              238  STORE_FAST               'useX'

 L.1397       240  LOAD_CONST               (0, 0)
              242  STORE_FAST               'xr'
            244_0  COME_FROM           234  '234'

 L.1398       244  LOAD_FAST                'yr'
              246  LOAD_CONST               None
              248  COMPARE_OP               is
          250_252  POP_JUMP_IF_TRUE    314  'to 314'
              254  LOAD_FAST                'yr'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_CONST               None
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_FALSE   282  'to 282'
              268  LOAD_FAST                'yr'
              270  LOAD_CONST               1
              272  BINARY_SUBSCR    
              274  LOAD_CONST               None
              276  COMPARE_OP               is
          278_280  POP_JUMP_IF_TRUE    314  'to 314'
            282_0  COME_FROM           264  '264'
              282  LOAD_GLOBAL              np
              284  LOAD_METHOD              isnan
              286  LOAD_FAST                'yr'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  LOAD_METHOD              any
              292  CALL_METHOD_0         0  '0 positional arguments'
          294_296  POP_JUMP_IF_TRUE    314  'to 314'
              298  LOAD_GLOBAL              np
              300  LOAD_METHOD              isinf
              302  LOAD_FAST                'yr'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  LOAD_METHOD              any
              308  CALL_METHOD_0         0  '0 positional arguments'
          310_312  POP_JUMP_IF_FALSE   322  'to 322'
            314_0  COME_FROM           294  '294'
            314_1  COME_FROM           278  '278'
            314_2  COME_FROM           250  '250'

 L.1399       314  LOAD_CONST               False
              316  STORE_FAST               'useY'

 L.1400       318  LOAD_CONST               (0, 0)
              320  STORE_FAST               'yr'
            322_0  COME_FROM           310  '310'

 L.1402       322  LOAD_GLOBAL              QtCore
              324  LOAD_METHOD              QRectF
              326  LOAD_FAST                'xr'
              328  LOAD_CONST               0
              330  BINARY_SUBSCR    
              332  LOAD_FAST                'yr'
              334  LOAD_CONST               0
              336  BINARY_SUBSCR    
              338  LOAD_FAST                'xr'
              340  LOAD_CONST               1
              342  BINARY_SUBSCR    
              344  LOAD_FAST                'xr'
              346  LOAD_CONST               0
              348  BINARY_SUBSCR    
              350  BINARY_SUBTRACT  
              352  LOAD_FAST                'yr'
              354  LOAD_CONST               1
              356  BINARY_SUBSCR    
              358  LOAD_FAST                'yr'
              360  LOAD_CONST               0
              362  BINARY_SUBSCR    
              364  BINARY_SUBTRACT  
              366  CALL_METHOD_4         4  '4 positional arguments'
              368  STORE_FAST               'bounds'

 L.1403       370  LOAD_FAST                'self'
              372  LOAD_METHOD              mapFromItemToView
              374  LOAD_FAST                'item'
              376  LOAD_FAST                'bounds'
              378  CALL_METHOD_2         2  '2 positional arguments'
              380  LOAD_METHOD              boundingRect
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  STORE_FAST               'bounds'

 L.1405       386  LOAD_GLOBAL              any
              388  LOAD_FAST                'useX'
              390  LOAD_FAST                'useY'
              392  BUILD_LIST_2          2 
              394  CALL_FUNCTION_1       1  '1 positional argument'
          396_398  POP_JUMP_IF_TRUE    402  'to 402'

 L.1406       400  CONTINUE             58  'to 58'
            402_0  COME_FROM           396  '396'

 L.1409       402  LOAD_FAST                'useX'
              404  LOAD_FAST                'useY'
              406  COMPARE_OP               !=
          408_410  POP_JUMP_IF_FALSE   478  'to 478'

 L.1410       412  LOAD_GLOBAL              round
              414  LOAD_FAST                'item'
              416  LOAD_METHOD              transformAngle
              418  CALL_METHOD_0         0  '0 positional arguments'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  STORE_FAST               'ang'

 L.1411       424  LOAD_FAST                'ang'
              426  LOAD_CONST               0
              428  COMPARE_OP               ==
          430_432  POP_JUMP_IF_TRUE    478  'to 478'
              434  LOAD_FAST                'ang'
              436  LOAD_CONST               180
              438  COMPARE_OP               ==
          440_442  POP_JUMP_IF_FALSE   446  'to 446'

 L.1412       444  JUMP_FORWARD        478  'to 478'
            446_0  COME_FROM           440  '440'

 L.1413       446  LOAD_FAST                'ang'
              448  LOAD_CONST               90
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_TRUE    464  'to 464'
              456  LOAD_FAST                'ang'
              458  LOAD_CONST               270
              460  COMPARE_OP               ==
              462  POP_JUMP_IF_FALSE    58  'to 58'
            464_0  COME_FROM           452  '452'

 L.1414       464  LOAD_FAST                'useY'
              466  LOAD_FAST                'useX'
              468  ROT_TWO          
              470  STORE_FAST               'useX'
              472  STORE_FAST               'useY'
              474  JUMP_FORWARD        478  'to 478'

 L.1418       476  CONTINUE             58  'to 58'
            478_0  COME_FROM           474  '474'
            478_1  COME_FROM           444  '444'
            478_2  COME_FROM           430  '430'
            478_3  COME_FROM           408  '408'

 L.1421       478  LOAD_FAST                'itemBounds'
              480  LOAD_METHOD              append
              482  LOAD_FAST                'bounds'
              484  LOAD_FAST                'useX'
              486  LOAD_FAST                'useY'
              488  LOAD_FAST                'pxPad'
              490  BUILD_TUPLE_4         4 
              492  CALL_METHOD_1         1  '1 positional argument'
              494  POP_TOP          
              496  JUMP_BACK            58  'to 58'
            498_0  COME_FROM            90  '90'

 L.1426       498  LOAD_GLOBAL              int
              500  LOAD_FAST                'item'
              502  LOAD_METHOD              flags
              504  CALL_METHOD_0         0  '0 positional arguments'
              506  LOAD_FAST                'item'
              508  LOAD_ATTR                ItemHasNoContents
              510  BINARY_AND       
              512  CALL_FUNCTION_1       1  '1 positional argument'
              514  LOAD_CONST               0
              516  COMPARE_OP               >
          518_520  POP_JUMP_IF_FALSE   526  'to 526'

 L.1427       522  CONTINUE             58  'to 58'
              524  JUMP_FORWARD        534  'to 534'
            526_0  COME_FROM           518  '518'

 L.1429       526  LOAD_FAST                'item'
              528  LOAD_METHOD              boundingRect
              530  CALL_METHOD_0         0  '0 positional arguments'
              532  STORE_FAST               'bounds'
            534_0  COME_FROM           524  '524'

 L.1430       534  LOAD_FAST                'self'
              536  LOAD_METHOD              mapFromItemToView
              538  LOAD_FAST                'item'
              540  LOAD_FAST                'bounds'
              542  CALL_METHOD_2         2  '2 positional arguments'
              544  LOAD_METHOD              boundingRect
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  STORE_FAST               'bounds'

 L.1431       550  LOAD_FAST                'itemBounds'
              552  LOAD_METHOD              append
              554  LOAD_FAST                'bounds'
              556  LOAD_CONST               True
              558  LOAD_CONST               True
              560  LOAD_CONST               0
              562  BUILD_TUPLE_4         4 
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          
              568  JUMP_BACK            58  'to 58'
              570  POP_BLOCK        
            572_0  COME_FROM_LOOP       50  '50'

 L.1436       572  LOAD_CONST               None
              574  LOAD_CONST               None
              576  BUILD_LIST_2          2 
              578  STORE_FAST               'range'

 L.1437       580  SETUP_LOOP          790  'to 790'
              582  LOAD_FAST                'itemBounds'
              584  GET_ITER         
              586  FOR_ITER            788  'to 788'
              588  UNPACK_SEQUENCE_4     4 
              590  STORE_FAST               'bounds'
              592  STORE_FAST               'useX'
              594  STORE_FAST               'useY'
              596  STORE_FAST               'px'

 L.1438       598  LOAD_FAST                'useY'
          600_602  POP_JUMP_IF_FALSE   688  'to 688'

 L.1439       604  LOAD_FAST                'range'
              606  LOAD_CONST               1
              608  BINARY_SUBSCR    
              610  LOAD_CONST               None
              612  COMPARE_OP               is-not
          614_616  POP_JUMP_IF_FALSE   668  'to 668'

 L.1440       618  LOAD_GLOBAL              min
              620  LOAD_FAST                'bounds'
              622  LOAD_METHOD              top
              624  CALL_METHOD_0         0  '0 positional arguments'
              626  LOAD_FAST                'range'
              628  LOAD_CONST               1
              630  BINARY_SUBSCR    
              632  LOAD_CONST               0
              634  BINARY_SUBSCR    
              636  CALL_FUNCTION_2       2  '2 positional arguments'
              638  LOAD_GLOBAL              max
              640  LOAD_FAST                'bounds'
              642  LOAD_METHOD              bottom
              644  CALL_METHOD_0         0  '0 positional arguments'
              646  LOAD_FAST                'range'
              648  LOAD_CONST               1
              650  BINARY_SUBSCR    
              652  LOAD_CONST               1
              654  BINARY_SUBSCR    
              656  CALL_FUNCTION_2       2  '2 positional arguments'
              658  BUILD_LIST_2          2 
              660  LOAD_FAST                'range'
              662  LOAD_CONST               1
              664  STORE_SUBSCR     
              666  JUMP_FORWARD        688  'to 688'
            668_0  COME_FROM           614  '614'

 L.1442       668  LOAD_FAST                'bounds'
              670  LOAD_METHOD              top
              672  CALL_METHOD_0         0  '0 positional arguments'
              674  LOAD_FAST                'bounds'
              676  LOAD_METHOD              bottom
              678  CALL_METHOD_0         0  '0 positional arguments'
              680  BUILD_LIST_2          2 
              682  LOAD_FAST                'range'
              684  LOAD_CONST               1
              686  STORE_SUBSCR     
            688_0  COME_FROM           666  '666'
            688_1  COME_FROM           600  '600'

 L.1443       688  LOAD_FAST                'useX'
          690_692  POP_JUMP_IF_FALSE   778  'to 778'

 L.1444       694  LOAD_FAST                'range'
              696  LOAD_CONST               0
              698  BINARY_SUBSCR    
              700  LOAD_CONST               None
              702  COMPARE_OP               is-not
          704_706  POP_JUMP_IF_FALSE   758  'to 758'

 L.1445       708  LOAD_GLOBAL              min
              710  LOAD_FAST                'bounds'
              712  LOAD_METHOD              left
              714  CALL_METHOD_0         0  '0 positional arguments'
              716  LOAD_FAST                'range'
              718  LOAD_CONST               0
              720  BINARY_SUBSCR    
              722  LOAD_CONST               0
              724  BINARY_SUBSCR    
              726  CALL_FUNCTION_2       2  '2 positional arguments'
              728  LOAD_GLOBAL              max
              730  LOAD_FAST                'bounds'
              732  LOAD_METHOD              right
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  LOAD_FAST                'range'
              738  LOAD_CONST               0
              740  BINARY_SUBSCR    
              742  LOAD_CONST               1
              744  BINARY_SUBSCR    
              746  CALL_FUNCTION_2       2  '2 positional arguments'
              748  BUILD_LIST_2          2 
              750  LOAD_FAST                'range'
              752  LOAD_CONST               0
              754  STORE_SUBSCR     
              756  JUMP_FORWARD        778  'to 778'
            758_0  COME_FROM           704  '704'

 L.1447       758  LOAD_FAST                'bounds'
              760  LOAD_METHOD              left
              762  CALL_METHOD_0         0  '0 positional arguments'
              764  LOAD_FAST                'bounds'
              766  LOAD_METHOD              right
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  BUILD_LIST_2          2 
              772  LOAD_FAST                'range'
              774  LOAD_CONST               0
              776  STORE_SUBSCR     
            778_0  COME_FROM           756  '756'
            778_1  COME_FROM           690  '690'

 L.1448       778  LOAD_FAST                'profiler'
              780  CALL_FUNCTION_0       0  '0 positional arguments'
              782  POP_TOP          
          784_786  JUMP_BACK           586  'to 586'
              788  POP_BLOCK        
            790_0  COME_FROM_LOOP      580  '580'

 L.1455       790  LOAD_FAST                'self'
              792  LOAD_METHOD              width
              794  CALL_METHOD_0         0  '0 positional arguments'
              796  STORE_FAST               'w'

 L.1456       798  LOAD_FAST                'self'
              800  LOAD_METHOD              height
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  STORE_FAST               'h'

 L.1458       806  LOAD_FAST                'w'
              808  LOAD_CONST               0
              810  COMPARE_OP               >
          812_814  POP_JUMP_IF_FALSE   978  'to 978'
              816  LOAD_FAST                'range'
              818  LOAD_CONST               0
              820  BINARY_SUBSCR    
              822  LOAD_CONST               None
              824  COMPARE_OP               is-not
          826_828  POP_JUMP_IF_FALSE   978  'to 978'

 L.1459       830  LOAD_FAST                'range'
              832  LOAD_CONST               0
              834  BINARY_SUBSCR    
              836  LOAD_CONST               1
              838  BINARY_SUBSCR    
              840  LOAD_FAST                'range'
              842  LOAD_CONST               0
              844  BINARY_SUBSCR    
              846  LOAD_CONST               0
              848  BINARY_SUBSCR    
              850  BINARY_SUBTRACT  
              852  LOAD_FAST                'w'
              854  BINARY_TRUE_DIVIDE
              856  STORE_FAST               'pxSize'

 L.1460       858  SETUP_LOOP          978  'to 978'
              860  LOAD_FAST                'itemBounds'
              862  GET_ITER         
            864_0  COME_FROM           882  '882'
              864  FOR_ITER            976  'to 976'
              866  UNPACK_SEQUENCE_4     4 
              868  STORE_FAST               'bounds'
              870  STORE_FAST               'useX'
              872  STORE_FAST               'useY'
              874  STORE_FAST               'px'

 L.1461       876  LOAD_FAST                'px'
              878  LOAD_CONST               0
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_TRUE    864  'to 864'
              886  LOAD_FAST                'useX'
          888_890  POP_JUMP_IF_TRUE    896  'to 896'

 L.1462   892_894  CONTINUE            864  'to 864'
            896_0  COME_FROM           888  '888'

 L.1463       896  LOAD_GLOBAL              min
              898  LOAD_FAST                'range'
              900  LOAD_CONST               0
              902  BINARY_SUBSCR    
              904  LOAD_CONST               0
              906  BINARY_SUBSCR    
              908  LOAD_FAST                'bounds'
              910  LOAD_METHOD              left
              912  CALL_METHOD_0         0  '0 positional arguments'
              914  LOAD_FAST                'px'
              916  LOAD_FAST                'pxSize'
              918  BINARY_MULTIPLY  
              920  BINARY_SUBTRACT  
              922  CALL_FUNCTION_2       2  '2 positional arguments'
              924  LOAD_FAST                'range'
              926  LOAD_CONST               0
              928  BINARY_SUBSCR    
              930  LOAD_CONST               0
              932  STORE_SUBSCR     

 L.1464       934  LOAD_GLOBAL              max
              936  LOAD_FAST                'range'
              938  LOAD_CONST               0
              940  BINARY_SUBSCR    
              942  LOAD_CONST               1
              944  BINARY_SUBSCR    
              946  LOAD_FAST                'bounds'
              948  LOAD_METHOD              right
              950  CALL_METHOD_0         0  '0 positional arguments'
              952  LOAD_FAST                'px'
              954  LOAD_FAST                'pxSize'
              956  BINARY_MULTIPLY  
              958  BINARY_ADD       
              960  CALL_FUNCTION_2       2  '2 positional arguments'
              962  LOAD_FAST                'range'
              964  LOAD_CONST               0
              966  BINARY_SUBSCR    
              968  LOAD_CONST               1
              970  STORE_SUBSCR     
          972_974  JUMP_BACK           864  'to 864'
              976  POP_BLOCK        
            978_0  COME_FROM_LOOP      858  '858'
            978_1  COME_FROM           826  '826'
            978_2  COME_FROM           812  '812'

 L.1465       978  LOAD_FAST                'h'
              980  LOAD_CONST               0
              982  COMPARE_OP               >
          984_986  POP_JUMP_IF_FALSE  1150  'to 1150'
              988  LOAD_FAST                'range'
              990  LOAD_CONST               1
              992  BINARY_SUBSCR    
              994  LOAD_CONST               None
              996  COMPARE_OP               is-not
         998_1000  POP_JUMP_IF_FALSE  1150  'to 1150'

 L.1466      1002  LOAD_FAST                'range'
             1004  LOAD_CONST               1
             1006  BINARY_SUBSCR    
             1008  LOAD_CONST               1
             1010  BINARY_SUBSCR    
             1012  LOAD_FAST                'range'
             1014  LOAD_CONST               1
             1016  BINARY_SUBSCR    
             1018  LOAD_CONST               0
             1020  BINARY_SUBSCR    
             1022  BINARY_SUBTRACT  
             1024  LOAD_FAST                'h'
             1026  BINARY_TRUE_DIVIDE
             1028  STORE_FAST               'pxSize'

 L.1467      1030  SETUP_LOOP         1150  'to 1150'
             1032  LOAD_FAST                'itemBounds'
             1034  GET_ITER         
           1036_0  COME_FROM          1054  '1054'
             1036  FOR_ITER           1148  'to 1148'
             1038  UNPACK_SEQUENCE_4     4 
             1040  STORE_FAST               'bounds'
             1042  STORE_FAST               'useX'
             1044  STORE_FAST               'useY'
             1046  STORE_FAST               'px'

 L.1468      1048  LOAD_FAST                'px'
             1050  LOAD_CONST               0
             1052  COMPARE_OP               ==
         1054_1056  POP_JUMP_IF_TRUE   1036  'to 1036'
             1058  LOAD_FAST                'useY'
         1060_1062  POP_JUMP_IF_TRUE   1068  'to 1068'

 L.1469  1064_1066  CONTINUE           1036  'to 1036'
           1068_0  COME_FROM          1060  '1060'

 L.1470      1068  LOAD_GLOBAL              min
             1070  LOAD_FAST                'range'
             1072  LOAD_CONST               1
             1074  BINARY_SUBSCR    
             1076  LOAD_CONST               0
             1078  BINARY_SUBSCR    
             1080  LOAD_FAST                'bounds'
             1082  LOAD_METHOD              top
             1084  CALL_METHOD_0         0  '0 positional arguments'
             1086  LOAD_FAST                'px'
             1088  LOAD_FAST                'pxSize'
             1090  BINARY_MULTIPLY  
             1092  BINARY_SUBTRACT  
             1094  CALL_FUNCTION_2       2  '2 positional arguments'
             1096  LOAD_FAST                'range'
             1098  LOAD_CONST               1
             1100  BINARY_SUBSCR    
             1102  LOAD_CONST               0
             1104  STORE_SUBSCR     

 L.1471      1106  LOAD_GLOBAL              max
             1108  LOAD_FAST                'range'
             1110  LOAD_CONST               1
             1112  BINARY_SUBSCR    
             1114  LOAD_CONST               1
             1116  BINARY_SUBSCR    
             1118  LOAD_FAST                'bounds'
             1120  LOAD_METHOD              bottom
             1122  CALL_METHOD_0         0  '0 positional arguments'
             1124  LOAD_FAST                'px'
             1126  LOAD_FAST                'pxSize'
             1128  BINARY_MULTIPLY  
             1130  BINARY_ADD       
             1132  CALL_FUNCTION_2       2  '2 positional arguments'
             1134  LOAD_FAST                'range'
             1136  LOAD_CONST               1
             1138  BINARY_SUBSCR    
             1140  LOAD_CONST               1
             1142  STORE_SUBSCR     
         1144_1146  JUMP_BACK          1036  'to 1036'
             1148  POP_BLOCK        
           1150_0  COME_FROM_LOOP     1030  '1030'
           1150_1  COME_FROM           998  '998'
           1150_2  COME_FROM           984  '984'

 L.1473      1150  LOAD_FAST                'range'
             1152  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 244_0

    def childrenBoundingRect(self, *args, **kwds):
        range = (self.childrenBounds)(*args, **kwds)
        tr = self.targetRange()
        if range[0] is None:
            range[0] = tr[0]
        if range[1] is None:
            range[1] = tr[1]
        bounds = QtCore.QRectF(range[0][0], range[1][0], range[0][1] - range[0][0], range[1][1] - range[1][0])
        return bounds

    def updateViewRange(self, forceX=False, forceY=False):
        viewRange = [
         self.state['targetRange'][0][:], self.state['targetRange'][1][:]]
        changed = [False, False]
        aspect = self.state['aspectLocked']
        tr = self.targetRect()
        bounds = self.rect()
        if aspect is not False:
            if 0 not in [aspect, tr.height(), bounds.height(), bounds.width()]:
                targetRatio = tr.width() / tr.height() if tr.height() != 0 else 1
                viewRatio = (bounds.width() / bounds.height() if bounds.height() != 0 else 1) / aspect
                viewRatio = 1 if viewRatio == 0 else viewRatio
                if forceX:
                    ax = 0
                else:
                    if forceY:
                        ax = 1
                    else:
                        ax = 0 if targetRatio > viewRatio else 1
                if ax == 0:
                    dy = 0.5 * (tr.width() / viewRatio - tr.height())
                    if dy != 0:
                        changed[1] = True
                    viewRange[1] = [
                     self.state['targetRange'][1][0] - dy, self.state['targetRange'][1][1] + dy]
                else:
                    dx = 0.5 * (tr.height() * viewRatio - tr.width())
                    if dx != 0:
                        changed[0] = True
                    viewRange[0] = [
                     self.state['targetRange'][0][0] - dx, self.state['targetRange'][0][1] + dx]
        limits = (
         self.state['limits']['xLimits'], self.state['limits']['yLimits'])
        minRng = [self.state['limits']['xRange'][0], self.state['limits']['yRange'][0]]
        maxRng = [self.state['limits']['xRange'][1], self.state['limits']['yRange'][1]]
        for axis in (0, 1):
            if limits[axis][0] is None and limits[axis][1] is None and minRng[axis] is None:
                if maxRng[axis] is None:
                    continue
                elif limits[axis][0] is not None:
                    if limits[axis][1] is not None:
                        if maxRng[axis] is not None:
                            maxRng[axis] = min(maxRng[axis], limits[axis][1] - limits[axis][0])
                        else:
                            maxRng[axis] = limits[axis][1] - limits[axis][0]
                else:
                    diff = viewRange[axis][1] - viewRange[axis][0]
                    if maxRng[axis] is not None and diff > maxRng[axis]:
                        delta = maxRng[axis] - diff
                        changed[axis] = True
                    else:
                        if minRng[axis] is not None and diff < minRng[axis]:
                            delta = minRng[axis] - diff
                            changed[axis] = True
                        else:
                            delta = 0
                    viewRange[axis][0] -= delta / 2.0
                    viewRange[axis][1] += delta / 2.0
                    mn, mx = limits[axis]
                    if mn is not None and viewRange[axis][0] < mn:
                        delta = mn - viewRange[axis][0]
                        viewRange[axis][0] += delta
                        viewRange[axis][1] += delta
                        changed[axis] = True
                if mx is not None and viewRange[axis][1] > mx:
                    delta = mx - viewRange[axis][1]
                    viewRange[axis][0] += delta
                    viewRange[axis][1] += delta
                    changed[axis] = True

        changed = [viewRange[i][0] != self.state['viewRange'][i][0] or viewRange[i][1] != self.state['viewRange'][i][1] for i in (0,
                                                                                                                                  1)]
        self.state['viewRange'] = viewRange
        if changed[0]:
            self.sigXRangeChanged.emit(self, tuple(self.state['viewRange'][0]))
        if changed[1]:
            self.sigYRangeChanged.emit(self, tuple(self.state['viewRange'][1]))
        if any(changed):
            self.sigRangeChanged.emit(self, self.state['viewRange'])
            self.update()
            self._matrixNeedsUpdate = True
            for ax in (0, 1):
                if not changed[ax]:
                    continue
                link = self.linkedView(ax)
                if link is not None:
                    link.linkedViewChanged(self, ax)

    def updateMatrix(self, changed=None):
        bounds = self.rect()
        vr = self.viewRect()
        if vr.height() == 0 or vr.width() == 0:
            return
        scale = Point(bounds.width() / vr.width(), bounds.height() / vr.height())
        if not self.state['yInverted']:
            scale = scale * Point(1, -1)
        if self.state['xInverted']:
            scale = scale * Point(-1, 1)
        m = QtGui.QTransform()
        center = bounds.center()
        m.translate(center.x(), center.y())
        m.scale(scale[0], scale[1])
        st = Point(vr.center())
        m.translate(-st[0], -st[1])
        self.childGroup.setTransform(m)
        self.sigTransformChanged.emit(self)
        self._matrixNeedsUpdate = False

    def paint(self, p, opt, widget):
        self.checkSceneChange()
        if self.border is not None:
            bounds = self.shape()
            p.setPen(self.border)
            p.drawPath(bounds)

    def updateBackground(self):
        bg = self.state['background']
        if bg is None:
            self.background.hide()
        else:
            self.background.show()
            self.background.setBrush(fn.mkBrush(bg))

    def updateViewLists(self):
        try:
            self.window()
        except RuntimeError:
            return
        else:

            def cmpViews(a, b):
                wins = 100 * cmp(a.window() is self.window(), b.window() is self.window())
                alpha = cmp(a.name, b.name)
                return wins + alpha

            nv = list(ViewBox.NamedViews.values())
            sortList(nv, cmpViews)
            if self in nv:
                nv.remove(self)
            self.menu.setViewList(nv)
            for ax in (0, 1):
                link = self.state['linkedViews'][ax]
                if isinstance(link, basestring):
                    for v in nv:
                        if link == v.name:
                            self.linkView(ax, v)

    @staticmethod
    def updateAllViewLists():
        for v in ViewBox.AllViews:
            v.updateViewLists()

    @staticmethod
    def forgetView(vid, name):
        if ViewBox is None:
            return
        if QtGui.QApplication.instance() is None:
            return
        for v in list(ViewBox.AllViews.keys()):
            if id(v) == vid:
                ViewBox.AllViews.pop(v)
                break

        ViewBox.NamedViews.pop(name, None)
        ViewBox.updateAllViewLists()

    @staticmethod
    def quit():
        for k in ViewBox.AllViews:
            if isQObjectAlive(k):
                if getConfigOption('crashWarning'):
                    sys.stderr.write('Warning: ViewBox should be closed before application exit.\n')
            try:
                k.destroyed.disconnect()
            except RuntimeError:
                pass
            except TypeError:
                pass
            except AttributeError:
                pass

    def locate(self, item, timeout=3.0, children=False):
        """
        Temporarily display the bounding rect of an item and lines connecting to the center of the view.
        This is useful for determining the location of items that may be out of the range of the ViewBox.
        if allChildren is True, then the bounding rect of all item's children will be shown instead.
        """
        self.clearLocate()
        if item.scene() is not self.scene():
            raise Exception('Item does not share a scene with this ViewBox.')
        else:
            c = self.viewRect().center()
            if children:
                br = self.mapFromItemToView(item, item.childrenBoundingRect()).boundingRect()
            else:
                br = self.mapFromItemToView(item, item.boundingRect()).boundingRect()
            g = ItemGroup()
            g.setParentItem(self.childGroup)
            self.locateGroup = g
            g.box = QtGui.QGraphicsRectItem(br)
            g.box.setParentItem(g)
            g.lines = []
            for p in (br.topLeft(), br.bottomLeft(), br.bottomRight(), br.topRight()):
                line = QtGui.QGraphicsLineItem(c.x(), c.y(), p.x(), p.y())
                line.setParentItem(g)
                g.lines.append(line)

            for item in g.childItems():
                item.setPen(fn.mkPen(color='y', width=3))

            g.setZValue(1000000)
            if children:
                g.path = QtGui.QGraphicsPathItem(g.childrenShape())
            else:
                g.path = QtGui.QGraphicsPathItem(g.shape())
        g.path.setParentItem(g)
        g.path.setPen(fn.mkPen('g'))
        g.path.setZValue(100)
        QtCore.QTimer.singleShot(timeout * 1000, self.clearLocate)

    def clearLocate(self):
        if self.locateGroup is None:
            return
        self.scene().removeItem(self.locateGroup)
        self.locateGroup = None


from .ViewBoxMenu import ViewBoxMenu