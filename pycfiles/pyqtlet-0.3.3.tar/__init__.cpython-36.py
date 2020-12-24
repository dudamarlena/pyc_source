# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/__init__.py
# Compiled at: 2018-09-18 02:36:48
# Size of source mod 2**32: 647 bytes
from .map import Map
from .layer import LayerGroup, FeatureGroup, imageOverlay
from .layer.tile import TileLayer
from .layer.marker import Marker
from .layer.vector import Circle, CircleMarker, Polygon, Polyline, Rectangle
from .control import Control

class L:
    __doc__ = '\n    Leaflet namespace that holds reference to all the leaflet objects\n    '
    map = Map
    tileLayer = TileLayer
    imageOverlay = imageOverlay
    marker = Marker
    circleMarker = CircleMarker
    polyline = Polyline
    polygon = Polygon
    rectangle = Rectangle
    circle = Circle
    layerGroup = LayerGroup
    featureGroup = FeatureGroup
    control = Control