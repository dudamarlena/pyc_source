# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/symath/graph/generation.py
# Compiled at: 2015-08-21 11:58:24
import directed, random

def random_graph(nodecount, edgeprobability, directedEdges=True):
    """
  Generate a random graph

  currently directedEdges must be True
  """
    assert directedEdges == True
    rv = directed.DirectedGraph()
    for i in range(nodecount):
        rv.add_node(i)
        for j in range(nodecount):
            if random.random() <= edgeprobability:
                rv.connect(i, j)

    return rv