# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/geomodel.py
# Compiled at: 2009-08-04 20:01:31
"""Defines the GeoModel class for running basic geospatial queries on
single-point geographic entities in Google App Engine.

TODO(romannurik): document how bounding box and proximity queries work.
"""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import copy, logging, math, sys
from google.appengine.ext import db
import geocell, geomath, geotypes, util
DEBUG = False

def default_cost_function(num_cells, resolution):
    """The default cost function, used if none is provided by the developer."""
    return float('inf') if num_cells > pow(geocell._GEOCELL_GRID_SIZE, 2) else 0


class GeoModel(db.Model):
    """A base model class for single-point geographically located entities.

  Attributes:
    location: A db.GeoPt that defines the single geographic point
        associated with this entity.
  """
    location = db.GeoPtProperty(required=True)
    location_geocells = db.StringListProperty()

    def update_location(self):
        """Syncs underlying geocell properties with the entity's location.

    Updates the underlying geocell properties of the entity to match the
    entity's location property. A put() must occur after this call to save
    the changes to App Engine."""
        max_res_geocell = geocell.compute(self.location)
        self.location_geocells = [ max_res_geocell[:res] for res in range(1, geocell.MAX_GEOCELL_RESOLUTION + 1)
                                 ]

    @staticmethod
    def bounding_box_fetch(query, bbox, max_results=1000, cost_function=None):
        """Performs a bounding box fetch on the given query.

    Fetches entities matching the given query with an additional filter
    matching only those entities that are inside of the given rectangular
    bounding box.

    Args:
      query: A db.Query on entities of this kind that should be additionally
          filtered by bounding box and subsequently fetched.
      bbox: A geotypes.Box indicating the bounding box to filter entities by.
      max_results: An optional int indicating the maximum number of desired
          results.
      cost_function: An optional function that accepts two arguments:
          * num_cells: the number of cells to search
          * resolution: the resolution of each cell to search
          and returns the 'cost' of querying against this number of cells
          at the given resolution.

    Returns:
      The fetched entities.

    Raises:
      Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
    """
        results = []
        if cost_function is None:
            cost_function = default_cost_function
        query_geocells = geocell.best_bbox_search_cells(bbox, cost_function)
        if query_geocells:
            if query._Query__orderings:
                cell_results = [ copy.deepcopy(query).filter('location_geocells =', search_cell).fetch(max_results) for search_cell in query_geocells
                               ]
                query_orderings = query._Query__orderings or []

                def _ordering_fn(ent1, ent2):
                    for (prop, direction) in query_orderings:
                        prop_cmp = cmp(getattr(ent1, prop), getattr(ent2, prop))
                        if prop_cmp != 0:
                            return prop_cmp if direction == 1 else -prop_cmp

                    return -1

                util.merge_in_place(cmp_fn=_ordering_fn, *cell_results)
                results = cell_results[0][:max_results]
            else:
                results = query.filter('location_geocells IN', query_geocells).fetch(1000)[:max_results]
        else:
            results = []
        if DEBUG:
            logging.info('bbox query looked in %d geocells' % len(query_geocells))
        return [ entity for entity in results if entity.location.lat >= bbox.south if entity.location.lat <= bbox.north if entity.location.lon >= bbox.west if entity.location.lon <= bbox.east
               ]

    @staticmethod
    def proximity_fetch(query, center, max_results=10, max_distance=0):
        """Performs a proximity/radius fetch on the given query.

    Fetches at most <max_results> entities matching the given query,
    ordered by ascending distance from the given center point, and optionally
    limited by the given maximum distance.

    This method uses a greedy algorithm that starts by searching high-resolution
    geocells near the center point and gradually looking in lower and lower
    resolution cells until max_results entities have been found matching the
    given query and no closer possible entities can be found.

    Args:
      query: A db.Query on entities of this kind.
      center: A geotypes.Point or db.GeoPt indicating the center point around
          which to search for matching entities.
      max_results: An int indicating the maximum number of desired results.
          The default is 10, and the larger this number, the longer the fetch
          will take.
      max_distance: An optional number indicating the maximum distance to
          search, in meters.

    Returns:
      The fetched entities, sorted in ascending order by distance to the search
      center.

    Raises:
      Any exceptions that google.appengine.ext.db.Query.fetch() can raise.
    """
        results = []
        searched_cells = set()
        cur_containing_geocell = geocell.compute(center)
        cur_geocells = [
         cur_containing_geocell]
        closest_possible_next_result_dist = 0

        def _merge_results_in_place(a, b):
            util.merge_in_place(a, b, cmp_fn=lambda x, y: cmp(x[1], y[1]), dup_fn=lambda x, y: x[0].key() == y[0].key())

        sorted_edges = [
         (0, 0)]
        sorted_edge_distances = [0]
        while cur_geocells:
            closest_possible_next_result_dist = sorted_edge_distances[0]
            if max_distance and closest_possible_next_result_dist > max_distance:
                break
            cur_geocells_unique = list(set(cur_geocells).difference(searched_cells))
            cur_resolution = len(cur_geocells[0])
            temp_query = copy.deepcopy(query)
            temp_query.filter('location_geocells IN', cur_geocells_unique)
            new_results = temp_query.fetch(1000)
            if DEBUG:
                logging.info('fetch complete for %s' % ((',').join(cur_geocells_unique),))
            searched_cells.update(cur_geocells)
            new_results = [ (entity, geomath.distance(center, entity.location)) for entity in new_results
                          ]
            new_results = sorted(new_results, lambda dr1, dr2: cmp(dr1[1], dr2[1]))
            new_results = new_results[:max_results]
            if len(results) > len(new_results):
                _merge_results_in_place(results, new_results)
            else:
                _merge_results_in_place(new_results, results)
                results = new_results
            results = results[:max_results]
            (sorted_edges, sorted_edge_distances) = util.distance_sorted_edges(cur_geocells, center)
            if len(results) == 0 or len(cur_geocells) == 4:
                cur_containing_geocell = cur_containing_geocell[:-1]
                cur_geocells = list(set([ cell[:-1] for cell in cur_geocells ]))
                if not cur_geocells or not cur_geocells[0]:
                    break
            elif len(cur_geocells) == 1:
                nearest_edge = sorted_edges[0]
                cur_geocells.append(geocell.adjacent(cur_geocells[0], nearest_edge))
            elif len(cur_geocells) == 2:
                nearest_edge = util.distance_sorted_edges([cur_containing_geocell], center)[0][0]
                if nearest_edge[0] == 0:
                    perpendicular_nearest_edge = [ x for x in sorted_edges if x[0] != 0 ][0]
                else:
                    perpendicular_nearest_edge = [ x for x in sorted_edges if x[0] == 0 ][0]
                cur_geocells.extend([ geocell.adjacent(cell, perpendicular_nearest_edge) for cell in cur_geocells
                                    ])
            if len(results) < max_results:
                if DEBUG:
                    logging.debug('have %d results but want %d results, continuing search' % (
                     len(results), max_results))
                continue
            if DEBUG:
                logging.debug('have %d results' % (len(results),))
            current_farthest_returnable_result_dist = geomath.distance(center, results[(max_results - 1)][0].location)
            if closest_possible_next_result_dist >= current_farthest_returnable_result_dist:
                if DEBUG:
                    logging.debug('DONE next result at least %f away, current farthest is %f dist' % (
                     closest_possible_next_result_dist,
                     current_farthest_returnable_result_dist))
                break
            if DEBUG:
                logging.debug('next result at least %f away, current farthest is %f dist' % (
                 closest_possible_next_result_dist,
                 current_farthest_returnable_result_dist))

        if DEBUG:
            logging.info('proximity query looked in %d geocells' % len(searched_cells))
        return [ entity for (entity, dist) in results[:max_results] if not max_distance or dist < max_distance
               ]