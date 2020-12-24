# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/vector/circlemarker.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 487 bytes
from .path import Path

class CircleMarker(Path):

    def __init__(self, latLng, options=None):
        super().__init__()
        self.latLng = latLng
        self.options = options
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'L.circleMarker({latLng}'.format(latLng=(self.latLng))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)