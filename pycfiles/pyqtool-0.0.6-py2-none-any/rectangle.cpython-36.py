# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/vector/rectangle.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 427 bytes
from .polygon import Polygon

class Rectangle(Polygon):

    def __init__(self, latLngs, options=None):
        super().__init__(latLngs, options)

    def _initJs(self):
        leafletJsObject = 'L.rectangle({latLngs}'.format(latLngs=(self.latLngs))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)