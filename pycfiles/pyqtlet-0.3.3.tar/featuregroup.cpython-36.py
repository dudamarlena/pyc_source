# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/featuregroup.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 1514 bytes
from .layergroup import LayerGroup
from ..layer import marker, vector

class FeatureGroup(LayerGroup):
    __doc__ = '\n    Used to group several layers and handle them as one. If you add it to the map, any layers added or removed from the group will be added/removed on the map as well. \n    '

    def _initJs(self):
        leafletJsObject = 'new L.featureGroup()'
        self._createJsObject(leafletJsObject)

    def createAndAddDrawnLayer(self, drawnLayer, options=None):
        layerType = drawnLayer['layerType']
        if layerType == 'polygon':
            coords = drawnLayer['layer']['_latlngs']['0']
            coords = [coords[p] for p in coords]
            self.addLayer(vector.Polygon(coords, options))
        else:
            if layerType == 'marker':
                coords = drawnLayer['layer']['_latlng']
                self.addLayer(marker.Marker(coords, options))
            else:
                if layerType == 'polyline':
                    coords = drawnLayer['layer']['_latlngs']
                    coords = [coords[p] for p in coords]
                    self.addLayer(vector.Polyline(coords, options))
                else:
                    if layerType == 'rectangle':
                        coords = drawnLayer['layer']['_latlngs']['0']
                        coords = [coords[p] for p in coords]
                        self.addLayer(vector.Rectangle(coords, options))
                    elif layerType == 'circle':
                        coords = drawnLayer['layer']['_latlng']
                        radius = drawnLayer['layer']['options']['radius']
                        self.addLayer(vector.Circle([coords['lat'], coords['lng']], radius))