# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/imageoverlay.py
# Compiled at: 2018-09-18 02:36:48
# Size of source mod 2**32: 576 bytes
from .layer import Layer

class imageOverlay(Layer):

    def __init__(self, imageURL, bounds, options=None):
        super().__init__()
        self.imageURL = imageURL
        self.bounds = bounds
        self.options = options
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'L.imageOverlay("{imageURL}",{bounds}'.format(imageURL=(self.imageURL), bounds=(self.bounds))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)