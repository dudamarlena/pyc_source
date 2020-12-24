# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/LabelItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5146 bytes
from ..Qt import QtGui, QtCore
from .. import functions as fn
from .GraphicsWidget import GraphicsWidget
from .GraphicsWidgetAnchor import GraphicsWidgetAnchor
from .. import getConfigOption
__all__ = [
 'LabelItem']

class LabelItem(GraphicsWidget, GraphicsWidgetAnchor):
    """LabelItem"""

    def __init__(self, text=' ', parent=None, angle=0, **args):
        GraphicsWidget.__init__(self, parent)
        GraphicsWidgetAnchor.__init__(self)
        self.item = QtGui.QGraphicsTextItem(self)
        self.opts = {'color':None, 
         'justify':'center'}
        self.opts.update(args)
        self._sizeHint = {}
        self.setText(text)
        self.setAngle(angle)

    def setAttr(self, attr, value):
        """Set default text properties. See setText() for accepted parameters."""
        self.opts[attr] = value

    def setText(self, text, **args):
        """Set the text and text properties in the label. Accepts optional arguments for auto-generating
        a CSS style string:

        ==================== ==============================
        **Style Arguments:**
        color                (str) example: 'CCFF00'
        size                 (str) example: '8pt'
        bold                 (bool)
        italic               (bool)
        ==================== ==============================
        """
        self.text = text
        opts = self.opts
        for k in args:
            opts[k] = args[k]

        optlist = []
        color = self.opts['color']
        if color is None:
            color = getConfigOption('foreground')
        color = fn.mkColor(color)
        optlist.append('color: #' + fn.colorStr(color)[:6])
        if 'size' in opts:
            optlist.append('font-size: ' + opts['size'])
        if 'bold' in opts:
            if opts['bold'] in (True, False):
                optlist.append('font-weight: ' + {True:'bold',  False:'normal'}[opts['bold']])
        if 'italic' in opts:
            if opts['italic'] in (True, False):
                optlist.append('font-style: ' + {True:'italic',  False:'normal'}[opts['italic']])
        full = "<span style='%s'>%s</span>" % ('; '.join(optlist), text)
        self.item.setHtml(full)
        self.updateMin()
        self.resizeEvent(None)
        self.updateGeometry()

    def resizeEvent(self, ev):
        self.item.setPos(0, 0)
        bounds = self.itemRect()
        left = self.mapFromItem(self.item, QtCore.QPointF(0, 0)) - self.mapFromItem(self.item, QtCore.QPointF(1, 0))
        rect = self.rect()
        if self.opts['justify'] == 'left':
            if left.x() != 0:
                bounds.moveLeft(rect.left())
            elif left.y() < 0:
                bounds.moveTop(rect.top())
            elif left.y() > 0:
                bounds.moveBottom(rect.bottom())
        elif self.opts['justify'] == 'center':
            bounds.moveCenter(rect.center())
        elif self.opts['justify'] == 'right':
            if left.x() != 0:
                bounds.moveRight(rect.right())
            if left.y() < 0:
                bounds.moveBottom(rect.bottom())
            elif left.y() > 0:
                bounds.moveTop(rect.top())
        self.item.setPos(bounds.topLeft() - self.itemRect().topLeft())
        self.updateMin()

    def setAngle(self, angle):
        self.angle = angle
        self.item.resetTransform()
        self.item.rotate(angle)
        self.updateMin()

    def updateMin(self):
        bounds = self.itemRect()
        self.setMinimumWidth(bounds.width())
        self.setMinimumHeight(bounds.height())
        self._sizeHint = {QtCore.Qt.MinimumSize: (bounds.width(), bounds.height()), 
         QtCore.Qt.PreferredSize: (bounds.width(), bounds.height()), 
         QtCore.Qt.MaximumSize: (-1, -1), 
         QtCore.Qt.MinimumDescent: (0, 0)}
        self.updateGeometry()

    def sizeHint(self, hint, constraint):
        if hint not in self._sizeHint:
            return QtCore.QSizeF(0, 0)
        return (QtCore.QSizeF)(*self._sizeHint[hint])

    def itemRect(self):
        return self.item.mapRectToParent(self.item.boundingRect())