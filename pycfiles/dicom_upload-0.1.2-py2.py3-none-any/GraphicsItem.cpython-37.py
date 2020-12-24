# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/GraphicsItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 23395 bytes
from ..Qt import QtGui, QtCore, isQObjectAlive
from ..GraphicsScene import GraphicsScene
from ..Point import Point
from .. import functions as fn
import weakref, operator
from util.lru_cache import LRUCache

class GraphicsItem(object):
    """GraphicsItem"""
    _pixelVectorGlobalCache = LRUCache(100, 70)

    def __init__(self, register=True):
        if not hasattr(self, '_qtBaseClass'):
            for b in self.__class__.__bases__:
                if issubclass(b, QtGui.QGraphicsItem):
                    self.__class__._qtBaseClass = b
                    break

        if not hasattr(self, '_qtBaseClass'):
            raise Exception('Could not determine Qt base class for GraphicsItem: %s' % str(self))
        self._pixelVectorCache = [None, None]
        self._viewWidget = None
        self._viewBox = None
        self._connectedView = None
        self._exportOpts = False
        if register:
            GraphicsScene.registerObject(self)

    def getViewWidget(self):
        """
        Return the view widget for this item. 
        
        If the scene has multiple views, only the first view is returned.
        The return value is cached; clear the cached value with forgetViewWidget().
        If the view has been deleted by Qt, return None.
        """
        if self._viewWidget is None:
            scene = self.scene()
            if scene is None:
                return
            views = scene.views()
            if len(views) < 1:
                return
            self._viewWidget = weakref.ref(self.scene().views()[0])
        v = self._viewWidget()
        if v is not None:
            if not isQObjectAlive(v):
                return
        return v

    def forgetViewWidget(self):
        self._viewWidget = None

    def getViewBox(self):
        """
        Return the first ViewBox or GraphicsView which bounds this item's visible space.
        If this item is not contained within a ViewBox, then the GraphicsView is returned.
        If the item is contained inside nested ViewBoxes, then the inner-most ViewBox is returned.
        The result is cached; clear the cache with forgetViewBox()
        """
        if self._viewBox is None:
            p = self
            while 1:
                try:
                    p = p.parentItem()
                except RuntimeError:
                    return
                else:
                    if p is None:
                        vb = self.getViewWidget()
                        if vb is None:
                            return
                        self._viewBox = weakref.ref(vb)
                        break
                    if hasattr(p, 'implements') and p.implements('ViewBox'):
                        self._viewBox = weakref.ref(p)
                        break

        return self._viewBox()

    def forgetViewBox(self):
        self._viewBox = None

    def deviceTransform(self, viewportTransform=None):
        """
        Return the transform that converts local item coordinates to device coordinates (usually pixels).
        Extends deviceTransform to automatically determine the viewportTransform.
        """
        if self._exportOpts is not False:
            if 'painter' in self._exportOpts:
                return self._exportOpts['painter'].deviceTransform() * self.sceneTransform()
        if viewportTransform is None:
            view = self.getViewWidget()
            if view is None:
                return
            viewportTransform = view.viewportTransform()
        dt = self._qtBaseClass.deviceTransform(self, viewportTransform)
        if dt.determinant() == 0:
            return
        return dt

    def viewTransform(self):
        """Return the transform that maps from local coordinates to the item's ViewBox coordinates
        If there is no ViewBox, return the scene transform.
        Returns None if the item does not have a view."""
        view = self.getViewBox()
        if view is None:
            return
        if hasattr(view, 'implements'):
            if view.implements('ViewBox'):
                tr = self.itemTransform(view.innerSceneItem())
                if isinstance(tr, tuple):
                    tr = tr[0]
                return tr
        return self.sceneTransform()

    def getBoundingParents(self):
        """Return a list of parents to this item that have child clipping enabled."""
        p = self
        parents = []
        while 1:
            p = p.parentItem()
            if p is None:
                break
            if p.flags() & self.ItemClipsChildrenToShape:
                parents.append(p)

        return parents

    def viewRect(self):
        """Return the bounds (in item coordinates) of this item's ViewBox or GraphicsWidget"""
        view = self.getViewBox()
        if view is None:
            return
        bounds = self.mapRectFromView(view.viewRect())
        if bounds is None:
            return
        bounds = bounds.normalized()
        return bounds

    def pixelVectors(self, direction=None):
        """Return vectors in local coordinates representing the width and height of a view pixel.
        If direction is specified, then return vectors parallel and orthogonal to it.
        
        Return (None, None) if pixel size is not yet defined (usually because the item has not yet been displayed)
        or if pixel size is below floating-point precision limit.
        """
        dt = self.deviceTransform()
        if dt is None:
            return (None, None)
        dt.setMatrix(dt.m11(), dt.m12(), 0, dt.m21(), dt.m22(), 0, 0, 0, 1)
        if direction is None:
            if dt == self._pixelVectorCache[0]:
                return tuple(map(Point, self._pixelVectorCache[1]))
        key = (
         dt.m11(), dt.m21(), dt.m12(), dt.m22())
        pv = self._pixelVectorGlobalCache.get(key, None)
        if direction is None:
            if pv is not None:
                self._pixelVectorCache = [
                 dt, pv]
                return tuple(map(Point, pv))
        if direction is None:
            direction = QtCore.QPointF(1, 0)
        if direction.manhattanLength() == 0:
            raise Exception('Cannot compute pixel length for 0-length vector.')
        directionr = direction
        dirLine = QtCore.QLineF(QtCore.QPointF(0, 0), directionr)
        viewDir = dt.map(dirLine)
        if viewDir.length() == 0:
            return (None, None)
        try:
            normView = viewDir.unitVector()
            normOrtho = normView.normalVector()
        except:
            raise Exception('Invalid direction %s' % directionr)

        dti = fn.invertQTransform(dt)
        pv = (
         Point(dti.map(normView).p2()), Point(dti.map(normOrtho).p2()))
        self._pixelVectorCache[1] = pv
        self._pixelVectorCache[0] = dt
        self._pixelVectorGlobalCache[key] = pv
        return self._pixelVectorCache[1]

    def pixelLength(self, direction, ortho=False):
        """Return the length of one pixel in the direction indicated (in local coordinates)
        If ortho=True, then return the length of one pixel orthogonal to the direction indicated.
        
        Return None if pixel size is not yet defined (usually because the item has not yet been displayed).
        """
        normV, orthoV = self.pixelVectors(direction)
        if normV == None or orthoV == None:
            return
        if ortho:
            return orthoV.length()
        return normV.length()

    def pixelSize(self):
        v = self.pixelVectors()
        if v == (None, None):
            return (None, None)
        return ((v[0].x() ** 2 + v[0].y() ** 2) ** 0.5, (v[1].x() ** 2 + v[1].y() ** 2) ** 0.5)

    def pixelWidth(self):
        vt = self.deviceTransform()
        if vt is None:
            return 0
        vt = fn.invertQTransform(vt)
        return vt.map(QtCore.QLineF(0, 0, 1, 0)).length()

    def pixelHeight(self):
        vt = self.deviceTransform()
        if vt is None:
            return 0
        vt = fn.invertQTransform(vt)
        return vt.map(QtCore.QLineF(0, 0, 0, 1)).length()

    def mapToDevice(self, obj):
        """
        Return *obj* mapped from local coordinates to device coordinates (pixels).
        If there is no device mapping available, return None.
        """
        vt = self.deviceTransform()
        if vt is None:
            return
        return vt.map(obj)

    def mapFromDevice(self, obj):
        """
        Return *obj* mapped from device coordinates (pixels) to local coordinates.
        If there is no device mapping available, return None.
        """
        vt = self.deviceTransform()
        if vt is None:
            return
        if isinstance(obj, QtCore.QPoint):
            obj = QtCore.QPointF(obj)
        vt = fn.invertQTransform(vt)
        return vt.map(obj)

    def mapRectToDevice(self, rect):
        """
        Return *rect* mapped from local coordinates to device coordinates (pixels).
        If there is no device mapping available, return None.
        """
        vt = self.deviceTransform()
        if vt is None:
            return
        return vt.mapRect(rect)

    def mapRectFromDevice(self, rect):
        """
        Return *rect* mapped from device coordinates (pixels) to local coordinates.
        If there is no device mapping available, return None.
        """
        vt = self.deviceTransform()
        if vt is None:
            return
        vt = fn.invertQTransform(vt)
        return vt.mapRect(rect)

    def mapToView(self, obj):
        vt = self.viewTransform()
        if vt is None:
            return
        return vt.map(obj)

    def mapRectToView(self, obj):
        vt = self.viewTransform()
        if vt is None:
            return
        return vt.mapRect(obj)

    def mapFromView(self, obj):
        vt = self.viewTransform()
        if vt is None:
            return
        vt = fn.invertQTransform(vt)
        return vt.map(obj)

    def mapRectFromView(self, obj):
        vt = self.viewTransform()
        if vt is None:
            return
        vt = fn.invertQTransform(vt)
        return vt.mapRect(obj)

    def pos(self):
        return Point(self._qtBaseClass.pos(self))

    def viewPos(self):
        return self.mapToView(self.mapFromParent(self.pos()))

    def parentItem(self):
        return GraphicsScene.translateGraphicsItem(self._qtBaseClass.parentItem(self))

    def setParentItem(self, parent):
        if parent is not None:
            pscene = parent.scene()
            if pscene is not None:
                if self.scene() is not pscene:
                    pscene.addItem(self)
        return self._qtBaseClass.setParentItem(self, parent)

    def childItems(self):
        return list(map(GraphicsScene.translateGraphicsItem, self._qtBaseClass.childItems(self)))

    def sceneTransform(self):
        if self.scene() is None:
            return self.transform()
        return self._qtBaseClass.sceneTransform(self)

    def transformAngle(self, relativeItem=None):
        """Return the rotation produced by this item's transform (this assumes there is no shear in the transform)
        If relativeItem is given, then the angle is determined relative to that item.
        """
        if relativeItem is None:
            relativeItem = self.parentItem()
        tr = self.itemTransform(relativeItem)
        if isinstance(tr, tuple):
            tr = tr[0]
        vec = tr.map(QtCore.QLineF(0, 0, 1, 0))
        return vec.angleTo(QtCore.QLineF(vec.p1(), vec.p1() + QtCore.QPointF(1, 0)))

    def parentChanged(self):
        """Called when the item's parent has changed. 
        This method handles connecting / disconnecting from ViewBox signals
        to make sure viewRangeChanged works properly. It should generally be 
        extended, not overridden."""
        self._updateView()

    def _updateView(self):
        self.forgetViewBox()
        self.forgetViewWidget()
        view = self.getViewBox()
        oldView = None
        if self._connectedView is not None:
            oldView = self._connectedView()
        if view is oldView:
            return
        if oldView is not None:
            for signal, slot in [('sigRangeChanged', self.viewRangeChanged), ('sigDeviceRangeChanged', self.viewRangeChanged),
             (
              'sigTransformChanged', self.viewTransformChanged),
             (
              'sigDeviceTransformChanged', self.viewTransformChanged)]:
                try:
                    getattr(oldView, signal).disconnect(slot)
                except (TypeError, AttributeError, RuntimeError):
                    pass

            self._connectedView = None
        if view is not None:
            if hasattr(view, 'sigDeviceRangeChanged'):
                view.sigDeviceRangeChanged.connect(self.viewRangeChanged)
                view.sigDeviceTransformChanged.connect(self.viewTransformChanged)
            else:
                view.sigRangeChanged.connect(self.viewRangeChanged)
                view.sigTransformChanged.connect(self.viewTransformChanged)
            self._connectedView = weakref.ref(view)
            self.viewRangeChanged()
            self.viewTransformChanged()
        self._replaceView(oldView)
        self.viewChanged(view, oldView)

    def viewChanged(self, view, oldView):
        """Called when this item's view has changed
        (ie, the item has been added to or removed from a ViewBox)"""
        pass

    def _replaceView(self, oldView, item=None):
        if item is None:
            item = self
        for child in item.childItems():
            if isinstance(child, GraphicsItem):
                if child.getViewBox() is oldView:
                    child._updateView()
            else:
                self._replaceView(oldView, child)

    def viewRangeChanged(self):
        """
        Called whenever the view coordinates of the ViewBox containing this item have changed.
        """
        pass

    def viewTransformChanged(self):
        """
        Called whenever the transformation matrix of the view has changed.
        (eg, the view range has changed or the view was resized)
        """
        pass

    def informViewBoundsChanged(self):
        """
        Inform this item's container ViewBox that the bounds of this item have changed.
        This is used by ViewBox to react if auto-range is enabled.
        """
        view = self.getViewBox()
        if view is not None:
            if hasattr(view, 'implements'):
                if view.implements('ViewBox'):
                    view.itemBoundsChanged(self)

    def childrenShape(self):
        """Return the union of the shapes of all descendants of this item in local coordinates."""
        childs = self.allChildItems()
        shapes = [self.mapFromItem(c, c.shape()) for c in self.allChildItems()]
        return reduce(operator.add, shapes)

    def allChildItems(self, root=None):
        """Return list of the entire item tree descending from this item."""
        if root is None:
            root = self
        tree = []
        for ch in root.childItems():
            tree.append(ch)
            tree.extend(self.allChildItems(ch))

        return tree

    def setExportMode(self, export, opts=None):
        """
        This method is called by exporters to inform items that they are being drawn for export
        with a specific set of options. Items access these via self._exportOptions.
        When exporting is complete, _exportOptions is set to False.
        """
        if opts is None:
            opts = {}
        elif export:
            self._exportOpts = opts
        else:
            self._exportOpts = False

    def getContextMenus(self, event):
        if hasattr(self, 'getMenu'):
            return [self.getMenu()]
        return []