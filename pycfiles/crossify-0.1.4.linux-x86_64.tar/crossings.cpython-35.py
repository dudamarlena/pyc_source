# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/crossings.py
# Compiled at: 2017-12-11 15:01:39
# Size of source mod 2**32: 10056 bytes
import geopandas as gpd, numpy as np
from shapely.geometry import LineString, Point, Polygon
from . import validators

def make_crossings(intersections_dict, sidewalks):
    crs = sidewalks.crs
    validators.standardize_layer(sidewalks)
    ixn_dat = []
    st_crossings = []
    for i, (ixn, data) in enumerate(intersections_dict.items()):
        ixn_dat.append({'geometry': data['geometry'], 
         'ixn': i})
        for street in data['streets']:
            street['layer'] = validators.transform_layer(street['layer'])
            new_crossing = make_crossing(street, sidewalks, data['streets'])
            if new_crossing is not None:
                st_crossings.append(new_crossing)

    if not st_crossings:
        return
    st_crossings = gpd.GeoDataFrame(st_crossings)
    st_crossings = st_crossings[(st_crossings.type == 'LineString')]
    st_crossings = st_crossings[st_crossings.is_valid]

    def comp(geom):
        p1 = np.round(geom.coords[0], 2)
        p2 = np.round(geom.coords[(-1)], 2)
        return str([p1, p2])

    comparison = st_crossings.geometry.apply(comp)
    comparison.name = 'comp'
    unique = st_crossings.groupby(comparison).first()
    st_crossings = gpd.GeoDataFrame(unique.reset_index())
    st_crossings.crs = crs
    return st_crossings


def make_crossing(street, sidewalks, streets_list):
    """Attempts to create a street crossing line given a street segment and
    a GeoDataFrame sidewalks dataset. The street and sidewalks should have
    these properties:

    (1) The street should start at the street intersection and extend away
    from it.
    (2) The sidewalks should all be LineString geometries.

    If a crossing cannot be created that meets certain internal parameters,
    None is returned.

    :param street: The street geometry.
    :type street: shapely.geometry.LineString
    :param sidewalks: The sidewalks dataset.
    :type sidewalks: geopandas.GeoDataFrame
    :returns: If a crossing can be made, a shapely Linestring. Otherwise, None.
    :rtype: shapely.geometry.LineString or None

    """
    START_DIST = 4
    INCREMENT = 2
    MAX_DIST_ALONG = 25
    MAX_CROSSING_DIST = 30
    OFFSET = MAX_CROSSING_DIST / 2
    st_distance = min(street['geometry'].length / 2, MAX_DIST_ALONG)
    start_dist = min(START_DIST, st_distance / 2)
    layer = street['layer']
    sw_left = get_side_sidewalks(OFFSET, 'left', street, sidewalks)
    sw_right = get_side_sidewalks(OFFSET, 'right', street, sidewalks)
    if sw_left.empty or sw_right.empty:
        return
    sw_left = sw_left[(sw_left['layer'] == layer)]
    sw_right = sw_right[(sw_right['layer'] == layer)]
    if sw_left.empty or sw_right.empty:
        return
    crossings = []
    for dist in np.arange(start_dist, st_distance, INCREMENT):
        st_geom = street['geometry']
        point = st_geom.interpolate(dist)
        crossing1, left1, right1 = crossing_from_point(point, sw_left, sw_right)
        crossing2, left2, right2 = crossing_from_point(point, sw_right, sw_left)
        crossings.append({'geometry': crossing1, 
         'sw_left': left1, 
         'sw_right': right1})
        crossings.append({'geometry': crossing2, 
         'sw_left': left2, 
         'sw_right': right2})

    candidates = []
    for crossing in crossings:
        geometry_cr = crossing['geometry']
        geometry_st = street['geometry']
        if not geometry_cr.intersects(geometry_st):
            pass
        else:
            if geometry_cr.length > MAX_CROSSING_DIST:
                pass
            else:
                other_streets = []
                for st in streets_list:
                    if st == street:
                        pass
                    else:
                        if st['layer'] != layer:
                            pass
                        else:
                            other_streets.append(st['geometry'])

                if other_streets and crosses_other_streets(geometry_cr, other_streets):
                    pass
                else:
                    ixn = geometry_st.intersection(geometry_cr)
                    if ixn.type != 'Point':
                        pass
                    else:
                        crossing_distance = geometry_st.project(ixn)
                        crossing['search_distance'] = dist
                        crossing['crossing_distance'] = crossing_distance
                        st_seg = segment_at_distance(geometry_st, dist)
                        crossing['dotproduct'] = dotproduct(geometry_cr, st_seg)
                        crossing['layer'] = layer
                        candidates.append(crossing)

    if not candidates:
        return

    def cost(candidate):
        terms = []
        terms.append(candidate['geometry'].length)
        terms.append(0.2 * candidate['crossing_distance'])
        terms.append(500.0 * abs(candidate['dotproduct']))
        return sum(terms)

    best = sorted(candidates, key=cost)[0]
    return best


def get_side_sidewalks(offset, side, street, sidewalks):
    offset = street['geometry'].parallel_offset(offset, side, 0, 1, 1)
    if offset.type == 'MultiLineString':
        coords = []
        for geom in offset.geoms:
            coords += list(geom.coords)

        offset = LineString(coords)
    if side == 'left':
        offset.coords = offset.coords[::-1]
    st_buffer = Polygon(list(street['geometry'].coords) + list(offset.coords) + [
     street['geometry'].coords[0]])
    query = sidewalks.sindex.intersection(st_buffer.bounds, objects=True)
    query_sidewalks = sidewalks.loc[[q.object for q in query]]
    side_sidewalks = query_sidewalks[query_sidewalks.intersects(st_buffer)]
    return side_sidewalks


def crossing_from_point(point, sidewalks1, sidewalks2):
    idx1 = sidewalks1.distance(point).sort_values().index[0]
    geometry1 = sidewalks1.loc[(idx1, 'geometry')]
    point1 = geometry1.interpolate(geometry1.project(point))
    idx2 = sidewalks2.distance(point1).sort_values().index[0]
    geometry2 = sidewalks2.loc[(idx2, 'geometry')]
    point2 = geometry2.interpolate(geometry2.project(point))
    crossing = LineString([point1, point2])
    return (
     crossing, idx1, idx2)


def crosses_other_streets(crossing, other_streets):
    for street in other_streets:
        if street.intersects(crossing):
            return True

    return False


def cut(line, distance):
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
             LineString(coords[:i + 1]),
             LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
             LineString(coords[:i] + [(cp.x, cp.y)]),
             LineString([(cp.x, cp.y)] + coords[i:])]


def segment_at_distance(line, distance):
    if distance <= 0.0 or distance >= line.length:
        raise ValueError('Distance < 0 or longer than LineString')
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance or pd > distance:
            return LineString(coords[i - 1:i + 1])


def dotproduct(segment1, segment2):

    def unit_vector(segment):
        coords = np.array(segment.coords)
        vector = coords[1] - coords[0]
        unit_vector = vector / segment.length
        return unit_vector

    vector1 = unit_vector(segment1)
    vector2 = unit_vector(segment2)
    return vector1.dot(vector2)