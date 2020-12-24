# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/IsocurveItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3857 bytes
from .GraphicsObject import *
from .. import functions as fn
from ..Qt import QtGui, QtCore

class IsocurveItem(GraphicsObject):
    __doc__ = '\n    **Bases:** :class:`GraphicsObject <pyqtgraph.GraphicsObject>`\n    \n    Item displaying an isocurve of a 2D array.To align this item correctly with an \n    ImageItem,call isocurve.setParentItem(image)\n    '

    def __init__(self, data=None, level=0, pen='w'):
        """
        Create a new isocurve item. 
        
        ==============  ===============================================================
        **Arguments:**
        data            A 2-dimensional ndarray. Can be initialized as None, and set
                        later using :func:`setData <pyqtgraph.IsocurveItem.setData>`
        level           The cutoff value at which to draw the isocurve.
        pen             The color of the curve item. Can be anything valid for
                        :func:`mkPen <pyqtgraph.mkPen>`
        ==============  ===============================================================
        """
        GraphicsObject.__init__(self)
        self.level = level
        self.data = None
        self.path = None
        self.setPen(pen)
        self.setData(data, level)

    def setData(self, data, level=None):
        """
        Set the data/image to draw isocurves for.
        
        ==============  ========================================================================
        **Arguments:**
        data            A 2-dimensional ndarray.
        level           The cutoff value at which to draw the curve. If level is not specified,
                        the previously set level is used.
        ==============  ========================================================================
        """
        if level is None:
            level = self.level
        self.level = level
        self.data = data
        self.path = None
        self.prepareGeometryChange()
        self.update()

    def setLevel(self, level):
        """Set the level at which the isocurve is drawn."""
        self.level = level
        self.path = None
        self.prepareGeometryChange()
        self.update()

    def setPen(self, *args, **kwargs):
        """Set the pen used to draw the isocurve. Arguments can be any that are valid 
        for :func:`mkPen <pyqtgraph.mkPen>`"""
        self.pen = (fn.mkPen)(*args, **kwargs)
        self.update()

    def setBrush(self, *args, **kwargs):
        """Set the brush used to draw the isocurve. Arguments can be any that are valid 
        for :func:`mkBrush <pyqtgraph.mkBrush>`"""
        self.brush = (fn.mkBrush)(*args, **kwargs)
        self.update()

    def updateLines(self, data, level):
        self.setData(data, level)

    def boundingRect(self):
        if self.data is None:
            return QtCore.QRectF()
        if self.path is None:
            self.generatePath()
        return self.path.boundingRect()

    def generatePath(self):
        if self.data is None:
            self.path = None
            return
        lines = fn.isocurve((self.data), (self.level), connected=True, extendToEdge=True)
        self.path = QtGui.QPainterPath()
        for line in lines:
            (self.path.moveTo)(*line[0])
            for p in line[1:]:
                (self.path.lineTo)(*p)

    def paint(self, p, *args):
        if self.data is None:
            return
        if self.path is None:
            self.generatePath()
        p.setPen(self.pen)
        p.drawPath(self.path)