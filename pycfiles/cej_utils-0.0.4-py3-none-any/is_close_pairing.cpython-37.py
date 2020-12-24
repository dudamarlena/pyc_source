# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caidan/Projects/cej-utils/cej_utils/is_close_pairing.py
# Compiled at: 2020-02-14 16:59:04
# Size of source mod 2**32: 2708 bytes
from shapely.geometry import Point, MultiPoint, Polygon, LineString
from shapely.ops import split, nearest_points, snap
LARGE_DISTANCE = 10000000

def min_arc_length(tooth_boundary, pts):
    """
    Finds the minimum arc length between two points on a closed boundary.
    """
    multi_pts = MultiPoint(pts)
    cmp_pts = [Point(pts[0]), Point(pts[1])]
    s = split(tooth_boundary, multi_pts)

    def eq_fn(p1, p2):
        """ Check if two points are essentially the same. """
        return p1.almost_equals(p2, 2)

    select_frag = None
    for s_frag in s:
        frag_pts = [
         Point(s_frag.coords[0]), Point(s_frag.coords[(-1)])]
        if not (eq_fn(frag_pts[0], cmp_pts[0]) and eq_fn(frag_pts[1], cmp_pts[1])):
            if not eq_fn(frag_pts[0], cmp_pts[1]) or eq_fn(frag_pts[1], cmp_pts[0]):
                select_frag = s_frag
                break

    if select_frag:
        frag_length = select_frag.length
        complement_frag_length = tooth_boundary.length - frag_length
        return (min(frag_length, complement_frag_length), select_frag)
    print('no match')
    return (LARGE_DISTANCE, LARGE_DISTANCE)


def create_shapely_polygon(geometry):
    """
    Creates shapely polygon
    """
    p = []
    for xy in geometry:
        p.append((xy['x'], xy['y']))

    return Polygon(p)


def is_close_pairing_on_arc(pt1, pt2, tooth_poly):
    """
    Checks if pt1 is close to pt2 by comparing straight line distance to distance along
    tooth boundary.
    """
    if not isinstance(tooth_poly, Polygon):
        try:
            shapely_poly = create_shapely_polygon(tooth_poly)
        except Exception as e:
            try:
                print(f"EXCEPTION_tooth_poly: {tooth_poly}")
                raise e
            finally:
                e = None
                del e

    else:
        shapely_poly = tooth_poly
    tooth_boundary = shapely_poly.boundary
    npt0_0, npt0_1 = nearest_points(tooth_boundary, Point(pt1[0]['x'], pt1[0]['y']))
    npt1_0, npt1_1 = nearest_points(tooth_boundary, Point(pt2[0]['x'], pt2[0]['y']))
    new_pts = [npt0_0, npt1_0]
    line = LineString(new_pts)
    new_tooth_boundary = snap(tooth_boundary, line, 0.1)
    min_length_along_arc, s_arc = min_arc_length(new_tooth_boundary, new_pts)
    val = line.length * 1.5 > min_length_along_arc
    return val