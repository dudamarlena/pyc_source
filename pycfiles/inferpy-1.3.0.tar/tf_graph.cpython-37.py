# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/tf_graph.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 3229 bytes
from collections import defaultdict
import networkx as nx, tensorflow as tf

def _get_varname(op):
    op_name = op.name
    idx = op_name.find('/')
    if idx != -1:
        if '/Assign' not in op_name:
            return op_name[:idx]
    return op_name


def _children(op):
    return set((_get_varname(opc) for out in op.outputs for opc in out.consumers()))


def _clean_graph(G, varnames):
    g_nodes = list(G.nodes)
    for n in g_nodes:
        if n not in varnames:
            if '/Assign' in n:
                predecesors = list(G.predecessors(n))
                n_name = n[n.rfind('/')]
                assert len(predecesors) <= 2
                if len(predecesors) == 2:
                    if predecesors[0] == n_name:
                        G.add_edge(predecesors[1], predecesors[0])
                    else:
                        G.add_edge(predecesors[0], predecesors[1])
            else:
                for p in G.predecessors(n):
                    for s in G.successors(n):
                        G.add_edge(p, s)

            G.remove_node(n)

    return G


def get_graph(varnames):
    ops = tf.get_default_graph().get_operations()
    dependencies = defaultdict(set)
    for op in ops:
        if 'sample_shape' not in op.name:
            c = _children(op)
            op_name = _get_varname(op)
            c.discard(op_name)
            dependencies[op_name].update(c)

    G = nx.DiGraph(dependencies)
    _clean_graph(G, varnames)
    return G


def get_empty_graph():
    return nx.DiGraph()