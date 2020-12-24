# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/qpixmapwidget.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a pure Qt widget that displays an image"""
from __future__ import absolute_import
from taurus.external.qt import Qt
__all__ = [
 'QPixmapWidget']
__docformat__ = 'restructuredtext'

class QPixmapWidget(Qt.QWidget):
    """This widget displays an image (pixmap). By default the pixmap is
    scaled to the widget size and the aspect ratio is kept.
    The default alignment of the pixmap inside the widget space is horizontal
    left, vertical center."""
    DefaultAlignment = Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter
    DefaultAspectRatioMode = Qt.Qt.KeepAspectRatio
    DefaultTransformationMode = Qt.Qt.SmoothTransformation

    def __init__(self, parent=None, designMode=False):
        self._pixmap = Qt.QPixmap()
        self._pixmapDrawn = None
        self._alignment = self.DefaultAlignment
        self._pixmapAspectRatioMode = self.DefaultAspectRatioMode
        self._pixmapTransformationMode = self.DefaultTransformationMode
        Qt.QWidget.__init__(self, parent)
        return

    def _getPixmap(self):
        if self._pixmapDrawn is None:
            self._pixmapDrawn = self.recalculatePixmap()
        return self._pixmapDrawn

    def recalculatePixmap(self):
        origPixmap = self._pixmap
        if origPixmap.isNull():
            return origPixmap
        return origPixmap.scaled(self.size(), self._pixmapAspectRatioMode, self._pixmapTransformationMode)

    def _setDirty(self):
        self._pixmapDrawn = None
        return

    def paintEvent(self, paintEvent):
        """Overwrite the paintEvent from QWidget to draw the pixmap"""
        pixmap = self._getPixmap()
        w, h = self.width(), self.height()
        painter = Qt.QPainter(self)
        painter.setRenderHint(Qt.QPainter.Antialiasing)
        pw, ph = pixmap.width(), pixmap.height()
        align = self._alignment
        hAlign = align & Qt.Qt.AlignHorizontal_Mask
        vAlign = align & Qt.Qt.AlignVertical_Mask
        x, y = (0, 0)
        if hAlign & Qt.Qt.AlignHCenter:
            x = (w - pw) // 2
        elif hAlign & Qt.Qt.AlignRight:
            x = w - pw
        if vAlign & Qt.Qt.AlignVCenter:
            y = (h - ph) // 2
        elif vAlign & Qt.Qt.AlignBottom:
            y = h - ph
        x, y = max(0, x), max(0, y)
        painter.drawPixmap(x, y, pixmap)

    def resizeEvent(self, event):
        self._setDirty()
        return Qt.QWidget.resizeEvent(self, event)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return {'module': 'taurus.qt.qtgui.display', 
           'group': 'Taurus Display', 
           'icon': 'designer:graphicsview.png', 
           'container': False}

    def getPixmap(self):
        """Returns the pixmap.Returns None if no pixmap is set.
        :return: the current pixmap
        :rtype: PyQt4.Qt.QPixmap"""
        return self._pixmap

    def setPixmap(self, pixmap):
        """Sets the pixmap for this widget. Setting it to None disables pixmap
        :param pixmap: the new pixmap
        :type  pixmap: PyQt4.Qt.QPixmap"""
        self._pixmap = Qt.QPixmap(pixmap)
        self._setDirty()
        self.update()

    def resetPixmap(self):
        """Resets the pixmap for this widget."""
        self.setPixmap(Qt.QPixmap())

    def getAspectRatioMode(self):
        """Returns the aspect ratio to apply when drawing the pixmap.
        :return: the current aspect ratio
        :rtype: PyQt4.Qt.AspectRatioMode"""
        return self._pixmapAspectRatioMode

    def setAspectRatioMode(self, aspect):
        """Sets the aspect ratio mode to apply when drawing the pixmap.
        :param pixmap: the new aspect ratio mode
        :type  pixmap: PyQt4.Qt.AspectRatioMode"""
        self._pixmapAspectRatioMode = aspect
        self._setDirty()
        self.update()

    def resetAspectRatioMode(self):
        """Resets the aspect ratio mode to KeepAspectRatio"""
        self.setAspectRatioMode(self.DefaultAspectRatioMode)

    def getTransformationMode(self):
        """Returns the transformation mode to apply when drawing the pixmap.
        :return: the current transformation mode
        :rtype: PyQt4.Qt.TransformationMode"""
        return self._pixmapTransformationMode

    def setTransformationMode(self, transformation):
        """Sets the transformation mode to apply when drawing the pixmap.
        :param pixmap: the new transformation mode
        :type  pixmap: PyQt4.Qt.TransformationMode"""
        self._pixmapTransformationMode = transformation
        self._setDirty()
        self.update()

    def resetTransformationMode(self):
        """Resets the transformation mode to SmoothTransformation"""
        self.setTransformationMode(self.DefaultTransformationMode)

    def getAlignment(self):
        """Returns the alignment to apply when drawing the pixmap.
        :return: the current alignment
        :rtype: PyQt4.Qt.Alignment"""
        return self._alignment

    def setAlignment(self, alignment):
        """Sets the alignment to apply when drawing the pixmap.
        :param pixmap: the new alignment
        :type  pixmap: PyQt4.Qt.Alignment"""
        self._alignment = Qt.Qt.Alignment(alignment)
        self.update()

    def resetAlignment(self):
        """Resets the transformation mode to Qt.Qt.AlignLeft | Qt.Qt.AlignVCenter"""
        self.setAlignment(self.DefaultAlignment)

    pixmap = Qt.pyqtProperty('QPixmap', getPixmap, setPixmap, resetPixmap, doc="the widget's pixmap")
    aspectRatioMode = Qt.pyqtProperty('Qt::AspectRatioMode', getAspectRatioMode, setAspectRatioMode, resetAspectRatioMode, doc="the widget's pixmap aspect ratio mode")
    transformationMode = Qt.pyqtProperty('Qt::TransformationMode', getTransformationMode, setTransformationMode, resetTransformationMode, doc="the widget's pixmap transformation mode")
    alignment = Qt.pyqtProperty('Qt::Alignment', getAlignment, setAlignment, resetAlignment, doc="the widget's pixmap alignment")


def demo():
    """QPixmap Widget"""
    from .demo import qpixmapwidgetdemo
    return qpixmapwidgetdemo.main()


def main():
    return demo()


if __name__ == '__main__':
    main()