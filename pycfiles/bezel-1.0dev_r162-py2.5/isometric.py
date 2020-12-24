# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/widgets/tiles/isometric.py
# Compiled at: 2009-02-25 04:20:27
from bezel.graphics.widget import Widget
from bezel.graphics.widgets.tiles.tilemap import BaseTilemap
import pygame

class IsometricTilemap(BaseTilemap, Widget):

    def __init__(self, *args, **kwargs):
        super(IsometricTilemap, self).__init__(*args, **kwargs)
        (map_width, map_height) = self.map_size
        (tile_width, tile_height) = self.tile_size
        self.size = (map_width * tile_width, map_height * tile_height / 2.0)

    def paint(self):
        super(IsometricTilemap, self).paint()
        surface = pygame.Surface(self.rect.size)
        map_height = self.map_size[1]
        (tile_width, tile_height) = self.tile_size
        blit = surface.blit
        for ((x, y, z), tile) in self:
            iso_x = x - y - 1 + map_height
            iso_y = (x + y - 1) / 2.0 - z
            iso_x *= tile_width / 2.0
            iso_y *= tile_height / 2.0
            blit(tile, (iso_x, iso_y))

        self.surface = surface