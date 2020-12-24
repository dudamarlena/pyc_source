# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/vector/polyline.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 485 bytes
from .path import Path

class Polyline(Path):

    def __init__(self, latLngs, options=None):
        super().__init__()
        self.latLngs = latLngs
        self.options = options
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'L.polyline({latLngs}'.format(latLngs=(self.latLngs))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)