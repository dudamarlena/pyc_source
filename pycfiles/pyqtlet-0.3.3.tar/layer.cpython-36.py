# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/layer.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 1809 bytes
from ..core import Evented

class Layer(Evented):
    layerId = 0

    @property
    def layerName(self):
        return self._layerName

    @layerName.setter
    def layerName(self, name):
        self._layerName = name

    @property
    def jsName(self):
        return self._layerName

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map_):
        self._map = map_

    def __init__(self):
        super().__init__()
        self._map = None
        self._layerName = self._getNewLayerName()

    def _getNewLayerName(self):
        layerName = 'l{}'.format(self.layerId)
        Layer.layerId += 1
        return layerName

    def addTo(self, map_):
        map_.addLayer(self)

    def removeFrom(self, map_):
        map_.removeLayer(self)

    def bindPopup(self, content, options=None):
        js = '{layerName}.bindPopup("{content}"'.format(layerName=(self._layerName),
          content=content)
        if options:
            js += ', {options}'.format(self._stringifyForJs(options))
        js += ')'
        self.runJavaScript(js)

    def unbindPopup(self):
        js = '{layerName}.unbindPopup()'.format(layerName=(self._layerName))
        self.runJavaScript(js)

    def bindTooltip(self, content, options=None):
        js = '{layerName}.bindTooltip("{content}"'.format(layerName=(self._layerName),
          content=content)
        if options:
            js += ', {options}'.format(self._stringifyForJs(options))
        js += ')'
        self.runJavaScript(js)

    def unbindTooltip(self):
        js = '{layerName}.unbindTooltip()'.format(layerName=(self._layerName))
        self.runJavaScript(js)