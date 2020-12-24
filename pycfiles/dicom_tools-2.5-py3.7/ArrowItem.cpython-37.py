# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/ArrowItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4655 bytes
from ..Qt import QtGui, QtCore
from .. import functions as fn
import numpy as np
__all__ = [
 'ArrowItem']

class ArrowItem(QtGui.QGraphicsPathItem):
    __doc__ = '\n    For displaying scale-invariant arrows.\n    For arrows pointing to a location on a curve, see CurveArrow\n    \n    '

    def __init__(self, **opts):
        """
        Arrows can be initialized with any keyword arguments accepted by 
        the setStyle() method.
        """
        self.opts = {}
        QtGui.QGraphicsPathItem.__init__(self, opts.get('parent', None))
        if 'size' in opts:
            opts['headLen'] = opts['size']
        if 'width' in opts:
            opts['headWidth'] = opts['width']
        defaultOpts = {'pxMode':True,  'angle':-150, 
         'pos':(0, 0), 
         'headLen':20, 
         'tipAngle':25, 
         'baseAngle':0, 
         'tailLen':None, 
         'tailWidth':3, 
         'pen':(200, 200, 200), 
         'brush':(50, 50, 200)}
        defaultOpts.update(opts)
        (self.setStyle)(**defaultOpts)
        self.rotate(self.opts['angle'])
        (self.moveBy)(*self.opts['pos'])

    def setStyle(self, **opts):
        """
        Changes the appearance of the arrow.
        All arguments are optional:
        
        ======================  =================================================
        **Keyword Arguments:**
        angle                   Orientation of the arrow in degrees. Default is
                                0; arrow pointing to the left.
        headLen                 Length of the arrow head, from tip to base.
                                default=20
        headWidth               Width of the arrow head at its base.
        tipAngle                Angle of the tip of the arrow in degrees. Smaller
                                values make a 'sharper' arrow. If tipAngle is
                                specified, ot overrides headWidth. default=25
        baseAngle               Angle of the base of the arrow head. Default is
                                0, which means that the base of the arrow head
                                is perpendicular to the arrow tail.
        tailLen                 Length of the arrow tail, measured from the base
                                of the arrow head to the end of the tail. If
                                this value is None, no tail will be drawn.
                                default=None
        tailWidth               Width of the tail. default=3
        pen                     The pen used to draw the outline of the arrow.
        brush                   The brush used to fill the arrow.
        ======================  =================================================
        """
        self.opts.update(opts)
        opt = dict([(k, self.opts[k]) for k in ('headLen', 'tipAngle', 'baseAngle',
                                                'tailLen', 'tailWidth')])
        self.path = (fn.makeArrowPath)(**opt)
        self.setPath(self.path)
        self.setPen(fn.mkPen(self.opts['pen']))
        self.setBrush(fn.mkBrush(self.opts['brush']))
        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)

    def paint(self, p, *args):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        (QtGui.QGraphicsPathItem.paint)(self, p, *args)

    def shape(self):
        return self.path

    def dataBounds(self, ax, frac, orthoRange=None):
        pw = 0
        pen = self.pen()
        if not pen.isCosmetic():
            pw = pen.width() * 0.7072
        if self.opts['pxMode']:
            return [
             0, 0]
        br = self.boundingRect()
        if ax == 0:
            return [
             br.left() - pw, br.right() + pw]
        return [br.top() - pw, br.bottom() + pw]

    def pixelPadding(self):
        pad = 0
        if self.opts['pxMode']:
            br = self.boundingRect()
            pad += (br.width() ** 2 + br.height() ** 2) ** 0.5
        pen = self.pen()
        if pen.isCosmetic():
            pad += max(1, pen.width()) * 0.7072
        return pad