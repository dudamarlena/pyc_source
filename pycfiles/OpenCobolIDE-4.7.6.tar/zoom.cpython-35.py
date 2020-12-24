# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/modes/zoom.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 3317 bytes
"""
This module contains the ZoomMode which lets you zoom in and out the editor.
"""
from pyqode.core.api.mode import Mode
from pyqode.qt import QtCore, QtGui, QtWidgets

class ZoomMode(Mode):
    __doc__ = ' Zooms/Unzooms the editor (Ctrl+mouse wheel or Ctrl + 0 to reset).\n\n    This mode make it possible to zoom in/out the editor view.\n\n    Here are the controls:\n      * **zoom out**: *ctrl+-* or *ctrl+mouse wheel backward*\n      * **zoom in**: *ctrl++* or *ctrl+mouse wheel forward*\n      * **reset**: *ctrl + 0*\n    '

    def __init__(self):
        super(ZoomMode, self).__init__()
        self.prev_delta = 0
        self.default_font_size = 10

    def on_state_changed(self, state):
        if state:
            self.editor.mouse_wheel_activated.connect(self._on_wheel_event)
            self.editor.key_pressed.connect(self._on_key_pressed)
            self.mnu_zoom = QtWidgets.QMenu('Zoom')
            a = self.mnu_zoom.addAction(QtGui.QIcon.fromTheme('zoom-in'), 'Zoom in')
            a.setShortcut('Ctrl++')
            a.triggered.connect(self.editor.zoom_in)
            a = self.mnu_zoom.addAction(QtGui.QIcon.fromTheme('zoom-out'), 'Zoom out')
            a.setShortcut('Ctrl+-')
            a.triggered.connect(self.editor.zoom_out)
            a = self.mnu_zoom.addAction(QtGui.QIcon.fromTheme('zoom-fit-best'), 'Reset zoom')
            a.setShortcut('Ctrl+0')
            a.triggered.connect(self.editor.reset_zoom)
            a = self.mnu_zoom.menuAction()
            a.setIcon(QtGui.QIcon.fromTheme('zoom'))
            self.editor.add_action(a, sub_menu=None)
        else:
            self.editor.mouse_wheel_activated.disconnect(self._on_wheel_event)
            self.editor.remove_action(self.mnu_zoom.menuAction(), sub_menu=None)
            self.editor.key_pressed.disconnect(self._on_key_pressed)

    def _on_key_pressed(self, event):
        """
        Resets editor font size to the default font size

        :param event: wheelEvent
        :type event: QKeyEvent
        """
        if int(event.modifiers()) & QtCore.Qt.ControlModifier > 0 and not int(event.modifiers()) & QtCore.Qt.ShiftModifier:
            if event.key() == QtCore.Qt.Key_0:
                self.editor.reset_zoom()
                event.accept()
            if event.key() == QtCore.Qt.Key_Plus:
                self.editor.zoom_in()
                event.accept()
            if event.key() == QtCore.Qt.Key_Minus:
                self.editor.zoom_out()
                event.accept()

    def _on_wheel_event(self, event):
        """
        Increments or decrements editor fonts settings on mouse wheel event
        if ctrl modifier is on.

        :param event: wheel event
        :type event: QWheelEvent
        """
        try:
            delta = event.angleDelta().y()
        except AttributeError:
            delta = event.delta()

        if int(event.modifiers()) & QtCore.Qt.ControlModifier > 0:
            if delta < self.prev_delta:
                self.editor.zoom_out()
                event.accept()
        else:
            self.editor.zoom_in()
            event.accept()