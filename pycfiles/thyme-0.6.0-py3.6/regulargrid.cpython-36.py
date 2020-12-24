# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thyme/grid/regulargrid.py
# Compiled at: 2020-04-06 09:21:33
# Size of source mod 2**32: 5596 bytes
"""
Utilities for representing and working with Regular Grids.

Regular, orthogonal lat-lon grids are presently supported.
"""
import math
EARTH_RADIUS_METERS = 6371000

class RegularGrid:
    __doc__ = 'Encapsulate information describing a regular lat-lon grid.\n\n    In this model, the grid extent (min/max x/y coordinates) represents its\n    outer envelope (corresponding with the outer edges of the outermost cells),\n    while the grid coordinates are defined at the center of each grid\n    cell, i.e. offset from the bottom-left corner of the cell by half the cell\n    width and half the cell height.\n\n    This representation of a regular grid was chosen in order to build\n    tesselations whose cell coordinates are evenly distributed within the\n    defined envelope. This is especially useful when several congruent regular\n    grids are to be defined adjacent to each other with shared edges, because\n    it allows the shared edges to be equidistant to neighboring points from\n    both grids while also allowing the points to be evenly spaced.\n\n    Attributes:\n        x_min: X-coordinate of the left edge of the bottom-left grid cell.\n        y_min: Y-coordinate of the bottom edge of the bottom-left grid cell.\n        x_max: X-coordinate of the right edge of the top-right grid cell.\n        y_max: Y-coordinate of the top edge of the top-right grid cell.\n        cellsize_x: Width of each regular grid cell in the x-direction.\n        cellsize_y: Height of each regular grid cell in the y-direction.\n        x_coords: List containing calculated x-coordinate of each grid column.\n            The coordinate identifies the center location of each grid cell\n            (for example, the x-coordinate of the first grid cell is equal to\n            origin_x + cellsize_x/2.\n        y_coords: List containing calculated y-coordinate of each grid row. The\n            coordinate identifies the center location of each grid cell (for\n            example, the y-coordinate of the first grid cell is equal to\n            origin_y + cellsize_y/2.\n    '

    def __init__(self, x_min, y_min, x_max, y_max, cellsize_x, cellsize_y):
        """Initialize RegularGrid object.

        Args:
            x_min: X-coordinate of the left edge of the bottom-left grid cell.
            y_min: Y-coordinate of the bottom edge of the bottom-left grid
                cell.
            x_max: X-coordinate of the right edge of the top-right grid cell.
            y_max: Y-coordinate of the top edge of the top-right grid cell.
            cellsize_x: Width of each regular grid cell in the x-direction.
            cellsize_y: Height of each regular grid cell in the y-direction.
        """
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.cellsize_x = cellsize_x
        self.cellsize_y = cellsize_y
        self.x_coords = None
        self.y_coords = None
        self.calc_gridpoints()

    def calc_gridpoints(self):
        """Calculate and store x/y coordinates of grid points."""
        x = self.x_min + self.cellsize_x / 2
        y = self.y_min + self.cellsize_y / 2
        self.x_coords = []
        while x <= self.x_max:
            self.x_coords.append(x)
            x += self.cellsize_x

        self.y_coords = []
        while y <= self.y_max:
            self.y_coords.append(y)
            y += self.cellsize_y

    @staticmethod
    def calc_cellsizes(lon_min, lat_min, lon_max, lat_max, target_cellsize_meters):
        """Calculate appropriate lat/lon cell sizes from target size in meters.

        Given a lat/lon extent and target cell size in meters, calculate actual
        x and y cell sizes (in decimal degrees) that approximate the target
        cell size while ensuring the extent is divided into a whole number of
        cells in the x and y directions.

        Because degrees-per-meter varies by latitude, the midpoint of the given
        extent is used to calculate the conversion factor, as it should
        represent the average value for the whole grid.

        Args:
            lon_min: Minimum longitude of extent.
            lat_min: Minimum latitude of extent.
            lon_max: Maximum longitude of extent.
            lat_max: Maximum latitude of extent.
            target_cellsize_meters: Target cell size, in meters. Actual
                calculated cell sizes will be approximations of this.

        Returns:
            A 2-tuple in the form (cellsize_x, cellsize_y)
        """
        grid_width = abs(lon_max - lon_min)
        grid_height = abs(lat_max - lat_min)
        lat_mid = lat_min + grid_height / 2
        lat_mid_radians = math.radians(lat_mid)
        meters_per_degree = EARTH_RADIUS_METERS * math.pi / 180 * math.cos(lat_mid_radians)
        target_cellsize_dd = target_cellsize_meters / meters_per_degree
        num_cells_x = int(round(grid_width / target_cellsize_dd))
        cellsize_x = grid_width / num_cells_x
        num_cells_y = int(round(grid_height / target_cellsize_dd))
        cellsize_y = grid_height / num_cells_y
        return (
         cellsize_x, cellsize_y)