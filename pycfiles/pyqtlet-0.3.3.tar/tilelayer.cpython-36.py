# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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