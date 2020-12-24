# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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