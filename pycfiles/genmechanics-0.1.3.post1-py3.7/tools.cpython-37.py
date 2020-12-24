# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genmechanics/tools.py
# Compiled at: 2020-03-26 14:17:33
# Size of source mod 2**32: 5141 bytes
"""
Created on Sun Dec  4 20:13:02 2016

@author: steven
"""
import networkx as nx

def EquationsSystemAnalysis(Mo, vars_to_solve, overconstrain_stop=True):
    """
        Analyse a free equations system given by its ocurence matrix.
        :return: False (if system is unsolvable) if overconstrain_stop==True
        else, returns True, the solvable variables and the resolution order
    """
    if vars_to_solve == None:
        vars_to_solve = range(Mo.shape[1])
    neq, nvar = Mo.shape
    G = nx.Graph()
    Gp = nx.DiGraph()
    pos = {}
    for i in range(nvar):
        G.add_node(('v' + str(i)), bipartite=0)
        Gp.add_node(('v' + str(i)), bipartite=0)
        pos['v' + str(i)] = [i, 0]

    for i in range(neq):
        G.add_node(('e' + str(i)), bipartite=1)
        Gp.add_node(('e' + str(i)), bipartite=1)
        pos['e' + str(i)] = [i, 1]
        for j in range(nvar):
            if Mo[(i, j)] == 1:
                G.add_edge('e' + str(i), 'v' + str(j))
                Gp.add_edge('e' + str(i), 'v' + str(j))

    for Gi in (G.subgraph(c).copy() for c in nx.connected_components(G)):
        M = nx.bipartite.maximum_matching(Gi)
        for n1, n2 in M.items():
            Gp.add_edge(n1, n2)

    sinks = []
    sources = []
    for node in Gp.nodes():
        if Gp.out_degree(node) == 0:
            sinks.append(node)

    G2 = sources[:]
    for node in sources:
        for node2 in nx.descendants(Gp, node):
            if node2 not in G2:
                G2.append(node2)

    if overconstrain_stop:
        if G2 != []:
            return (
             False, [], None)
    G3 = sinks[:]
    for node in sinks:
        for node2 in nx.ancestors(Gp, node):
            if node2 not in G3:
                G3.append(node2)

    solvable_vars = []
    for var in vars_to_solve:
        if 'v' + str(var) not in G2 + G3:
            solvable_vars.append(var)

    G1 = G.copy()
    G1.remove_nodes_from(G2 + G3)
    G1p = nx.DiGraph()
    G1p.add_nodes_from(G1.nodes())
    for e in G1.edges():
        if e[0][0] == 'v':
            G1p.add_edge(e[0], e[1])
        else:
            G1p.add_edge(e[1], e[0])

    for G1i in (G1.subgraph(c).copy() for c in nx.connected_components(G1)):
        M1 = nx.bipartite.maximum_matching(G1i)
        for n1, n2 in M1.items():
            if n1[0] == 'e':
                G1p.add_edge(n1, n2)
            else:
                G1p.add_edge(n2, n1)

    scc = list(nx.strongly_connected_components(G1p))
    if scc != []:
        C = nx.condensation(G1p, scc)
        isc_vars = []
        for isc, sc in enumerate(scc):
            for var in solvable_vars:
                if 'v' + str(var) in sc:
                    isc_vars.append(isc)
                    break

        ancetres_vars = isc_vars[:]
        for isc_var in isc_vars:
            for ancetre in nx.ancestors(C, isc_var):
                if ancetre not in ancetres_vars:
                    ancetres_vars.append(ancetre)

        ordre_sc = [sc for sc in nx.topological_sort(C) if sc in ancetres_vars]
        ordre_ev = []
        for isc in ordre_sc:
            evs = sorted(scc[isc])
            levs = int(len(evs) / 2)
            ordre_ev.append(([int(e[1:]) for e in evs[0:levs]], [int(v[1:]) for v in evs[levs:]]))

        return (
         True, solvable_vars, ordre_ev)
    return (False, [], None)