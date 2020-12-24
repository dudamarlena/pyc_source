# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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