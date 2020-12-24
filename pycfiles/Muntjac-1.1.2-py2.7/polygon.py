# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/google_maps/overlay/polygon.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.addon.google_maps.overlay.poly_overlay import PolyOverlay

class Polygon(PolyOverlay):

    def __init__(self, Id, points, strokeColor='#ffffff', strokeWeight=1, strokeOpacity=1.0, fillColor='#777777', fillOpacity=0.2, clickable=False):
        super(Polygon, self).__init__(Id, points, strokeColor, strokeWeight, strokeOpacity, clickable)
        self._fillColor = fillColor
        self._fillOpacity = fillOpacity

    def getFillColor(self):
        return self._fillColor

    def setFillColor(self, fillColor):
        self._fillColor = fillColor

    def getFillOpacity(self):
        return self._fillOpacity

    def setFillOpacity(self, fillOpacity):
        self._fillOpacity = fillOpacity