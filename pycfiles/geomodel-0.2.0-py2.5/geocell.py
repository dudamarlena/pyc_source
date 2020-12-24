# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/geocell.py
# Compiled at: 2009-07-28 20:05:00
"""Defines the notion of 'geocells' and exposes methods to operate on them.

A geocell is a hexadecimal string that defines a two dimensional rectangular
region inside the [-90,90] x [-180,180] latitude/longitude space. A geocell's
'resolution' is its length. For most practical purposes, at high resolutions,
geocells can be treated as single points.

Much like geohashes (see http://en.wikipedia.org/wiki/Geohash), geocells are
hierarchical, in that any prefix of a geocell is considered its ancestor, with
geocell[:-1] being geocell's immediate parent cell.

To calculate the rectangle of a given geocell string, first divide the
[-90,90] x [-180,180] latitude/longitude space evenly into a 4x4 grid like so:

             +---+---+---+---+ (90, 180)
             | a | b | e | f |
             +---+---+---+---+
             | 8 | 9 | c | d |
             +---+---+---+---+
             | 2 | 3 | 6 | 7 |
             +---+---+---+---+
             | 0 | 1 | 4 | 5 |
  (-90,-180) +---+---+---+---+

NOTE: The point (0, 0) is at the intersection of grid cells 3, 6, 9 and c. And,
      for example, cell 7 should be the sub-rectangle from
      (-45, 90) to (0, 180).

Calculate the sub-rectangle for the first character of the geocell string and
re-divide this sub-rectangle into another 4x4 grid. For example, if the geocell
string is '78a', we will re-divide the sub-rectangle like so:

               .                   .
               .                   .
           . . +----+----+----+----+ (0, 180)
               | 7a | 7b | 7e | 7f |
               +----+----+----+----+
               | 78 | 79 | 7c | 7d |
               +----+----+----+----+
               | 72 | 73 | 76 | 77 |
               +----+----+----+----+
               | 70 | 71 | 74 | 75 |
  . . (-45,90) +----+----+----+----+
               .                   .
               .                   .

Continue to re-divide into sub-rectangles and 4x4 grids until the entire
geocell string has been exhausted. The final sub-rectangle is the rectangular
region for the geocell.
"""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import os.path, sys, geomath, geotypes
_GEOCELL_GRID_SIZE = 4
_GEOCELL_ALPHABET = '0123456789abcdef'
MAX_GEOCELL_RESOLUTION = 13
MAX_FEASIBLE_BBOX_SEARCH_CELLS = 300
NORTHWEST = (-1, 1)
NORTH = (0, 1)
NORTHEAST = (1, 1)
EAST = (1, 0)
SOUTHEAST = (1, -1)
SOUTH = (0, -1)
SOUTHWEST = (-1, -1)
WEST = (-1, 0)

def best_bbox_search_cells(bbox, cost_function):
    """Returns an efficient set of geocells to search in a bounding box query.

  This method is guaranteed to return a set of geocells having the same
  resolution.

  Args:
    bbox: A geotypes.Box indicating the bounding box being searched.
    cost_function: A function that accepts two arguments:
        * num_cells: the number of cells to search
        * resolution: the resolution of each cell to search
        and returns the 'cost' of querying against this number of cells
        at the given resolution.

  Returns:
    A list of geocell strings that contain the given box.
  """
    cell_ne = compute(bbox.north_east, resolution=MAX_GEOCELL_RESOLUTION)
    cell_sw = compute(bbox.south_west, resolution=MAX_GEOCELL_RESOLUTION)
    min_cost = float('inf')
    min_cost_cell_set = None
    min_resolution = len(os.path.commonprefix([cell_sw, cell_ne]))
    for cur_resolution in range(min_resolution, MAX_GEOCELL_RESOLUTION + 1):
        cur_ne = cell_ne[:cur_resolution]
        cur_sw = cell_sw[:cur_resolution]
        num_cells = interpolation_count(cur_ne, cur_sw)
        if num_cells > MAX_FEASIBLE_BBOX_SEARCH_CELLS:
            continue
        cell_set = sorted(interpolate(cur_ne, cur_sw))
        simplified_cells = []
        cost = cost_function(num_cells=len(cell_set), resolution=cur_resolution)
        if cost <= min_cost:
            min_cost = cost
            min_cost_cell_set = cell_set
        else:
            break

    return min_cost_cell_set


def collinear(cell1, cell2, column_test):
    """Determines whether the given cells are collinear along a dimension.

  Returns True if the given cells are in the same row (column_test=False)
  or in the same column (column_test=True).

  Args:
    cell1: The first geocell string.
    cell2: The second geocell string.
    column_test: A boolean, where False invokes a row collinearity test
        and 1 invokes a column collinearity test.

  Returns:
    A bool indicating whether or not the given cells are collinear in the given
    dimension.
  """
    for i in range(min(len(cell1), len(cell2))):
        (x1, y1) = _subdiv_xy(cell1[i])
        (x2, y2) = _subdiv_xy(cell2[i])
        if not column_test and y1 != y2:
            return False
        if column_test and x1 != x2:
            return False

    return True


def interpolate(cell_ne, cell_sw):
    """Calculates the grid of cells formed between the two given cells.

  Generates the set of cells in the grid created by interpolating from the
  given Northeast geocell to the given Southwest geocell.

  Assumes the Northeast geocell is actually Northeast of Southwest geocell.

  Arguments:
    cell_ne: The Northeast geocell string.
    cell_sw: The Southwest geocell string.

  Returns:
    A list of geocell strings in the interpolation.
  """
    cell_set = [
     [
      cell_sw]]
    while not collinear(cell_set[0][(-1)], cell_ne, True):
        cell_tmp = adjacent(cell_set[0][(-1)], (1, 0))
        if cell_tmp is None:
            break
        cell_set[0].append(cell_tmp)

    while cell_set[(-1)][(-1)] != cell_ne:
        cell_tmp_row = [ adjacent(g, (0, 1)) for g in cell_set[(-1)] ]
        if cell_tmp_row[0] is None:
            break
        cell_set.append(cell_tmp_row)

    return [ g for inner in cell_set for g in inner ]


def interpolation_count(cell_ne, cell_sw):
    """Computes the number of cells in the grid formed between two given cells.

  Computes the number of cells in the grid created by interpolating from the
  given Northeast geocell to the given Southwest geocell. Assumes the Northeast
  geocell is actually Northeast of Southwest geocell.

  Arguments:
    cell_ne: The Northeast geocell string.
    cell_sw: The Southwest geocell string.

  Returns:
    An int, indicating the number of geocells in the interpolation.
  """
    bbox_ne = compute_box(cell_ne)
    bbox_sw = compute_box(cell_sw)
    cell_lat_span = bbox_sw.north - bbox_sw.south
    cell_lon_span = bbox_sw.east - bbox_sw.west
    num_cols = int((bbox_ne.east - bbox_sw.west) / cell_lon_span)
    num_rows = int((bbox_ne.north - bbox_sw.south) / cell_lat_span)
    return num_cols * num_rows


def all_adjacents(cell):
    """Calculates all of the given geocell's adjacent geocells.

  Args:
    cell: The geocell string for which to calculate adjacent/neighboring cells.

  Returns:
    A list of 8 geocell strings and/or None values indicating adjacent cells.
  """
    return [ adjacent(cell, d) for d in [NORTHWEST, NORTH, NORTHEAST, EAST,
     SOUTHEAST, SOUTH, SOUTHWEST, WEST]
           ]


def adjacent(cell, dir):
    """Calculates the geocell adjacent to the given cell in the given direction.

  Args:
    cell: The geocell string whose neighbor is being calculated.
    dir: An (x, y) tuple indicating direction, where x and y can be -1, 0, or 1.
        -1 corresponds to West for x and South for y, and
         1 corresponds to East for x and North for y.
        Available helper constants are NORTH, EAST, SOUTH, WEST,
        NORTHEAST, NORTHWEST, SOUTHEAST, and SOUTHWEST.

  Returns:
    The geocell adjacent to the given cell in the given direction, or None if
    there is no such cell.
  """
    if cell is None:
        return
    dx = dir[0]
    dy = dir[1]
    cell_adj_arr = list(cell)
    i = len(cell_adj_arr) - 1
    while i >= 0 and (dx != 0 or dy != 0):
        (x, y) = _subdiv_xy(cell_adj_arr[i])
        if dx == -1:
            if x == 0:
                x = _GEOCELL_GRID_SIZE - 1
            else:
                x -= 1
                dx = 0
        elif dx == 1:
            if x == _GEOCELL_GRID_SIZE - 1:
                x = 0
            else:
                x += 1
                dx = 0
        if dy == 1:
            if y == _GEOCELL_GRID_SIZE - 1:
                y = 0
            else:
                y += 1
                dy = 0
        elif dy == -1:
            if y == 0:
                y = _GEOCELL_GRID_SIZE - 1
            else:
                y -= 1
                dy = 0
        cell_adj_arr[i] = _subdiv_char((x, y))
        i -= 1

    if dy != 0:
        return
    return ('').join(cell_adj_arr)


def contains_point(cell, point):
    """Returns whether or not the given cell contains the given point."""
    return compute(point, len(cell)) == cell


def point_distance(cell, point):
    """Returns the shortest distance between a point and a geocell bounding box.

  If the point is inside the cell, the shortest distance is always to a 'edge'
  of the cell rectangle. If the point is outside the cell, the shortest distance
  will be to either a 'edge' or 'corner' of the cell rectangle.

  Returns:
    The shortest distance from the point to the geocell's rectangle, in meters.
  """
    bbox = compute_box(cell)
    between_w_e = bbox.west <= point.lon and point.lon <= bbox.east
    between_n_s = bbox.south <= point.lat and point.lat <= bbox.north
    if between_w_e:
        if between_n_s:
            return min(geomath.distance(point, (bbox.south, point.lon)), geomath.distance(point, (bbox.north, point.lon)), geomath.distance(point, (point.lat, bbox.east)), geomath.distance(point, (point.lat, bbox.west)))
        else:
            return min(geomath.distance(point, (bbox.south, point.lon)), geomath.distance(point, (bbox.north, point.lon)))
    elif between_n_s:
        return min(geomath.distance(point, (point.lat, bbox.east)), geomath.distance(point, (point.lat, bbox.west)))
    else:
        return min(geomath.distance(point, (bbox.south, bbox.east)), geomath.distance(point, (bbox.north, bbox.east)), geomath.distance(point, (bbox.south, bbox.west)), geomath.distance(point, (bbox.north, bbox.west)))


def compute(point, resolution=MAX_GEOCELL_RESOLUTION):
    """Computes the geocell containing the given point to the given resolution.

  This is a simple 16-tree lookup to an arbitrary depth (resolution).

  Args:
    point: The geotypes.Point to compute the cell for.
    resolution: An int indicating the resolution of the cell to compute.

  Returns:
    The geocell string containing the given point, of length <resolution>.
  """
    north = 90.0
    south = -90.0
    east = 180.0
    west = -180.0
    cell = ''
    while len(cell) < resolution:
        subcell_lon_span = (east - west) / _GEOCELL_GRID_SIZE
        subcell_lat_span = (north - south) / _GEOCELL_GRID_SIZE
        x = min(int(_GEOCELL_GRID_SIZE * (point.lon - west) / (east - west)), _GEOCELL_GRID_SIZE - 1)
        y = min(int(_GEOCELL_GRID_SIZE * (point.lat - south) / (north - south)), _GEOCELL_GRID_SIZE - 1)
        cell += _subdiv_char((x, y))
        south += subcell_lat_span * y
        north = south + subcell_lat_span
        west += subcell_lon_span * x
        east = west + subcell_lon_span

    return cell


def compute_box(cell):
    """Computes the rectangular boundaries (bounding box) of the given geocell.

  Args:
    cell: The geocell string whose boundaries are to be computed.

  Returns:
    A geotypes.Box corresponding to the rectangular boundaries of the geocell.
  """
    if cell is None:
        return
    bbox = geotypes.Box(90.0, 180.0, -90.0, -180.0)
    while len(cell) > 0:
        subcell_lon_span = (bbox.east - bbox.west) / _GEOCELL_GRID_SIZE
        subcell_lat_span = (bbox.north - bbox.south) / _GEOCELL_GRID_SIZE
        (x, y) = _subdiv_xy(cell[0])
        bbox = geotypes.Box(bbox.south + subcell_lat_span * (y + 1), bbox.west + subcell_lon_span * (x + 1), bbox.south + subcell_lat_span * y, bbox.west + subcell_lon_span * x)
        cell = cell[1:]

    return bbox


def is_valid(cell):
    """Returns whether or not the given geocell string defines a valid geocell."""
    return bool(cell and reduce(lambda val, c: val and c in _GEOCELL_ALPHABET, cell, True))


def children(cell):
    """Calculates the immediate children of the given geocell.

  For example, the immediate children of 'a' are 'a0', 'a1', ..., 'af'.
  """
    return [ cell + chr for chr in _GEOCELL_ALPHABET ]


def _subdiv_xy(char):
    """Returns the (x, y) of the geocell character in the 4x4 alphabet grid."""
    char = _GEOCELL_ALPHABET.index(char)
    return ((char & 4) >> 1 | (char & 1) >> 0,
     (char & 8) >> 2 | (char & 2) >> 1)


def _subdiv_char(pos):
    """Returns the geocell character in the 4x4 alphabet grid at pos. (x, y)."""
    return _GEOCELL_ALPHABET[((pos[1] & 2) << 2 | (pos[0] & 2) << 1 | (pos[1] & 1) << 1 | (pos[0] & 1) << 0)]