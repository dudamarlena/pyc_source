# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/stone-mason/package/src/stonemason/resolution.py
# Compiled at: 2017-09-12 17:54:05
# Size of source mod 2**32: 1723 bytes
"""Handle dependeny resolutions"""
import json

class Node:
    __doc__ = 'A simple class to represent a node in a graph'

    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)


def create_dependency_graph(filename, node_list):
    """ Return a dictionary of Node instances representing the Dependency Graph """
    meta_data = json.load(open(filename))
    default_template = meta_data['default']
    nodes = {n:Node(n) for n in node_list}
    if default_template not in nodes:
        nodes[default_template] = Node(default_template)
    for k, v in nodes.items():
        deps = meta_data['dependencies'].get(k, None)
        if deps:
            for d in deps:
                v.add_edge(nodes[d])

    return nodes


def resolve(node, resolved=None, seen=None):
    """Graph dependency resolution algorithm

    Parameters
    ----------
    node: Node
        The node instance for which dependencies should be resolved

    Referenes
    ---------

        Source code obtained form the following paper. 

    .. https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html

    """
    if resolved is None:
        resolved = []
    if seen is None:
        seen = []
    seen.append(node)
    for edge in node.edges:
        if edge not in resolved:
            if edge in seen:
                raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
            resolve(edge, resolved, seen)

    resolved.append(node)
    return resolved