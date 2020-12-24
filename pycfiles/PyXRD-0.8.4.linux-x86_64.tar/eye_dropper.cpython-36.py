# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/plot/eye_dropper.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1776 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from .event_delegator import MPLCanvasEventDelegator

class EyeDropper:
    __doc__ = '\n        A wrapper that makes eye-dropping a plot possible. Will call\n        the click_callback with an x position and the click event object as\n        arguments.\n    '

    def __init__(self, plot_controller, click_callback=None):
        self._canvas = plot_controller.canvas
        self._window = self._canvas.get_window()
        self._click_callback = click_callback
        self.connect()

    def _on_motion(self, event):
        if self._window is not None:
            self._window.set_cursor(Gdk.Cursor.new(Gdk.CursorType.CROSSHAIR))
        return False

    def _on_click(self, event):
        x_pos = -1
        if event.inaxes:
            x_pos = event.xdata
        if callable(self._click_callback):
            self._click_callback(x_pos, event)
        if self._window is not None:
            self._window.set_cursor(None)
        return True

    def connect(self):
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.connect('motion_notify_event', (self._on_motion), first=True)
        delegator.connect('button_press_event', (self._on_click), first=True)

    def disconnect(self):
        if self._window is not None:
            self._window.set_cursor(None)
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.disconnect('motion_notify_event', self._on_motion)
        delegator.disconnect('button_press_event', self._on_click)