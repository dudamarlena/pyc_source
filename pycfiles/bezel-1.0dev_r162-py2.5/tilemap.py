# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/graphics/widgets/tiles/tilemap.py
# Compiled at: 2009-02-25 04:20:27


class BaseTilemap(object):

    def __init__(self, map_size, tile_size, *args, **kwargs):
        super(BaseTilemap, self).__init__(*args, **kwargs)
        self.map_size = map_size
        self.tile_size = tile_size
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def __iter__(self):
        z = 0
        for layer in self.layers:
            if isinstance(layer, dict):
                for (x, y) in layer:
                    item = layer[(x, y)]
                    yield ((x, y, z), item)

            else:
                for (y, row) in enumerate(layer):
                    for (x, item) in enumerate(row):
                        yield (
                         (
                          x, y, z), item)