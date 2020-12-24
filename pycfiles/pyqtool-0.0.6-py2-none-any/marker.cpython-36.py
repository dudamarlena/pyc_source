# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/marker/marker.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 838 bytes
from ..layer import Layer

class Marker(Layer):

    def __init__(self, latLng, options=None):
        super().__init__()
        self.latLng = latLng
        self.options = options
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'L.marker({latLng}'.format(latLng=(self.latLng))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)

    def setLatLng(self, latLng):
        js = '{layerName}.setLatLng({latLng})'.format(layerName=(self._layerName),
          latLng=latLng)
        self.runJavaScript(js)

    def setOpacity(self, opacity):
        js = '{layerName}.setOpacity({latLng})'.format(layerName=(self._layerName),
          opacity=opacity)
        self.runJavaScript(js)