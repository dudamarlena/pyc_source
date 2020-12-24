# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/util.py
# Compiled at: 2020-05-08 13:24:17
# Size of source mod 2**32: 617 bytes
import functools, operator
COORDS_TILED = 'xyzw'
COORDS_IN_TILE = 'ijkl'
COORDS_IN_ORIG = 'pqrs'
MAX_DRAM_BANK = 4

def serialize(vec, tile_size):
    return sum((vec[i] * functools.reduce(operator.mul, tile_size[:i]) for i in range(1, len(tile_size))), vec[0])


def serialize_iter(iterative, tile_size):
    return [serialize(x, tile_size) for x in iterative]


def deserialize(offset, tile_size):
    return tuple(deserialize_generator(offset, tile_size))


def deserialize_generator(offset, tile_size):
    for size in tile_size[:-1]:
        yield offset % size
        offset = offset // size

    yield offset