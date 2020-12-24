# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/higlass/tilesets.py
# Compiled at: 2020-01-26 00:21:31
# Size of source mod 2**32: 5493 bytes
import pandas as pd, numpy as np, slugid, h5py
from clodius.tiles.utils import tiles_wrapper_2d, bundled_tiles_wrapper_2d
from clodius.tiles.format import format_dense_tile

class Tileset:
    __doc__ = '\n    Object representing a data tileset.\n\n    Parameters\n    ----------\n    uuid : str\n        Tileset uid\n    tileset_info : callable\n        A function returning the information (min_pos, max_pos, max_width,\n        max_zoom) for this tileset.\n    tiles : callable\n        A function returning tile data for this tileset.\n    datatype : str\n        Datatype identifier for the viewer\n    name : str, optional\n        Name for the tileset. Also used as display name for the track.\n\n    '

    def __init__(self, uuid=None, tileset_info=None, tiles=None, chromsizes=lambda : None, datatype='unspecified', name=None, private=False):
        self.uuid = slugid.nice() if uuid is None else uuid
        self.name = name
        self.tileset_info_fn = tileset_info
        self.tiles_fn = tiles
        self.chromsizes_fn = chromsizes
        self.datatype = datatype
        self.private = private

    def tileset_info(self):
        info = self.tileset_info_fn()
        if self.name is not None:
            info['name'] = self.name
        return info

    def tiles(self, tile_ids):
        return self.tiles_fn(tile_ids)

    @property
    def meta(self):
        return {'uuid':self.uuid, 
         'datatype':self.datatype, 
         'private':self.private, 
         'name':self.name}


class ChromSizes(Tileset):

    def __init__(self, chromsizes, **kwargs):
        (super().__init__)(**kwargs)
        self.chromsizes = chromsizes


def chromsizes(filepath, uuid=None, **kwargs):
    from clodius.tiles.chromsizes import get_tsv_chromsizes
    return ChromSizes(uuid=uuid, 
     chromsizes=get_tsv_chromsizes(filepath), 
     datatype='chromsizes', **kwargs)


def cooler(filepath, uuid=None, **kwargs):
    from clodius.tiles.cooler import tileset_info, tiles
    return Tileset(uuid=uuid, 
     tileset_info=lambda : tileset_info(filepath), 
     tiles=lambda tids: tiles(filepath, tids), 
     datatype='matrix', **kwargs)


def beddb(filepath, uuid=None, **kwargs):
    from clodius.tiles.beddb import tileset_info, tiles
    return Tileset(uuid=uuid, 
     tileset_info=lambda : tileset_info(filepath), 
     tiles=lambda tids: tiles(filepath, tids), **kwargs)


def bigbed(filepath, uuid=None, chromsizes=None, **kwargs):
    from clodius.tiles.bigbed import tileset_info, tiles
    return Tileset(uuid=uuid, 
     tileset_info=lambda : tileset_info(filepath, chromsizes), 
     tiles=lambda tids: tiles(filepath, tids, chromsizes=chromsizes), **kwargs)


def bigwig(filepath, uuid=None, chromsizes=None, **kwargs):
    from clodius.tiles.bigwig import tileset_info, tiles
    return Tileset(uuid=uuid, 
     tileset_info=lambda : tileset_info(filepath, chromsizes), 
     tiles=lambda tids: tiles(filepath, tids, chromsizes=chromsizes), 
     datatype='vector', **kwargs)


def mrmatrix(filepath, uuid=None, **kwargs):
    from clodius.tiles.mrmatrix import tileset_info, tiles
    f = h5py.File(filepath, 'r')
    return Tileset(uuid=uuid, 
     tileset_info=lambda : tileset_info(f), 
     tiles=lambda tile_ids: tiles_wrapper_2d(tile_ids, lambda z, x, y: format_dense_tile(tiles(f, z, x, y))), 
     datatype='matrix', **kwargs)


def nplabels(labels_array, uuid=None, importances=None, **kwargs):
    """1d labels"""
    from clodius.tiles import nplabels
    from clodius.tiles import npvector
    return Tileset(uuid=uuid, 
     tileset_info=lambda : npvector.tileset_info(labels_array, bins_per_dimension=16), 
     tiles=lambda tids: nplabels.tiles_wrapper(labels_array, tids, importances), 
     datatype='linear-labels', **kwargs)


def h5labels(filename, uuid=None, importances=None, **kwargs):
    f = h5py.File(filename, 'r')
    return nplabels((f['labels']), uuid, importances, **kwargs)


def dfpoints--- This code section failed: ---

 L. 188         0  LOAD_CONST               0
                2  LOAD_CONST               ('tileset_info', 'tiles', 'format_data')
                4  IMPORT_NAME_ATTR         clodius.tiles.points
                6  IMPORT_FROM              tileset_info
                8  STORE_FAST               'tileset_info'
               10  IMPORT_FROM              tiles
               12  STORE_DEREF              'tiles'
               14  IMPORT_FROM              format_data
               16  STORE_DEREF              'format_data'
               18  POP_TOP          

 L. 190        20  LOAD_FAST                'tileset_info'
               22  LOAD_DEREF               'df'
               24  LOAD_DEREF               'x_col'
               26  LOAD_DEREF               'y_col'
               28  CALL_FUNCTION_3       3  '3 positional arguments'
               30  STORE_DEREF              'tsinfo'

 L. 191        32  LOAD_CONST               (1, 1)
               34  LOAD_CLOSURE             'df'
               36  LOAD_CLOSURE             'tiles'
               38  LOAD_CLOSURE             'tsinfo'
               40  LOAD_CLOSURE             'x_col'
               42  LOAD_CLOSURE             'y_col'
               44  BUILD_TUPLE_5         5 
               46  LOAD_LAMBDA              '<code_object <lambda>>'
               48  LOAD_STR                 'dfpoints.<locals>.<lambda>'
               50  MAKE_FUNCTION_9          'default, closure'
               52  STORE_DEREF              'tiles_fn'

 L. 195        54  LOAD_GLOBAL              Tileset
               56  BUILD_TUPLE_0         0 

 L. 196        58  LOAD_FAST                'uuid'

 L. 197        60  LOAD_CLOSURE             'tsinfo'
               62  BUILD_TUPLE_1         1 
               64  LOAD_LAMBDA              '<code_object <lambda>>'
               66  LOAD_STR                 'dfpoints.<locals>.<lambda>'
               68  MAKE_FUNCTION_8          'closure'

 L. 198        70  LOAD_CLOSURE             'format_data'
               72  LOAD_CLOSURE             'tiles_fn'
               74  BUILD_TUPLE_2         2 
               76  LOAD_LAMBDA              '<code_object <lambda>>'
               78  LOAD_STR                 'dfpoints.<locals>.<lambda>'
               80  MAKE_FUNCTION_8          'closure'

 L. 201        82  LOAD_STR                 'scatter-point'
               84  LOAD_CONST               ('uuid', 'tileset_info', 'tiles', 'datatype')
               86  BUILD_CONST_KEY_MAP_4     4 

 L. 202        88  LOAD_FAST                'kwargs'
               90  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               92  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               94  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_FUNCTION_9' instruction at offset 50


by_filetype = {'cooler':cooler, 
 'bigwig':bigwig, 
 'mrmatrix':mrmatrix, 
 'h5labels':h5labels}