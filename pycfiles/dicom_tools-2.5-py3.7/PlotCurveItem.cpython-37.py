# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/PlotCurveItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 22481 bytes
from ..Qt import QtGui, QtCore
try:
    from ..Qt import QtOpenGL
    HAVE_OPENGL = True
except:
    HAVE_OPENGL = False

import numpy as np
from .GraphicsObject import GraphicsObject
from .. import functions as fn
from ..Point import Point
import struct, sys
from .. import getConfigOption
from .. import debug
__all__ = [
 'PlotCurveItem']

class PlotCurveItem(GraphicsObject):
    __doc__ = '\n    Class representing a single plot curve. Instances of this class are created\n    automatically as part of PlotDataItem; these rarely need to be instantiated\n    directly.\n    \n    Features:\n    \n    - Fast data update\n    - Fill under curve\n    - Mouse interaction\n    \n    ====================  ===============================================\n    **Signals:**\n    sigPlotChanged(self)  Emitted when the data being plotted has changed\n    sigClicked(self)      Emitted when the curve is clicked\n    ====================  ===============================================\n    '
    sigPlotChanged = QtCore.Signal(object)
    sigClicked = QtCore.Signal(object)

    def __init__(self, *args, **kargs):
        """
        Forwards all arguments to :func:`setData <pyqtgraph.PlotCurveItem.setData>`.
        
        Some extra arguments are accepted as well:
        
        ==============  =======================================================
        **Arguments:**
        parent          The parent GraphicsObject (optional)
        clickable       If True, the item will emit sigClicked when it is 
                        clicked on. Defaults to False.
        ==============  =======================================================
        """
        GraphicsObject.__init__(self, kargs.get('parent', None))
        self.clear()
        self.metaData = {}
        self.opts = {'pen':fn.mkPen('w'), 
         'shadowPen':None, 
         'fillLevel':None, 
         'brush':None, 
         'stepMode':False, 
         'name':None, 
         'antialias':getConfigOption('antialias'), 
         'connect':'all', 
         'mouseWidth':8}
        self.setClickable(kargs.get('clickable', False))
        (self.setData)(*args, **kargs)

    def implements(self, interface=None):
        ints = [
         'plotData']
        if interface is None:
            return ints
        return interface in ints

    def name(self):
        return self.opts.get('name', None)

    def setClickable(self, s, width=None):
        """Sets whether the item responds to mouse clicks.
        
        The *width* argument specifies the width in pixels orthogonal to the
        curve that will respond to a mouse click.
        """
        self.clickable = s
        if width is not None:
            self.opts['mouseWidth'] = width
            self._mouseShape = None
            self._boundingRect = None

    def getData(self):
        return (
         self.xData, self.yData)

    def dataBounds(self, ax, frac=1.0, orthoRange=None):
        cache = self._boundsCache[ax]
        if cache is not None:
            if cache[0] == (frac, orthoRange):
                return cache[1]
        x, y = self.getData()
        if x is None or len(x) == 0:
            return (None, None)
        if ax == 0:
            d = x
            d2 = y
        else:
            if ax == 1:
                d = y
                d2 = x
            elif orthoRange is not None:
                mask = (d2 >= orthoRange[0]) * (d2 <= orthoRange[1])
                d = d[mask]
            else:
                if len(d) == 0:
                    return (None, None)
                else:
                    if frac >= 1.0:
                        b = (
                         np.nanmin(d), np.nanmax(d))
                    else:
                        if frac <= 0.0:
                            raise Exception("Value for parameter 'frac' must be > 0. (got %s)" % str(frac))
                        else:
                            mask = np.isfinite(d)
                            d = d[mask]
                            b = np.percentile(d, [50 * (1 - frac), 50 * (1 + frac)])
                    if ax == 1:
                        if self.opts['fillLevel'] is not None:
                            b = (
                             min(b[0], self.opts['fillLevel']), max(b[1], self.opts['fillLevel']))
                    pen = self.opts['pen']
                    spen = self.opts['shadowPen']
                    b = pen.isCosmetic() or (
                     b[0] - pen.widthF() * 0.7072, b[1] + pen.widthF() * 0.7072)
                if spen is not None and not spen.isCosmetic():
                    if spen.style() != QtCore.Qt.NoPen:
                        b = (
                         b[0] - spen.widthF() * 0.7072, b[1] + spen.widthF() * 0.7072)
            self._boundsCache[ax] = [
             (
              frac, orthoRange), b]
            return b

    def pixelPadding(self):
        pen = self.opts['pen']
        spen = self.opts['shadowPen']
        w = 0
        if pen.isCosmetic():
            w += pen.widthF() * 0.7072
        if spen is not None:
            if spen.isCosmetic():
                if spen.style() != QtCore.Qt.NoPen:
                    w = max(w, spen.widthF() * 0.7072)
        if self.clickable:
            w = max(w, self.opts['mouseWidth'] // 2 + 1)
        return w

    def boundingRect(self):
        if self._boundingRect is None:
            xmn, xmx = self.dataBounds(ax=0)
            ymn, ymx = self.dataBounds(ax=1)
            if xmn is None:
                return QtCore.QRectF()
            px = py = 0.0
            pxPad = self.pixelPadding()
            if pxPad > 0:
                px, py = self.pixelVectors()
                try:
                    px = 0 if px is None else px.length()
                except OverflowError:
                    px = 0

                try:
                    py = 0 if py is None else py.length()
                except OverflowError:
                    py = 0

                px *= pxPad
                py *= pxPad
            self._boundingRect = QtCore.QRectF(xmn - px, ymn - py, 2 * px + xmx - xmn, 2 * py + ymx - ymn)
        return self._boundingRect

    def viewTransformChanged(self):
        self.invalidateBounds()
        self.prepareGeometryChange()

    def invalidateBounds(self):
        self._boundingRect = None
        self._boundsCache = [None, None]

    def setPen(self, *args, **kargs):
        """Set the pen used to draw the curve."""
        self.opts['pen'] = (fn.mkPen)(*args, **kargs)
        self.invalidateBounds()
        self.update()

    def setShadowPen(self, *args, **kargs):
        """Set the shadow pen used to draw behind tyhe primary pen.
        This pen must have a larger width than the primary 
        pen to be visible.
        """
        self.opts['shadowPen'] = (fn.mkPen)(*args, **kargs)
        self.invalidateBounds()
        self.update()

    def setBrush(self, *args, **kargs):
        """Set the brush used when filling the area under the curve"""
        self.opts['brush'] = (fn.mkBrush)(*args, **kargs)
        self.invalidateBounds()
        self.update()

    def setFillLevel(self, level):
        """Set the level filled to when filling under the curve"""
        self.opts['fillLevel'] = level
        self.fillPath = None
        self.invalidateBounds()
        self.update()

    def setData(self, *args, **kargs):
        """
        ==============  ========================================================
        **Arguments:**
        x, y            (numpy arrays) Data to show 
        pen             Pen to use when drawing. Any single argument accepted by
                        :func:`mkPen <pyqtgraph.mkPen>` is allowed.
        shadowPen       Pen for drawing behind the primary pen. Usually this
                        is used to emphasize the curve by providing a 
                        high-contrast border. Any single argument accepted by
                        :func:`mkPen <pyqtgraph.mkPen>` is allowed.
        fillLevel       (float or None) Fill the area 'under' the curve to
                        *fillLevel*
        brush           QBrush to use when filling. Any single argument accepted
                        by :func:`mkBrush <pyqtgraph.mkBrush>` is allowed.
        antialias       (bool) Whether to use antialiasing when drawing. This
                        is disabled by default because it decreases performance.
        stepMode        If True, two orthogonal lines are drawn for each sample
                        as steps. This is commonly used when drawing histograms.
                        Note that in this case, len(x) == len(y) + 1
        connect         Argument specifying how vertexes should be connected
                        by line segments. Default is "all", indicating full
                        connection. "pairs" causes only even-numbered segments
                        to be drawn. "finite" causes segments to be omitted if
                        they are attached to nan or inf values. For any other
                        connectivity, specify an array of boolean values.
        ==============  ========================================================
        
        If non-keyword arguments are used, they will be interpreted as
        setData(y) for a single argument and setData(x, y) for two
        arguments.
        
        
        """
        (self.updateData)(*args, **kargs)

    def updateData(self, *args, **kargs):
        profiler = debug.Profiler()
        if len(args) == 1:
            kargs['y'] = args[0]
        else:
            if len(args) == 2:
                kargs['x'] = args[0]
                kargs['y'] = args[1]
            elif not 'y' not in kargs:
                if kargs['y'] is None:
                    kargs['y'] = np.array([])
                if 'x' not in kargs or kargs['x'] is None:
                    kargs['x'] = np.arange(len(kargs['y']))
                for k in ('x', 'y'):
                    data = kargs[k]
                    if isinstance(data, list):
                        data = np.array(data)
                        kargs[k] = data
                    if isinstance(data, np.ndarray):
                        if data.ndim > 1:
                            raise Exception('Plot data must be 1D ndarray.')
                        if 'complex' in str(data.dtype):
                            raise Exception('Can not plot complex data types.')

                profiler('data checks')
                self.invalidateBounds()
                self.prepareGeometryChange()
                self.informViewBoundsChanged()
                self.yData = kargs['y'].view(np.ndarray)
                self.xData = kargs['x'].view(np.ndarray)
                profiler('copy')
                if 'stepMode' in kargs:
                    self.opts['stepMode'] = kargs['stepMode']
                if self.opts['stepMode'] is True:
                    if len(self.xData) != len(self.yData) + 1:
                        raise Exception('len(X) must be len(Y)+1 since stepMode=True (got %s and %s)' % (self.xData.shape, self.yData.shape))
            elif self.xData.shape != self.yData.shape:
                raise Exception('X and Y arrays must be the same shape--got %s and %s.' % (self.xData.shape, self.yData.shape))
            self.path = None
            self.fillPath = None
            self._mouseShape = None
            if 'name' in kargs:
                self.opts['name'] = kargs['name']
            if 'connect' in kargs:
                self.opts['connect'] = kargs['connect']
            if 'pen' in kargs:
                self.setPen(kargs['pen'])
            if 'shadowPen' in kargs:
                self.setShadowPen(kargs['shadowPen'])
            if 'fillLevel' in kargs:
                self.setFillLevel(kargs['fillLevel'])
            if 'brush' in kargs:
                self.setBrush(kargs['brush'])
            if 'antialias' in kargs:
                self.opts['antialias'] = kargs['antialias']
            profiler('set')
            self.update()
            profiler('update')
            self.sigPlotChanged.emit(self)
            profiler('emit')

    def generatePath(self, x, y):
        if self.opts['stepMode']:
            x2 = np.empty((len(x), 2), dtype=(x.dtype))
            x2[:] = x[:, np.newaxis]
            if self.opts['fillLevel'] is None:
                x = x2.reshape(x2.size)[1:-1]
                y2 = np.empty((len(y), 2), dtype=(y.dtype))
                y2[:] = y[:, np.newaxis]
                y = y2.reshape(y2.size)
            else:
                x = x2.reshape(x2.size)
                y2 = np.empty((len(y) + 2, 2), dtype=(y.dtype))
                y2[1:-1] = y[:, np.newaxis]
                y = y2.reshape(y2.size)[1:-1]
                y[0] = self.opts['fillLevel']
                y[-1] = self.opts['fillLevel']
        path = fn.arrayToQPath(x, y, connect=(self.opts['connect']))
        return path

    def getPath--- This code section failed: ---

 L. 399         0  LOAD_FAST                'self'
                2  LOAD_ATTR                path
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE   102  'to 102'

 L. 400        10  LOAD_FAST                'self'
               12  LOAD_METHOD              getData
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  UNPACK_SEQUENCE_2     2 
               18  STORE_FAST               'x'
               20  STORE_FAST               'y'

 L. 401        22  LOAD_FAST                'x'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     62  'to 62'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'x'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_CONST               0
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_TRUE     62  'to 62'
               42  LOAD_FAST                'y'
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_TRUE     62  'to 62'
               50  LOAD_GLOBAL              len
               52  LOAD_FAST                'y'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  LOAD_CONST               0
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    74  'to 74'
             62_0  COME_FROM            48  '48'
             62_1  COME_FROM            40  '40'
             62_2  COME_FROM            28  '28'

 L. 402        62  LOAD_GLOBAL              QtGui
               64  LOAD_METHOD              QPainterPath
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               path
               72  JUMP_FORWARD         90  'to 90'
             74_0  COME_FROM            60  '60'

 L. 404        74  LOAD_FAST                'self'
               76  LOAD_ATTR                generatePath
               78  LOAD_FAST                'self'
               80  LOAD_METHOD              getData
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  CALL_FUNCTION_EX      0  'positional arguments only'
               86  LOAD_FAST                'self'
               88  STORE_ATTR               path
             90_0  COME_FROM            72  '72'

 L. 405        90  LOAD_CONST               None
               92  LOAD_FAST                'self'
               94  STORE_ATTR               fillPath

 L. 406        96  LOAD_CONST               None
               98  LOAD_FAST                'self'
              100  STORE_ATTR               _mouseShape
            102_0  COME_FROM             8  '8'

 L. 408       102  LOAD_FAST                'self'
              104  LOAD_ATTR                path
              106  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 72

    @debug.warnOnException
    def paint(self, p, opt, widget):
        profiler = debug.Profiler()
        if self.xData is None or len(self.xData) == 0:
            return
        if HAVE_OPENGL:
            if getConfigOption('enableExperimental'):
                if isinstance(widget, QtOpenGL.QGLWidget):
                    self.paintGL(p, opt, widget)
                    return
        else:
            x = None
            y = None
            path = self.getPath()
            profiler('generate path')
            if self._exportOpts is not False:
                aa = self._exportOpts.get('antialias', True)
            else:
                aa = self.opts['antialias']
            p.setRenderHint(p.Antialiasing, aa)
            if self.opts['brush'] is not None and self.opts['fillLevel'] is not None:
                if self.fillPath is None:
                    if x is None:
                        x, y = self.getData()
                    p2 = QtGui.QPainterPath(self.path)
                    p2.lineTo(x[(-1)], self.opts['fillLevel'])
                    p2.lineTo(x[0], self.opts['fillLevel'])
                    p2.lineTo(x[0], y[0])
                    p2.closeSubpath()
                    self.fillPath = p2
                profiler('generate fill path')
                p.fillPath(self.fillPath, self.opts['brush'])
                profiler('draw fill path')
        sp = fn.mkPen(self.opts['shadowPen'])
        cp = fn.mkPen(self.opts['pen'])
        if sp is not None:
            if sp.style() != QtCore.Qt.NoPen:
                p.setPen(sp)
                p.drawPath(path)
        p.setPen(cp)
        p.drawPath(path)
        profiler('drawPath')

    def paintGL(self, p, opt, widget):
        p.beginNativePainting()
        import OpenGL.GL as gl
        view = self.getViewBox()
        if view is not None:
            rect = view.mapRectToItem(self, view.boundingRect())
            gl.glEnable(gl.GL_STENCIL_TEST)
            gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
            gl.glDepthMask(gl.GL_FALSE)
            gl.glStencilFunc(gl.GL_NEVER, 1, 255)
            gl.glStencilOp(gl.GL_REPLACE, gl.GL_KEEP, gl.GL_KEEP)
            gl.glStencilMask(255)
            gl.glClear(gl.GL_STENCIL_BUFFER_BIT)
            gl.glBegin(gl.GL_TRIANGLES)
            gl.glVertex2f(rect.x(), rect.y())
            gl.glVertex2f(rect.x() + rect.width(), rect.y())
            gl.glVertex2f(rect.x(), rect.y() + rect.height())
            gl.glVertex2f(rect.x() + rect.width(), rect.y() + rect.height())
            gl.glVertex2f(rect.x() + rect.width(), rect.y())
            gl.glVertex2f(rect.x(), rect.y() + rect.height())
            gl.glEnd()
            gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
            gl.glDepthMask(gl.GL_TRUE)
            gl.glStencilMask(0)
            gl.glStencilFunc(gl.GL_EQUAL, 1, 255)
        try:
            x, y = self.getData()
            pos = np.empty((len(x), 2))
            pos[:, 0] = x
            pos[:, 1] = y
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            try:
                gl.glVertexPointerf(pos)
                pen = fn.mkPen(self.opts['pen'])
                color = pen.color()
                gl.glColor4f(color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0, color.alpha() / 255.0)
                width = pen.width()
                if pen.isCosmetic():
                    if width < 1:
                        width = 1
                gl.glPointSize(width)
                gl.glEnable(gl.GL_LINE_SMOOTH)
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, pos.size / pos.shape[(-1)])
            finally:
                gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        finally:
            p.endNativePainting()

    def clear(self):
        self.xData = None
        self.yData = None
        self.xDisp = None
        self.yDisp = None
        self.path = None
        self.fillPath = None
        self._mouseShape = None
        self._mouseBounds = None
        self._boundsCache = [None, None]

    def mouseShape(self):
        """
        Return a QPainterPath representing the clickable shape of the curve
        
        """
        if self._mouseShape is None:
            view = self.getViewBox()
            if view is None:
                return QtGui.QPainterPath()
            stroker = QtGui.QPainterPathStroker()
            path = self.getPath()
            path = self.mapToItem(view, path)
            stroker.setWidth(self.opts['mouseWidth'])
            mousePath = stroker.createStroke(path)
            self._mouseShape = self.mapFromItem(view, mousePath)
        return self._mouseShape

    def mouseClickEvent(self, ev):
        if not self.clickable or ev.button() != QtCore.Qt.LeftButton:
            return
        if self.mouseShape().contains(ev.pos()):
            ev.accept()
            self.sigClicked.emit(self)


class ROIPlotItem(PlotCurveItem):
    __doc__ = 'Plot curve that monitors an ROI and image for changes to automatically replot.'

    def __init__(self, roi, data, img, axes=(0, 1), xVals=None, color=None):
        self.roi = roi
        self.roiData = data
        self.roiImg = img
        self.axes = axes
        self.xVals = xVals
        PlotCurveItem.__init__(self, (self.getRoiData()), x=(self.xVals), color=color)
        roi.sigRegionChanged.connect(self.roiChangedEvent)

    def getRoiData(self):
        d = self.roi.getArrayRegion((self.roiData), (self.roiImg), axes=(self.axes))
        if d is None:
            return
        while d.ndim > 1:
            d = d.mean(axis=1)

        return d

    def roiChangedEvent(self):
        d = self.getRoiData()
        self.updateData(d, self.xVals)