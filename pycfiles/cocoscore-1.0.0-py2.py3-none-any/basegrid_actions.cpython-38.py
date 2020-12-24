# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\actions\basegrid_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 13381 bytes
__doc__ = 'Grid Actions\n\nGrid Actions\n============\n\nThere are 2 kinds of grids:\n\n  - `Grid3D` : A 3D grid with x,y and z coordinates\n  - `TiledGrid3D` : A 3D grid with x,y and z coordinates, composed\n     with independent tiles\n\n\nHence, there are 2 kinds of grid actions:\n\n  - `Grid3DAction`\n  - `TiledGrid3DAction`\n\nThe `Grid3DAction` can modify any of vertex of the grid in any direction (x,y or z).\nThe `TiledGrid3DAction` can modify any tile of the grid without modifying the adjacent tiles.\n\nTo understand visually the difference between these 2 kinds of grids, try these examples:\n\n  - run ``test/test_shakytiles3d.py`` to see a `TiledGrid3DAction` example \n  - run ``test/test_shaky3d.py`` to see the `Grid3DAction` counterpart\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
from cocos.grid import Grid3D, TiledGrid3D
import cocos.director as director
from cocos.euclid import *
from .base_actions import *
__all__ = [
 'GridException',
 'GridBaseAction',
 'Grid3DAction',
 'TiledGrid3DAction',
 'AccelAmplitude',
 'DeccelAmplitude',
 'AccelDeccelAmplitude',
 'StopGrid',
 'ReuseGrid']

class GridException(Exception):
    pass


class GridBaseAction(IntervalAction):
    """GridBaseAction"""

    def init(self, grid=(4, 4), duration=5):
        """Initialize the Grid Action

        :Parameters:
            `grid` : (int,int)
                Number of horizontal and vertical quads in the grid
            `duration` : int 
                Number of seconds that the action will last
        """
        self.duration = duration
        if not isinstance(grid, Point2):
            grid = Point2(*grid)
        self.grid = grid

    def start(self):
        new_grid = self.get_grid()
        if self.target.grid and self.target.grid.reuse_grid > 0:
            if self.target.grid.active and self.grid == self.target.grid.grid and type(new_grid) == type(self.target.grid):
                self.target.grid.vertex_points = self.target.grid.vertex_list.vertices[:]
                self.target.grid.reuse_grid -= 1
                self.target.grid.reuse_grid = max(0, self.target.grid.reuse_grid)
            else:
                raise GridException('Cannot reuse grid. class grid or grid size did not match: %s vs %s and %s vs %s' % (
                 str(self.grid), str(self.target.grid.grid),
                 type(new_grid), type(self.target.grid)))
        else:
            if self.target.grid:
                if self.target.grid.active:
                    self.target.grid.active = False
            self.target.grid = new_grid
            self.target.grid.init(self.grid)
            self.target.grid.active = True
        x, y = director.get_window_size()
        self.size_x = x // self.grid.x
        self.size_y = y // self.grid.y

    def __reversed__(self):
        return _ReverseTime(self)


class Grid3DAction(GridBaseAction):
    """Grid3DAction"""

    def get_grid(self):
        return Grid3D()

    def get_vertex(self, x, y):
        """Get the current vertex coordinate

        :Parameters:
            `x` : int 
               x-vertex
            `y` : int
               y-vertex

        :rtype: (float, float, float)
        """
        return self.target.grid.get_vertex(x, y)

    def get_original_vertex(self, x, y):
        """Get the original vertex coordinate.
        The original vertices are the ones weren't modified by the current action.

        :Parameters:
            `x` : int 
               x-vertex
            `y` : int
               y-vertex

        :rtype: (float, float, float)
        """
        return self.target.grid.get_original_vertex(x, y)

    def set_vertex(self, x, y, v):
        """Set a vertex point is a certain value

        :Parameters:
            `x` : int 
               x-vertex
            `y` : int
               y-vertex
            `v` : (float, float, float)
                tuple value for the vertex
        """
        return self.target.grid.set_vertex(x, y, v)


class TiledGrid3DAction(GridBaseAction):
    """TiledGrid3DAction"""

    def get_grid(self):
        return TiledGrid3D()

    def set_tile(self, x, y, coords):
        """Set the 4 tile coordinates

        Coordinates positions::

            3 <-- 2
                  ^
                  |
            0 --> 1

        :Parameters:
            `x` : int 
                x coodinate of the tile
            `y` : int 
                y coordinate of the tile
            `coords` : [ float, float, float, float, float, float, float, float, float, float, float, float ]
                The 4 coordinates in the format (x0, y0, z0, x1, y1, z1,..., x3, y3, z3)
        """
        return self.target.grid.set_tile(x, y, coords)

    def get_original_tile(self, x, y):
        """Get the 4-original tile coordinates.

        Coordinates positions::

            3 <-- 2
                  ^
                  |
            0 --> 1

        :Parameters:
            `x` : int
                x coordinate of the tile
            `y` : int
                y coordinate of the tile

        :rtype: [ float, float, float, float, float, float, float, float, float, float, float, float ]
        :returns: The 4 coordinates with the following order: x0, y0, z0, x1, y1, z1,...,x3, y3, z3
        """
        return self.target.grid.get_original_tile(x, y)

    def get_tile(self, x, y):
        """Get the current tile coordinates.

        Coordinates positions::

            3 <-- 2
                  ^
                  |
            0 --> 1

        :Parameters:
            `x` : int
                x coordinate of the tile
            `y` : int
                y coordinate of the tile

        :rtype: [ float, float, float, float, float, float, float, float, float, float, float, float ]
        :returns: The 4 coordinates with the following order: x0, y0, z0, x1, y1, z1,...,x3, y3, z3
        """
        return self.target.grid.get_tile(x, y)


class AccelDeccelAmplitude(IntervalAction):
    """AccelDeccelAmplitude"""

    def init(self, other, rate=1.0):
        """Init method.

        :Parameters:
            `other` : `IntervalAction`
                The action that will be affected
            `rate` : float
                The acceleration rate. 1 is linear (default value)
        """
        if not hasattr(other, 'amplitude'):
            raise GridException('Invalid Composition: IncAmplitude needs an action with amplitude')
        self.other = other
        self.rate = rate
        self.duration = other.duration

    def start(self):
        self.other.target = self.target
        self.other.start()

    def update(self, t):
        f = t * 2
        if f > 1:
            f -= 1
            f = 1 - f
        self.other.amplitude_rate = f ** self.rate
        self.other.update(t)

    def __reversed__(self):
        return AccelDeccelAmplitude(Reverse(self.other))


class AccelAmplitude(IntervalAction):
    """AccelAmplitude"""

    def init(self, other, rate=1):
        """Init method.

        :Parameters:
            `other` : `IntervalAction`
                The action that will be affected
            `rate` : float
                The acceleration rate. 1 is linear (default value)
        """
        if not hasattr(other, 'amplitude'):
            raise GridException('Invalid Composition: IncAmplitude needs an action with amplitude')
        self.other = other
        self.duration = other.duration
        self.rate = rate

    def start(self):
        self.other.target = self.target
        self.other.start()

    def update(self, t):
        self.other.amplitude_rate = t ** self.rate
        self.other.update(t)

    def __reversed__(self):
        return DeccelAmplitude((Reverse(self.other)), rate=(self.rate))


class DeccelAmplitude(AccelAmplitude):
    """DeccelAmplitude"""

    def update(self, t):
        self.other.amplitude_rate = (1 - t) ** self.rate
        self.other.update(t)

    def __reversed__(self):
        return AccelAmplitude((Reverse(self.other)), rate=(self.rate))


class StopGrid(InstantAction):
    """StopGrid"""

    def start(self):
        if self.target.grid:
            if self.target.grid.active:
                self.target.grid.active = False


class ReuseGrid(InstantAction):
    """ReuseGrid"""

    def init(self, reuse_times=1):
        """
        :Parameters:
            `reuse_times` : int
                Number of times that the current grid will be reused by Grid actions. Default: 1
        """
        self.reuse_times = reuse_times

    def start(self):
        if self.target.grid and self.target.grid.active:
            self.target.grid.reuse_grid += self.reuse_times
        else:
            raise GridException('ReuseGrid must be used when a grid is still active')