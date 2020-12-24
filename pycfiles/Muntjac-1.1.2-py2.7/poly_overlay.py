# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/google_maps/overlay/poly_overlay.py
# Compiled at: 2013-04-04 15:36:36


class PolyOverlay(object):

    def __init__(self, Id, points, color='#ffffff', weight=1, opacity=1.0, clickable=False):
        self._id = Id
        self._points = points
        self._color = color
        self._weight = weight
        self._opacity = opacity
        self._clickable = clickable

    def getId(self):
        return self._id

    def setId(self, Id):
        self._id = Id

    def getPoints(self):
        return self._points

    def setPoints(self, points):
        self._points = points

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def getWeight(self):
        return self._weight

    def setWeight(self, weight):
        self._weight = weight

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity

    def isClickable(self):
        return self._clickable

    def setClickable(self, clickable):
        self._clickable = clickable