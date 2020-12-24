# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/util.py
# Compiled at: 2009-07-28 20:05:00
"""Defines utility functions used throughout the geocell/GeoModel library."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import geocell, geomath, geotypes

def merge_in_place(*lists, **kwargs):
    """Merges an arbitrary number of pre-sorted lists in-place, into the first
  list, possibly pruning out duplicates. Source lists must not have
  duplicates.

  Args:
    list1: The first, sorted list into which the other lists should be merged.
    list2: A subsequent, sorted list to merge into the first.
    ...
    listn:  "   "
    cmp_fn: An optional binary comparison function that compares objects across
        lists and determines the merged list's sort order.
    dup_fn: An optional binary comparison function that should return True if
        the given objects are equivalent and one of them can be pruned from the
        resulting merged list.

  Returns:
    list1, in-placed merged wit the other lists, or an empty list if no lists
    were specified.
  """
    cmp_fn = kwargs.get('cmp_fn') or cmp
    dup_fn = kwargs.get('dup_fn') or None
    if not lists:
        return []
    reverse_indices = [ len(arr) for arr in lists ]
    aggregate_reverse_index = sum(reverse_indices)
    while aggregate_reverse_index > 0:
        pull_arr_index = None
        pull_val = None
        for i in range(len(lists)):
            if reverse_indices[i] == 0:
                pass
            elif pull_arr_index is not None and dup_fn and dup_fn(lists[i][(-reverse_indices[i])], pull_val):
                reverse_indices[i] -= 1
                aggregate_reverse_index -= 1
            elif pull_arr_index is None or cmp_fn(lists[i][(-reverse_indices[i])], pull_val) < 0:
                pull_arr_index = i
                pull_val = lists[i][(-reverse_indices[i])]

        if pull_arr_index != 0:
            lists[0].insert(len(lists[0]) - reverse_indices[0], pull_val)
        aggregate_reverse_index -= 1
        reverse_indices[pull_arr_index] -= 1

    return lists[0]


def distance_sorted_edges(cells, point):
    """Returns the edges of the rectangular region containing all of the
  given geocells, sorted by distance from the given point, along with
  the actual distances from the point to these edges.

  Args:
    cells: The cells (should be adjacent) defining the rectangular region
        whose edge distances are requested.
    point: The point that should determine the edge sort order.

  Returns:
    A list of (direction, distance) tuples, where direction is the edge
    and distance is the distance from the point to that edge. A direction
    value of (0,-1), for example, corresponds to the South edge of the
    rectangular region containing all of the given geocells.
  """
    boxes = [ geocell.compute_box(cell) for cell in cells ]
    max_box = geotypes.Box(max([ box.north for box in boxes ]), max([ box.east for box in boxes ]), min([ box.south for box in boxes ]), min([ box.west for box in boxes ]))
    return zip(*sorted([
     (
      (0, -1),
      geomath.distance(geotypes.Point(max_box.south, point.lon), point)),
     (
      (0, 1),
      geomath.distance(geotypes.Point(max_box.north, point.lon), point)),
     (
      (-1, 0),
      geomath.distance(geotypes.Point(point.lat, max_box.west), point)),
     (
      (1, 0),
      geomath.distance(geotypes.Point(point.lat, max_box.east), point))], lambda x, y: cmp(x[1], y[1])))