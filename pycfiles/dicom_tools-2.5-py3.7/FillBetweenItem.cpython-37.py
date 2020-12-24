# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/FillBetweenItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2896 bytes
from ..Qt import QtGui, USE_PYQT5, USE_PYQT4, USE_PYSIDE
from .. import functions as fn
from .PlotDataItem import PlotDataItem
from .PlotCurveItem import PlotCurveItem

class FillBetweenItem(QtGui.QGraphicsPathItem):
    __doc__ = '\n    GraphicsItem filling the space between two PlotDataItems.\n    '

    def __init__(self, curve1=None, curve2=None, brush=None, pen=None):
        QtGui.QGraphicsPathItem.__init__(self)
        self.curves = None
        if curve1 is not None and curve2 is not None:
            self.setCurves(curve1, curve2)
        else:
            if curve1 is not None or curve2 is not None:
                raise Exception('Must specify two curves to fill between.')
        if brush is not None:
            self.setBrush(brush)
        self.setPen(pen)
        self.updatePath()

    def setBrush(self, *args, **kwds):
        QtGui.QGraphicsPathItem.setBrush(self, (fn.mkBrush)(*args, **kwds))

    def setPen(self, *args, **kwds):
        QtGui.QGraphicsPathItem.setPen(self, (fn.mkPen)(*args, **kwds))

    def setCurves(self, curve1, curve2):
        """Set the curves to fill between.
        
        Arguments must be instances of PlotDataItem or PlotCurveItem.
        
        Added in version 0.9.9
        """
        if self.curves is not None:
            for c in self.curves:
                try:
                    c.sigPlotChanged.disconnect(self.curveChanged)
                except (TypeError, RuntimeError):
                    pass

        curves = [
         curve1, curve2]
        for c in curves:
            if not isinstance(c, PlotDataItem) or isinstance(c, PlotCurveItem):
                raise TypeError('Curves must be PlotDataItem or PlotCurveItem.')

        self.curves = curves
        curve1.sigPlotChanged.connect(self.curveChanged)
        curve2.sigPlotChanged.connect(self.curveChanged)
        self.setZValue(min(curve1.zValue(), curve2.zValue()) - 1)
        self.curveChanged()

    def setBrush(self, *args, **kwds):
        """Change the fill brush. Acceps the same arguments as pg.mkBrush()"""
        QtGui.QGraphicsPathItem.setBrush(self, (fn.mkBrush)(*args, **kwds))

    def curveChanged(self):
        self.updatePath()

    def updatePath(self):
        if self.curves is None:
            self.setPath(QtGui.QPainterPath())
            return
        paths = []
        for c in self.curves:
            if isinstance(c, PlotDataItem):
                paths.append(c.curve.getPath())

        path = QtGui.QPainterPath()
        transform = QtGui.QTransform()
        p1 = paths[0].toSubpathPolygons(transform)
        p2 = paths[1].toReversed().toSubpathPolygons(transform)
        if len(p1) == 0 or len(p2) == 0:
            self.setPath(QtGui.QPainterPath())
            return
        path.addPolygon(p1[0] + p2[0])
        self.setPath(path)