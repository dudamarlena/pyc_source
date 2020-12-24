# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/models/graph.py
# Compiled at: 2016-11-04 17:46:31
# Size of source mod 2**32: 872 bytes
import re

class Edge:

    def __init__(self, edge_label):
        self.edge_label = edge_label


class Graph:
    __doc__ = ' Graph of tokens \n    '

    def __init__(self, graph_id, tokens):
        self.graph_id = graph_id
        self.tokens = tokens
        self.edges = []

    def add_an_edge():
        self.edges.append()