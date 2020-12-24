# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/TextItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5747 bytes
from ..Qt import QtCore, QtGui
from ..Point import Point
from .UIGraphicsItem import *
from .. import functions as fn

class TextItem(UIGraphicsItem):
    __doc__ = '\n    GraphicsItem displaying unscaled text (the text will always appear normal even inside a scaled ViewBox). \n    '

    def __init__(self, text='', color=(200, 200, 200), html=None, anchor=(0, 0), border=None, fill=None, angle=0):
        """
        ==============  =================================================================================
        **Arguments:**
        *text*          The text to display
        *color*         The color of the text (any format accepted by pg.mkColor)
        *html*          If specified, this overrides both *text* and *color*
        *anchor*        A QPointF or (x,y) sequence indicating what region of the text box will
                        be anchored to the item's position. A value of (0,0) sets the upper-left corner
                        of the text box to be at the position specified by setPos(), while a value of (1,1)
                        sets the lower-right corner.
        *border*        A pen to use when drawing the border
        *fill*          A brush to use when filling within the border
        ==============  =================================================================================
        """
        self.anchor = Point(anchor)
        UIGraphicsItem.__init__(self)
        self.textItem = QtGui.QGraphicsTextItem()
        self.textItem.setParentItem(self)
        self.lastTransform = None
        self._bounds = QtCore.QRectF()
        if html is None:
            self.setText(text, color)
        else:
            self.setHtml(html)
        self.fill = fn.mkBrush(fill)
        self.border = fn.mkPen(border)
        self.rotate(angle)
        self.setFlag(self.ItemIgnoresTransformations)

    def setText(self, text, color=(200, 200, 200)):
        """
        Set the text and color of this item. 
        
        This method sets the plain text of the item; see also setHtml().
        """
        color = fn.mkColor(color)
        self.textItem.setDefaultTextColor(color)
        self.textItem.setPlainText(text)
        self.updateText()

    def updateAnchor(self):
        pass

    def setPlainText(self, *args):
        """
        Set the plain text to be rendered by this item. 
        
        See QtGui.QGraphicsTextItem.setPlainText().
        """
        (self.textItem.setPlainText)(*args)
        self.updateText()

    def setHtml(self, *args):
        """
        Set the HTML code to be rendered by this item. 
        
        See QtGui.QGraphicsTextItem.setHtml().
        """
        (self.textItem.setHtml)(*args)
        self.updateText()

    def setTextWidth(self, *args):
        """
        Set the width of the text.
        
        If the text requires more space than the width limit, then it will be
        wrapped into multiple lines.
        
        See QtGui.QGraphicsTextItem.setTextWidth().
        """
        (self.textItem.setTextWidth)(*args)
        self.updateText()

    def setFont(self, *args):
        """
        Set the font for this text. 
        
        See QtGui.QGraphicsTextItem.setFont().
        """
        (self.textItem.setFont)(*args)
        self.updateText()

    def updateText(self):
        self.textItem.resetTransform()
        if self._exportOpts is not False:
            if 'resolutionScale' in self._exportOpts:
                s = self._exportOpts['resolutionScale']
                self.textItem.scale(s, s)
        self.textItem.setPos(0, 0)
        br = self.textItem.boundingRect()
        apos = self.textItem.mapToParent(Point(br.width() * self.anchor.x(), br.height() * self.anchor.y()))
        self.textItem.setPos(-apos.x(), -apos.y())

    def viewRangeChanged(self):
        self.updateText()

    def boundingRect(self):
        return self.textItem.mapToParent(self.textItem.boundingRect()).boundingRect()

    def paint(self, p, *args):
        tr = p.transform()
        if self.lastTransform is not None:
            if tr != self.lastTransform:
                self.viewRangeChanged()
        self.lastTransform = tr
        if self.border.style() != QtCore.Qt.NoPen or self.fill.style() != QtCore.Qt.NoBrush:
            p.setPen(self.border)
            p.setBrush(self.fill)
            p.setRenderHint(p.Antialiasing, True)
            p.drawPolygon(self.textItem.mapToParent(self.textItem.boundingRect()))