# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/compiler/cycle.py
# Compiled at: 2012-03-02 14:59:52
import logging
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.cycles import find_cycle
logger = logging.getLogger(__name__)

class CycleDetector(object):

    def __init__(self, nodes, edges):
        self.graph = digraph()
        self.graph.add_nodes(nodes)
        for edge in edges:
            logger.debug('      %s --> %s', edge[0], edge[1])
            self.graph.add_edge(edge)

    def detect_cycle(self):
        return find_cycle(self.graph)