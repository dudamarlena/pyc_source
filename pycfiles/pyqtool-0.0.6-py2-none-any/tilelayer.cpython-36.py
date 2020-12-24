# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/samhattangady/projects/skylark/pyqtlet/pyqtlet/leaflet/layer/tile/tilelayer.py
# Compiled at: 2018-05-21 03:35:26
# Size of source mod 2**32: 526 bytes
from . import GridLayer

class TileLayer(GridLayer):

    def __init__(self, urlTemplate, options=None):
        super().__init__()
        self.urlTemplate = urlTemplate
        self.options = options
        self._initJs()

    def _initJs(self):
        leafletJsObject = 'L.tileLayer("{urlTemplate}"'.format(urlTemplate=(self.urlTemplate))
        if self.options:
            leafletJsObject += ', {options}'.format(options=(self.options))
        leafletJsObject += ')'
        self._createJsObject(leafletJsObject)