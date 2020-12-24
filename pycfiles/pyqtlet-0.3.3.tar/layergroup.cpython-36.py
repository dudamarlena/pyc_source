# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet_examples/pyqtlet/leaflet/layer/layergroup.py
# Compiled at: 2018-09-25 05:41:06
# Size of source mod 2**32: 1340 bytes
from .layer import Layer

class LayerGroup(Layer):
    __doc__ = '\n    Used to group several layers and handle them as one. If you add it to the map, any layers added or removed from the group will be added/removed on the map as well. \n    '

    @property
    def layers(self):
        return self._layers

    def __init__(self):
        super().__init__()
        self._layers = []
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'new L.layerGroup()'
        self._createJsObject(leafletJsObject)

    def addLayer(self, layer):
        self._layers.append(layer)
        js = '{layerGroup}.addLayer({layerName})'.format(layerGroup=(self._layerName), layerName=(layer._layerName))
        self.runJavaScript(js)

    def removeLayer(self, layer):
        if layer not in self._layers:
            return
        self._layers.remove(layer)
        js = '{layerGroup}.removeLayer({layerName})'.format(layerGroup=(self._layerName), layerName=(layer._layerName))
        self.runJavaScript(js)

    def clearLayers(self):
        js = '{layerGroup}.clearLayers()'.format(layerGroup=(self._layerName))
        self.runJavaScript(js)

    def toGeoJSON(self, callback):
        self.getJsResponse('{layer}.toGeoJSON()'.format(layer=(self.jsName)), callback)