# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/tiles/tile_manager.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1989 bytes
"""
Object that can download tile images at various zoom levels
"""
from pyowm.commons.http_client import HttpClient
from pyowm.commons.image import Image
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.tile import Tile
from pyowm.tiles.uris import ROOT_TILE_URL

class TileManager(object):
    __doc__ = '\n    A manager objects that reads OWM map layers tile images .\n\n    :param API_key: the OWM Weather API key\n    :type API_key: str\n    :param map_layer: the layer for which you want tiles fetched. Allowed map layers are specified by the `pyowm.tiles.enum.MapLayerEnum` enumerator class.\n    :type map_layer: str\n    :returns: a *TileManager* instance\n    :raises: *AssertionError* when no API Key or no map layer is provided, or map layer name is not a string\n\n    '

    def __init__(self, API_key, map_layer):
        assert API_key is not None, 'You must provide a valid API Key'
        self.API_key = API_key
        assert map_layer is not None, 'You must provide a valid map layer name'
        assert isinstance(map_layer, str), 'Map layer name must be a string'
        self.map_layer = map_layer
        self.http_client = HttpClient()

    def get_tile(self, x, y, zoom):
        """
        Retrieves the tile having the specified coordinates and zoom level

        :param x: horizontal tile number in OWM tile reference system
        :type x: int
        :param y: vertical tile number in OWM tile reference system
        :type y: int
        :param zoom: zoom level for the tile
        :type zoom: int
        :returns: a `pyowm.tiles.Tile` instance

        """
        status, data = self.http_client.get_png(ROOT_TILE_URL % self.map_layer + '/%s/%s/%s.png' % (zoom, x, y), params={'appid': self.API_key})
        img = Image(data, ImageTypeEnum.PNG)
        return Tile(x, y, zoom, self.map_layer, img)

    def __repr__(self):
        return '<%s.%s - layer name=%s>' % (__name__, self.__class__.__name__, self.map_layer)