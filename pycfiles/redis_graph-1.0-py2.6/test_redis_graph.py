# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/test/test_redis_graph.py
# Compiled at: 2010-11-30 07:26:38
from redis_graph import *

def test_edges():
    add_edge(from_node='frodo', to_node='gandalf')
    assert has_edge(from_node='frodo', to_node='gandalf') == True
    assert has_edge(from_node='gandalf', to_node='frodo') == False
    assert list(neighbors('frodo')) == ['gandalf']
    assert len(neighbors('frodo')) == 1
    delete_edge(from_node='frodo', to_node='gandalf')
    assert has_edge(from_node='frodo', to_node='gandalf') == False
    assert len(neighbors('frodo')) == 0


def test_node_values():
    set_node_value('frodo', '1')
    assert get_node_value('frodo') == '1'


def test_edge_values():
    set_edge_value('frodo_baggins', '2')
    assert get_edge_value('frodo_baggins') == '2'


if __name__ == '__main__':
    test_edges()
    test_node_values()
    test_edge_values()