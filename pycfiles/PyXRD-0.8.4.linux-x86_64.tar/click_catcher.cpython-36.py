# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/plot/click_catcher.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1423 bytes
from .event_delegator import MPLCanvasEventDelegator

class ClickCatcher:
    __doc__ = '\n        This class can be used to register matplotlib artists, which will\n        fire the update_callback method when clicked. When registering\n        the artist, an arbitrary object can be passed which is passed to the\n        callback. \n    '

    def __init__(self, plot_controller, update_callback=None):
        self.plot_controller = plot_controller
        self._canvas = plot_controller.canvas
        self._window = self._canvas.get_window()
        self._update_callback = update_callback
        self.connect()
        self._artists = {}

    def register_artist(self, artist, obj):
        self._artists[artist] = obj
        artist.set_picker(True)

    def _on_pick(self, event):
        if event.artist is not None:
            obj = self._artists.get(event.artist, None)
            self._update_callback(obj)
        return False

    def connect(self):
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.connect('pick_event', (self._on_pick), first=True)

    def disconnect(self):
        delegator = MPLCanvasEventDelegator.wrap_canvas(self._canvas)
        delegator.disconnect('pick_event', self._on_pick)