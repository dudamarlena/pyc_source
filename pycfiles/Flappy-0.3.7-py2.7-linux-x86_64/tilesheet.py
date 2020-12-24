# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display/tilesheet.py
# Compiled at: 2014-03-13 10:09:15
from flappy import _core
from flappy._core import _Tilesheet

class Tilesheet(_Tilesheet):
    TILE_SCALE = 1
    TILE_ROTATION = 2
    TILE_RGB = 4
    TILE_ALPHA = 8
    TILE_TRANS_2x2 = 16
    TILE_SMOOTH = 4096
    TILE_BLEND_ADD = 65536
    TILE_BLEND_MASK = 983040

    def __init__(self, bitmap_data):
        self._bitmap_data = bitmap_data
        _Tilesheet.__init__(self, bitmap_data)

    def addTileRect(self, rect, center_point=None):
        _Tilesheet.addTileRect(self, rect, center_point)

    def drawTiles(self, graphics_obj, tile_data, flags=0):
        graphics_obj.drawTiles(self, tile_data, flags)