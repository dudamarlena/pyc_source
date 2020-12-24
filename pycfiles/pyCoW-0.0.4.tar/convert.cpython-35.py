# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pycovjson/convert.py
# Compiled at: 2016-11-10 06:15:19
# Size of source mod 2**32: 821 bytes
from pycovjson.read_netcdf import NetCDFReader as Reader
from pycovjson.write import Writer
from pycovjson.model import TileSet

def main(input_file, output_file, variable, tiled=False, tile_shape=[], axis=''):
    if output_file == None:
        output_file = 'coverage.json'

    def tile_by_axis(variable, axis):
        """

        :param variable:
        :param axis:
        :return: tile_shape
        """
        shape = Reader.get_shape(variable)
        TileSet.create_tileset()
        return tile_shape

    if tiled:
        tile_shape = tile_by_axis(variable, axis)
    Writer(output_file, input_file, [variable], tiled=tiled, tile_shape=tile_shape).write()


if __name__ == '__main__':
    main()