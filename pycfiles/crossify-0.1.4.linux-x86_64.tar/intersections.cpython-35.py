# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nick/accessmap/projects/crossify/venv/lib/python3.5/site-packages/crossify/intersections.py
# Compiled at: 2017-12-11 11:40:22
# Size of source mod 2**32: 2120 bytes
import numpy as np
from shapely.geometry import LineString, Point

def group_intersections(G):
    intersections = [node for node, degree in G.degree if degree > 2]
    intersection_groups = {}
    for intersection_id in intersections:
        data = G.node[intersection_id]
        intersection = Point(data['x'], data['y'])
        incoming = set(G.predecessors(intersection_id))
        outgoing = set(G.successors(intersection_id))
        incoming = incoming.difference(outgoing)
        edges = []
        for node in incoming:
            edges.append(get_edge(G, node, intersection_id))

        for node in outgoing:
            edges.append(get_edge(G, intersection_id, node))

        edges_ordered = []
        for i, edge in enumerate(edges):
            copy = edge.copy()
            point = Point(*edge['geometry'].coords[(-1)])
            if point.distance(intersection) < 0.1:
                reversed_street = LineString(edge['geometry'].coords[::-1])
                copy['geometry'] = reversed_street
            edges_ordered.append(copy)

        intersection_groups[intersection_id] = {'geometry': intersection, 
         'streets': edges_ordered}

    return intersection_groups


def get_edge(G, from_node, to_node):
    edge = G[from_node][to_node][0]
    if 'geometry' not in edge:
        start = Point((G.nodes[from_node]['x'], G.nodes[from_node]['y']))
        end = Point((G.nodes[to_node]['x'], G.nodes[to_node]['y']))
        edge['geometry'] = LineString([start, end])
    if 'layer' in edge:
        if edge['layer'] is np.nan:
            edge['layer'] = 0
    else:
        edge['layer'] = 0
    return edge