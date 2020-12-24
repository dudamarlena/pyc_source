# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sewergraph\tests\net_resolution_test.py
# Compiled at: 2018-09-15 10:57:59
# Size of source mod 2**32: 1842 bytes
import networkx as nx, sewergraph as sg, os
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

def test_map_to_lower_res_graph():
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    G1.add_edges_from([(5, 4), (4, 3), (3, 2), (2, 1)])
    G2.add_edges_from([(5, 3), (3, 2), (2, 1)])
    map_01 = sg.map_to_lower_res_graph(G1, G2)
    agg_01 = sg.map_to_lower_res_graph(G1, G2, return_agg=True)
    assert map_01 == {4: 3}
    assert agg_01 == {3: {4}}
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    G1.add_edges_from([(5, 4), (4, 3), (7, 6), (6, 3), (3, 2), (2, 1)])
    G2.add_edges_from([(5, 3), (7, 3), (3, 2), (2, 1)])
    map_02 = sg.map_to_lower_res_graph(G1, G2)
    agg_02 = sg.map_to_lower_res_graph(G1, G2, return_agg=True)
    assert map_02 == {4:3,  6:3}
    assert agg_02 == {3: {4, 6}}
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    G1.add_edges_from([(5, 4), (4, 3), (3, 2), (2, 1)])
    G2.add_edges_from([(5, 1)])
    map_03 = sg.map_to_lower_res_graph(G1, G2)
    assert map_03 == {4:1,  3:1,  2:1}
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    G1.add_edges_from([(5, 4), (4, 3), (3, 2), (2, 1), ('a', 3)])
    G2.add_edges_from([(5, 1)])
    map_04 = sg.map_to_lower_res_graph(G1, G2)
    agg_04 = sg.map_to_lower_res_graph(G1, G2, return_agg=True)
    assert map_04 == {4:1,  3:1,  2:1,  'a':1}
    assert agg_04 == {1: {4, 3, 2, 'a'}}
    G1 = nx.DiGraph()
    G2 = nx.DiGraph()
    G1.add_edges_from([(5, 4), (4, 3), (3, 2), (2, 1), ('a', 3), ('x', 'y'), ('y', 5)])
    G2.add_edges_from([(5, 1)])
    map_04 = sg.map_to_lower_res_graph(G1, G2)
    agg_04 = sg.map_to_lower_res_graph(G1, G2, return_agg=True)
    assert map_04 == {4:1,  3:1,  2:1,  'a':1,  'x':5,  'y':5}
    assert agg_04 == {1:{4, 3, 2, 'a'},  5:{'x', 'y'}}