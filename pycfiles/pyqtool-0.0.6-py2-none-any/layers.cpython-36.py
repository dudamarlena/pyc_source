# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/control/layers.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 699 bytes
from .control import Control

class Layers(Control):

    def __init__(self, layers=[], overlays={}, options=None):
        super().__init__()
        self.layers = layers
        self.overlays = overlays
        self.options = options
        self._initJs()

    def _initJs(self):
        jsObject = 'L.control.layers({layers}'.format(layers=(self._stringifyForJs(self.layers)))
        if self.overlays is not None:
            jsObject += ', {overlays}'.format(overlays=(self._stringifyForJs(self.overlays)))
        if self.options is not None:
            jsObject += ', {options}'.format(options=(self._stringifyForJs(self.options)))
        jsObject += ')'
        self._createJsObject(jsObject)