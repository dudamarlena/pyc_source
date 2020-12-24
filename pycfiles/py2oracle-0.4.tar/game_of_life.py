# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py2opencl/test/game_of_life.py
# Compiled at: 2014-11-11 10:50:58
from py2opencl import Py2OpenCL
import numpy
from numpy.random import randint
from ..compat import SafeArray
X, Y = (40, 40)

def show_iteration(grid, title=None):
    if title is not None:
        print '=====', title, '====='
    x, y = grid.shape
    for j in range(y):
        print ('').join((' ' if c == 0 else '*') for c in grid[:, j])

    print
    return


def next_it(x, y, dest, src):
    """
      neighbor coordinates:

       0, 1, 2,
       3,    4,
       5, 6, 7

    """
    live_neighbors = src[(x - 1, y - 1)] + src[(x, y - 1)] + src[(x + 1, y - 1)] + src[(x - 1, y)] + src[(x + 1, y)] + src[(x - 1, y + 1)] + src[(x, y + 1)] + src[(x + 1, y + 1)]
    if live_neighbors < 2:
        dest[(x, y)] = 0
    elif live_neighbors == 3:
        dest[(x, y)] = 1
    elif src[(x, y)] and live_neighbors == 2:
        dest[(x, y)] = 1
    elif live_neighbors > 3:
        dest[(x, y)] = 0
    else:
        dest[(x, y)] = 0


grid = randint(0, 2, size=(X, Y)).astype(numpy.dtype('uint8'))
show_iteration(grid, 'Initial Random State')
iterate = Py2OpenCL(next_it)
iterate.bind(grid, return_type='uchar')
for i in range(120):
    grid = iterate.apply(grid)
    show_iteration(grid, 'Generation %d' % i)