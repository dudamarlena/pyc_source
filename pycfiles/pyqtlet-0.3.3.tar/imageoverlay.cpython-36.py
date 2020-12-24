# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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