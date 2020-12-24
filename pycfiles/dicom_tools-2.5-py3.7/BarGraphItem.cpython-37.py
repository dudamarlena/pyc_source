# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/BarGraphItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4828 bytes
from ..Qt import QtGui, QtCore
from .GraphicsObject import GraphicsObject
from .. import getConfigOption
from .. import functions as fn
import numpy as np
__all__ = [
 'BarGraphItem']

class BarGraphItem(GraphicsObject):

    def __init__(self, **opts):
        """
        Valid keyword options are:
        x, x0, x1, y, y0, y1, width, height, pen, brush
        
        x specifies the x-position of the center of the bar.
        x0, x1 specify left and right edges of the bar, respectively.
        width specifies distance from x0 to x1.
        You may specify any combination:
            
            x, width
            x0, width
            x1, width
            x0, x1
            
        Likewise y, y0, y1, and height. 
        If only height is specified, then y0 will be set to 0
        
        Example uses:
        
            BarGraphItem(x=range(5), height=[1,5,2,4,3], width=0.5)
            
        
        """
        GraphicsObject.__init__(self)
        self.opts = dict(x=None,
          y=None,
          x0=None,
          y0=None,
          x1=None,
          y1=None,
          height=None,
          width=None,
          pen=None,
          brush=None,
          pens=None,
          brushes=None)
        self._shape = None
        self.picture = None
        (self.setOpts)(**opts)

    def setOpts(self, **opts):
        self.opts.update(opts)
        self.picture = None
        self._shape = None
        self.update()
        self.informViewBoundsChanged()

    def drawPicture(self):
        self.picture = QtGui.QPicture()
        self._shape = QtGui.QPainterPath()
        p = QtGui.QPainter(self.picture)
        pen = self.opts['pen']
        pens = self.opts['pens']
        if pen is None:
            if pens is None:
                pen = getConfigOption('foreground')
        brush = self.opts['brush']
        brushes = self.opts['brushes']
        if brush is None:
            if brushes is None:
                brush = (128, 128, 128)

        def asarray(x):
            if x is None or np.isscalar(x) or isinstance(x, np.ndarray):
                return x
            return np.array(x)

        x = asarray(self.opts.get('x'))
        x0 = asarray(self.opts.get('x0'))
        x1 = asarray(self.opts.get('x1'))
        width = asarray(self.opts.get('width'))
        if x0 is None:
            if width is None:
                raise Exception('must specify either x0 or width')
            elif x1 is not None:
                x0 = x1 - width
            else:
                if x is not None:
                    x0 = x - width / 2.0
                else:
                    raise Exception('must specify at least one of x, x0, or x1')
        else:
            if width is None:
                if x1 is None:
                    raise Exception('must specify either x1 or width')
                width = x1 - x0
            y = asarray(self.opts.get('y'))
            y0 = asarray(self.opts.get('y0'))
            y1 = asarray(self.opts.get('y1'))
            height = asarray(self.opts.get('height'))
            if y0 is None:
                if height is None:
                    y0 = 0
                else:
                    if y1 is not None:
                        y0 = y1 - height
                    else:
                        if y is not None:
                            y0 = y - height / 2.0
                        else:
                            y0 = 0
        if height is None:
            if y1 is None:
                raise Exception('must specify either y1 or height')
            height = y1 - y0
        p.setPen(fn.mkPen(pen))
        p.setBrush(fn.mkBrush(brush))
        for i in range(len(x0)):
            if pens is not None:
                p.setPen(fn.mkPen(pens[i]))
            else:
                if brushes is not None:
                    p.setBrush(fn.mkBrush(brushes[i]))
                else:
                    if np.isscalar(x0):
                        x = x0
                    else:
                        x = x0[i]
                    if np.isscalar(y0):
                        y = y0
                    else:
                        y = y0[i]
                    if np.isscalar(width):
                        w = width
                    else:
                        w = width[i]
                if np.isscalar(height):
                    h = height
                else:
                    h = height[i]
            rect = QtCore.QRectF(x, y, w, h)
            p.drawRect(rect)
            self._shape.addRect(rect)

        p.end()
        self.prepareGeometryChange()

    def paint(self, p, *args):
        if self.picture is None:
            self.drawPicture()
        self.picture.play(p)

    def boundingRect(self):
        if self.picture is None:
            self.drawPicture()
        return QtCore.QRectF(self.picture.boundingRect())

    def shape(self):
        if self.picture is None:
            self.drawPicture()
        return self._shape