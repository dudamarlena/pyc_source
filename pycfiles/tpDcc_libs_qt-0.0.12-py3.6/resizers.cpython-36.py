# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/core/resizers.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 6476 bytes
"""
Module that contains implementation for dialog/window resizers
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
from tpDcc.libs.qt.core import qtutils

class ResizeDirection:
    Left = 1
    Top = 2
    Right = 4
    Bottom = 8


class WindowResizer(QFrame, object):
    windowResized = Signal()
    windowResizedStarted = Signal()
    windowResizedFinished = Signal()

    def __init__(self, parent):
        super(WindowResizer, self).__init__(parent)
        self._init()
        self._direction = 0
        self._widget_mouse_pos = None
        self._widget_geometry = None
        self._frameless = None
        self.setStyleSheet('background: transparent;')
        self.windowResizedStarted.connect(self._on_window_resize_started)

    def paintEvent(self, event):
        """
        Overrides base QFrame paintEvent function
        Override to make mouse events work in transparent widgets
        :param event: QPaintEvent
        """
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 0, 0, 1))
        painter.end()

    def leaveEvent(self, event):
        """
        Overrides base QFrame leaveEvent function
        :param event: QEvent
        """
        QApplication.restoreOverrideCursor()

    def mousePressEvent(self, event):
        """
        Overrides base QFrame mousePressEvent function
        :param event: QEvent
        """
        self.windowResizedStarted.emit()

    def mouseMoveEvent(self, event):
        """
        Overrides base QFrame mouseMoveEvent function
        :param event: QEvent
        """
        self.windowResized.emit()

    def mouseReleaseEvent(self, event):
        """
        Overrides base QFrame mouseReleaseEvent function
        :param event: QEvent
        """
        self.windowResizedFinished.emit()

    def setParent(self, parent):
        self._frameless = parent
        super(WindowResizer, self).setParent(parent)

    def set_resize_direction(self, direction):
        """
        Sets the resize direction

        .. code-block:: python

            setResizeDirection(ResizeDirection.Left | ResizeDireciton.Top)

        :param direction: ResizeDirection
        :return: ResizeDirection
        :rtype: int
        """
        self._direction = direction

    def _init(self):
        """
        Internal function that initializes reisizer
        Override in custom resizers
        """
        self.windowResized.connect(self._on_window_resized)

    def _on_window_resized(self):
        """
        Internal function that resizes the frame based on the mouse position and the current direction
        """
        pos = QCursor.pos()
        new_geo = self.window().frameGeometry()
        min_width = self.window().minimumSize().width()
        min_height = self.window().minimumSize().height()
        if self._direction & ResizeDirection.Left == ResizeDirection.Left:
            left = new_geo.left()
            new_geo.setLeft(pos.x() - self._widget_mouse_pos.x())
            if new_geo.width() <= min_width:
                new_geo.setLeft(left)
        if self._direction & ResizeDirection.Top == ResizeDirection.Top:
            top = new_geo.top()
            new_geo.setTop(pos.y() - self._widget_mouse_pos.y())
            if new_geo.height() <= min_height:
                new_geo.setTop(top)
        if self._direction & ResizeDirection.Right == ResizeDirection.Right:
            new_geo.setRight(pos.x() + (self.minimumSize().width() - self._widget_mouse_pos.x()))
        if self._direction & ResizeDirection.Bottom == ResizeDirection.Bottom:
            new_geo.setBottom(pos.y() + (self.minimumSize().height() - self._widget_mouse_pos.y()))
        x = new_geo.x()
        y = new_geo.y()
        w = max(new_geo.width(), min_width)
        h = max(new_geo.height(), min_height)
        self.window().setGeometry(x, y, w, h)

    def _on_window_resize_started(self):
        self._widget_mouse_pos = self.mapFromGlobal(QCursor.pos())
        self._widget_geometry = self.window().frameGeometry()


class CornerResizer(WindowResizer, object):
    __doc__ = '\n    Resizer for window corners\n    '

    def __init__(self, parent=None):
        super(CornerResizer, self).__init__(parent)

    def enterEvent(self, event):
        """
        Overrides base QFrame enterEvenet function
        :param event: QEvent
        """
        if self._direction == ResizeDirection.Left | ResizeDirection.Top or self._direction == ResizeDirection.Right | ResizeDirection.Bottom:
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
        elif self._direction == ResizeDirection.Right | ResizeDirection.Top or self._direction == ResizeDirection.Left | ResizeDirection.Bottom:
            QApplication.setOverrideCursor(Qt.SizeBDiagCursor)

    def _init(self):
        super(CornerResizer, self)._init()
        self.setFixedSize(qtutils.size_by_dpi(QSize(10, 10)))


class VerticalResizer(WindowResizer, object):
    __doc__ = '\n    Resize for top and bottom sides of the window\n    '

    def __init__(self, parent=None):
        super(VerticalResizer, self).__init__(parent)

    def enterEvent(self, event):
        """
        Overrides base QFrame enterEvenet function
        :param event: QEvent
        """
        QApplication.setOverrideCursor(Qt.SizeVerCursor)

    def _init(self):
        super(VerticalResizer, self)._init()
        self.setFixedHeight(qtutils.dpi_scale(8))


class HorizontalResizer(WindowResizer, object):
    __doc__ = '\n    Resize for left and right sides of the window\n    '

    def __init__(self, parent=None):
        super(HorizontalResizer, self).__init__(parent)

    def enterEvent(self, event):
        """
        Overrides base QFrame enterEvenet function
        :param event: QEvent
        """
        QApplication.setOverrideCursor(Qt.SizeHorCursor)

    def _init(self):
        super(HorizontalResizer, self)._init()
        self.setFixedWidth(qtutils.dpi_scale(8))