# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/grids.py
# Compiled at: 2019-12-06 13:46:29
# Size of source mod 2**32: 939 bytes
from itertools import islice
import numpy as np

class GridParseError(Exception):
    pass


def load_grid(file_path):
    with open(file_path, 'r') as (ifp):
        return load_grid_stream(ifp)


def load_grid_stream(ifp):
    grid_size = None
    grid_origin = None
    for l in ifp:
        l = l.strip()
        if l.startswith('#'):
            continue
        else:
            if l.startswith('object 1'):
                grid_size = np.array([int(x) for x in l.split(' ')[-3:]])
            else:
                if l.startswith('origin'):
                    grid_origin = np.array([float(x) for x in l.split(' ')[-3:]])
                elif l.endswith('data follows'):
                    break

    if grid_size is None:
        raise GridParseError('No grid size specified')
    arr = np.loadtxt(islice(ifp, 0, grid_size.prod()))
    if arr.size != grid_size.prod():
        raise GridParseError('Incorrect number of elements')
    arr = arr.reshape(grid_size)
    return (
     arr, grid_origin)