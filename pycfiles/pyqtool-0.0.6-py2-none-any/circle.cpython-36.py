# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/vector/circle.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 513 bytes
from .circlemarker import CircleMarker

class Circle(CircleMarker):

    def __init__(self, latLng, radius, options=None):
        self.radius = radius
        super().__init__(latLng, options)

    def _initJs(self):
        leafletJsObject = 'L.circle({latLng},{radius}'.format(latLng=(self.latLng), radius=(self.radius))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)