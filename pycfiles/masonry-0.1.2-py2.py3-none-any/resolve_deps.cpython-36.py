# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../package/src/stonemason/resolve_deps.py
# Compiled at: 2017-06-19 18:25:37
# Size of source mod 2**32: 1332 bytes
import json

class Node:
    __doc__ = 'A simple class to represent a node in a graph'

    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, node):
        self.edges.append(node)


def create_dep_graph(filename):
    meta_data = json.load(open(filename))
    default_template = meta_data['default']
    nodes = {}
    nodes[default_template] = Node(default_template)
    for p in meta_data['dependencies']:
        nodes[p] = Node(p)

    for k, v in nodes.items():
        deps = meta_data['dependencies'].get(k, None)
        if deps:
            for d in deps:
                v.add_edge(nodes[d])

    return nodes


def dep_resolve(node, resolved, seen):
    """Graph dependency resolution algorithm 
    
    Parameters
    ----------
    node: Node

    Referenes
    ---------

        Source code obtained form the following paper. 

    .. https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html
        
    """
    seen.append(node)
    for edge in node.edges:
        if edge not in resolved:
            if edge in seen:
                raise Exception('Circular reference detected: %s -&gt; %s' % (node.name, edge.name))
            dep_resolve(edge, resolved, seen)

    resolved.append(node)
    return resolved