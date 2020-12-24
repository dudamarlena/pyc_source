# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/plot/motion_tracker.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1217 bytes
from .event_delegator import MPLCanvasEventDelegator

class MotionTracker:
    __doc__ = '\n        A wrapper that tracks mouse movements on a plot. Will call\n        the update_callback with an x position and the click event object as\n        arguments.\n    '

    def __init__(self, plot_controller, update_callback=None):
        self._canvas = plot_controller.canvas
        self._window = self._canvas.get_window()
        self._update_callback = update_callback
        self.connect()

    def _on_motion(self, event):
        x_pos = -1
        if event.inaxes:
            x_pos = event.xdata
        if callable(self._update_callback):
            self._update_callback(x_pos, event)
        return False

    def connect(self):
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.connect('motion_notify_event', (self._on_motion), first=True)

    def disconnect(self):
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.disconnect('motion_notify_event', self._on_motion)