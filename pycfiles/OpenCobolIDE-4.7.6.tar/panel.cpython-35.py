# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/api/panel.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 3799 bytes
"""
This module contains the panel API.
"""
import logging
from pyqode.core.api.mode import Mode
from pyqode.qt import QtWidgets, QtGui

def _logger():
    """ Returns module's logger """
    return logging.getLogger(__name__)


class Panel(QtWidgets.QWidget, Mode):
    __doc__ = '\n    Base class for editor panels.\n\n    A panel is a mode and a QWidget.\n\n    .. note:: Use enabled to disable panel actions and setVisible to change the\n        visibility of the panel.\n    '

    class Position(object):
        __doc__ = '\n        Enumerates the possible panel positions\n        '
        TOP = 0
        LEFT = 1
        RIGHT = 2
        BOTTOM = 3

        @classmethod
        def iterable(cls):
            """ Returns possible positions as an iterable (list) """
            return [
             cls.TOP, cls.LEFT, cls.RIGHT, cls.BOTTOM]

    @property
    def scrollable(self):
        """
        A scrollable panel will follow the editor's scroll-bars. Left and right
        panels follow the vertical scrollbar. Top and bottom panels follow the
        horizontal scrollbar.

        :type: bool
        """
        return self._scrollable

    @scrollable.setter
    def scrollable(self, value):
        self._scrollable = value

    def __init__(self, dynamic=False):
        Mode.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.dynamic = dynamic
        self.order_in_zone = -1
        self._scrollable = False
        self._background_brush = None
        self._foreground_pen = None
        self.position = -1

    def on_install(self, editor):
        """
        Extends :meth:`pyqode.core.api.Mode.on_install` method to set the
        editor instance as the parent widget.

        .. warning:: Don't forget to call **super** if you override this
            method!

        :param editor: editor instance
        :type editor: pyqode.core.api.CodeEdit
        """
        Mode.on_install(self, editor)
        self.setParent(editor)
        self.setPalette(QtWidgets.QApplication.instance().palette())
        self.setFont(QtWidgets.QApplication.instance().font())
        self.editor.panels.refresh()
        self._background_brush = QtGui.QBrush(QtGui.QColor(self.palette().window().color()))
        self._foreground_pen = QtGui.QPen(QtGui.QColor(self.palette().windowText().color()))

    def paintEvent(self, event):
        if self.isVisible():
            self._background_brush = QtGui.QBrush(QtGui.QColor(self.palette().window().color()))
            self._foreground_pen = QtGui.QPen(QtGui.QColor(self.palette().windowText().color()))
            painter = QtGui.QPainter(self)
            painter.fillRect(event.rect(), self._background_brush)

    def setVisible(self, visible):
        """
        Shows/Hides the panel

        Automatically call CodeEdit.refresh_panels.

        :param visible: Visible state
        """
        _logger().log(5, '%s visibility changed', self.name)
        super(Panel, self).setVisible(visible)
        if self.editor:
            self.editor.panels.refresh()