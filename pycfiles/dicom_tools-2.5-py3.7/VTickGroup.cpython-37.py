# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/VTickGroup.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3508 bytes
if __name__ == '__main__':
    import os, sys
    path = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(path, '..', '..'))
from ..Qt import QtGui, QtCore
from .. import functions as fn
import weakref
from .UIGraphicsItem import UIGraphicsItem
__all__ = [
 'VTickGroup']

class VTickGroup(UIGraphicsItem):
    __doc__ = '\n    **Bases:** :class:`UIGraphicsItem <pyqtgraph.UIGraphicsItem>`\n    \n    Draws a set of tick marks which always occupy the same vertical range of the view,\n    but have x coordinates relative to the data within the view.\n    \n    '

    def __init__(self, xvals=None, yrange=None, pen=None):
        """
        ==============  ===================================================================
        **Arguments:**
        xvals           A list of x values (in data coordinates) at which to draw ticks.
        yrange          A list of [low, high] limits for the tick. 0 is the bottom of
                        the view, 1 is the top. [0.8, 1] would draw ticks in the top
                        fifth of the view.
        pen             The pen to use for drawing ticks. Default is grey. Can be specified
                        as any argument valid for :func:`mkPen<pyqtgraph.mkPen>`
        ==============  ===================================================================
        """
        if yrange is None:
            yrange = [
             0, 1]
        if xvals is None:
            xvals = []
        UIGraphicsItem.__init__(self)
        if pen is None:
            pen = (200, 200, 200)
        self.path = QtGui.QGraphicsPathItem()
        self.ticks = []
        self.xvals = []
        self.yrange = [
         0, 1]
        self.setPen(pen)
        self.setYRange(yrange)
        self.setXVals(xvals)

    def setPen(self, *args, **kwargs):
        """Set the pen to use for drawing ticks. Can be specified as any arguments valid
        for :func:`mkPen<pyqtgraph.mkPen>`"""
        self.pen = (fn.mkPen)(*args, **kwargs)

    def setXVals(self, vals):
        """Set the x values for the ticks. 
        
        ==============   =====================================================================
        **Arguments:**
        vals             A list of x values (in data/plot coordinates) at which to draw ticks.
        ==============   =====================================================================
        """
        self.xvals = vals
        self.rebuildTicks()

    def setYRange(self, vals):
        """Set the y range [low, high] that the ticks are drawn on. 0 is the bottom of 
        the view, 1 is the top."""
        self.yrange = vals
        self.rebuildTicks()

    def dataBounds(self, *args, **kargs):
        pass

    def yRange(self):
        return self.yrange

    def rebuildTicks(self):
        self.path = QtGui.QPainterPath()
        yrange = self.yRange()
        for x in self.xvals:
            self.path.moveTo(x, 0.0)
            self.path.lineTo(x, 1.0)

    def paint(self, p, *args):
        (UIGraphicsItem.paint)(self, p, *args)
        br = self.boundingRect()
        h = br.height()
        br.setY(br.y() + self.yrange[0] * h)
        br.setHeight(h - (1.0 - self.yrange[1]) * h)
        p.translate(0, br.y())
        p.scale(1.0, br.height())
        p.setPen(self.pen)
        p.drawPath(self.path)