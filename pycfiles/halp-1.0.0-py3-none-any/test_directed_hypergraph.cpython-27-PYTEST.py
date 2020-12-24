# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\baven_000\Documents\GitHub\tmmurali\halp\build\lib\tests\test_directed_hypergraph.py
# Compiled at: 2014-10-22 00:44:38
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from os import remove
from halp.directed_hypergraph import DirectedHypergraph

def test_add_node():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    H = DirectedHypergraph()
    H.add_node(node_a)
    H.add_node(node_b, source=True)
    H.add_node(node_c, attrib_c)
    H.add_node(node_d, attrib_d, sink=False)
    @py_assert3 = H._node_attributes
    @py_assert1 = node_a in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_a]
    @py_assert3 = {}
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_b in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_b, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_b]['source']
    @py_assert2 = @py_assert0 is True
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, True)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_c in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_c, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_c) if 'node_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_c) else 'node_c', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_c]['alt_name']
    @py_assert3 = 1337
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_d in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_d, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_d]['label']
    @py_assert3 = 'black'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_d]['sink']
    @py_assert2 = @py_assert0 is False
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, False)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    H.add_nodes(node_a, common=False)
    @py_assert0 = H._node_attributes[node_a]['common']
    @py_assert2 = @py_assert0 is False
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py3)s', ), (@py_assert0, False)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    try:
        H.add_node(node_a, ['label', 'black'])
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except AttributeError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_add_nodes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': False}),
     (
      node_c, attrib_c), (node_d, attrib_d)]
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    @py_assert3 = H._node_attributes
    @py_assert1 = node_a in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}',), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_a]
    @py_assert2 = @py_assert0 == common_attrib
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py3)s',), (@py_assert0, common_attrib)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(common_attrib) if 'common_attrib' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(common_attrib) else 'common_attrib'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_b in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}',), (node_b, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_b]['source']
    @py_assert2 = @py_assert0 is False
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is',), (@py_assert2,), ('%(py1)s is %(py3)s',), (@py_assert0, False)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_c in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}',), (node_c, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_c) if 'node_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_c) else 'node_c', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_c]['alt_name']
    @py_assert3 = 1337
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_d in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}',), (node_d, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_d]['label']
    @py_assert3 = 'black'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._node_attributes[node_d]['sink']
    @py_assert2 = @py_assert0 is True
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is',), (@py_assert2,), ('%(py1)s is %(py3)s',), (@py_assert0, True)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    node_set = H.get_node_set()
    @py_assert3 = ['A', 'B', 'C', 'D']
    @py_assert5 = set(@py_assert3)
    @py_assert1 = node_set == @py_assert5
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}',), (node_set, @py_assert5)) % {'py0': @pytest_ar._saferepr(node_set) if 'node_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_set) else 'node_set', 'py2': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = len(node_set)
    @py_assert7 = len(node_list)
    @py_assert4 = @py_assert2 == @py_assert7
    if not @py_assert4:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py8)s\n{%(py8)s = %(py5)s(%(py6)s)\n}',), (@py_assert2, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(node_set) if 'node_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_set) else 'node_set', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py6': @pytest_ar._saferepr(node_list) if 'node_list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_list) else 'node_list'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert7 = None
    for node in H.node_iterator():
        @py_assert1 = node in node_set
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py2)s',), (node, node_set)) % {'py0': @pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node', 'py2': @pytest_ar._saferepr(node_set) if 'node_set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_set) else 'node_set'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    return


def test_add_hyperedge():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail = set([node_a, node_b])
    head = set([node_c, node_d])
    frozen_tail = frozenset(tail)
    frozen_head = frozenset(head)
    attrib = {'weight': 6, 'color': 'black'}
    H = DirectedHypergraph()
    H.add_node(node_a, label=1337)
    hyperedge_name = H.add_hyperedge(tail, head, attrib, weight=5)
    @py_assert2 = 'e1'
    @py_assert1 = hyperedge_name == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (hyperedge_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['tail']
    @py_assert2 = @py_assert0 == tail
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, tail)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail) if 'tail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail) else 'tail'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['head']
    @py_assert2 = @py_assert0 == head
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, head)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['weight']
    @py_assert3 = 5
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['color']
    @py_assert3 = 'black'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = H._successors[frozen_tail]
    @py_assert1 = frozen_head in @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (frozen_head, @py_assert2)) % {'py0': @pytest_ar._saferepr(frozen_head) if 'frozen_head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head) else 'frozen_head', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = H._successors[frozen_tail][frozen_head]
    @py_assert1 = hyperedge_name in @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (hyperedge_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = H._predecessors[frozen_head]
    @py_assert1 = frozen_tail in @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (frozen_tail, @py_assert2)) % {'py0': @pytest_ar._saferepr(frozen_tail) if 'frozen_tail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail) else 'frozen_tail', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = H._predecessors[frozen_head][frozen_tail]
    @py_assert1 = hyperedge_name in @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (hyperedge_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    for node in frozen_tail:
        @py_assert2 = H._forward_star[node]
        @py_assert1 = hyperedge_name in @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (hyperedge_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    for node in frozen_head:
        @py_assert2 = H._backward_star[node]
        @py_assert1 = hyperedge_name in @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py3)s', ), (hyperedge_name, @py_assert2)) % {'py0': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    new_attrib = {'weight': 10}
    H.add_hyperedge(tail, head, new_attrib)
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['weight']
    @py_assert3 = 10
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes[hyperedge_name]['color']
    @py_assert3 = 'black'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    try:
        H.add_hyperedge(set(), set())
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_hyperedge_attributes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail = set([node_a, node_b])
    head = set([node_c, node_d])
    frozen_tail = frozenset(tail)
    frozen_head = frozenset(head)
    attrib = {'weight': 6, 'color': 'black'}
    H = DirectedHypergraph()
    H.add_node(node_a, label=1337)
    hyperedge_name = H.add_hyperedge(tail, head, attrib, weight=5)
    @py_assert1 = H.get_hyperedge_attributes
    @py_assert4 = @py_assert1(hyperedge_name)
    @py_assert7 = {'tail': tail, 'head': head, 'weight': 5, 'color': 'black'}
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_attributes\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(hyperedge_name) if 'hyperedge_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_name) else 'hyperedge_name', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    try:
        H.get_hyperedge_attributes('e10')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_add_hyperedges():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    @py_assert0 = 'e1'
    @py_assert2 = @py_assert0 in hyperedge_names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, hyperedge_names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(hyperedge_names) if 'hyperedge_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_names) else 'hyperedge_names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'e2'
    @py_assert2 = @py_assert0 in hyperedge_names
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, hyperedge_names)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(hyperedge_names) if 'hyperedge_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_names) else 'hyperedge_names'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e1']['tail']
    @py_assert2 = @py_assert0 == tail1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py3)s',), (@py_assert0, tail1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail1) if 'tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail1) else 'tail1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e1']['head']
    @py_assert2 = @py_assert0 == head1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py3)s',), (@py_assert0, head1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head1) if 'head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head1) else 'head1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e1']['weight']
    @py_assert3 = 6
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes['e1']['color']
    @py_assert3 = 'black'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes['e1']['sink']
    @py_assert2 = @py_assert0 is False
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is',), (@py_assert2,), ('%(py1)s is %(py3)s',), (@py_assert0, False)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e2']['tail']
    @py_assert2 = @py_assert0 == tail2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py3)s',), (@py_assert0, tail2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail2) if 'tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail2) else 'tail2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e2']['head']
    @py_assert2 = @py_assert0 == head2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py3)s',), (@py_assert0, head2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head2) if 'head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head2) else 'head2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = H._hyperedge_attributes['e2']['weight']
    @py_assert3 = 1
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes['e2']['color']
    @py_assert3 = 'white'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = H._hyperedge_attributes['e2']['sink']
    @py_assert2 = @py_assert0 is False
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('is',), (@py_assert2,), ('%(py1)s is %(py3)s',), (@py_assert0, False)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = set(hyperedge_names)
    @py_assert6 = H.get_hyperedge_id_set
    @py_assert8 = @py_assert6()
    @py_assert4 = @py_assert2 == @py_assert8
    if not @py_assert4:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s.get_hyperedge_id_set\n}()\n}',), (@py_assert2, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py1': @pytest_ar._saferepr(hyperedge_names) if 'hyperedge_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_names) else 'hyperedge_names', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    for hyperedge_id in H.hyperedge_id_iterator():
        @py_assert1 = hyperedge_id in hyperedge_names
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in',), (@py_assert1,), ('%(py0)s in %(py2)s',), (hyperedge_id, hyperedge_names)) % {'py0': @pytest_ar._saferepr(hyperedge_id) if 'hyperedge_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_id) else 'hyperedge_id', 'py2': @pytest_ar._saferepr(hyperedge_names) if 'hyperedge_names' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hyperedge_names) else 'hyperedge_names'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    return


def test_remove_node():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H.remove_node(node_a)
    @py_assert3 = H._node_attributes
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._forward_star
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._forward_star\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._backward_star
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._backward_star\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'e2'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail1) if 'frozen_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail1) else 'frozen_tail1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head1) if 'frozen_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head1) else 'frozen_head1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head2 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head2, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head2) if 'frozen_head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head2) else 'frozen_head2', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail2 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail2, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail2) if 'frozen_tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail2) else 'frozen_tail2', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail3 in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail3) if 'frozen_tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail3) else 'frozen_tail3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head3 in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head3) if 'frozen_head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head3) else 'frozen_head3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    H.remove_node(node_e)
    @py_assert3 = H._node_attributes
    @py_assert1 = node_e not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_e, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_e) if 'node_e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_e) else 'node_e', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._forward_star
    @py_assert1 = node_e not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._forward_star\n}', ), (node_e, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_e) if 'node_e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_e) else 'node_e', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._backward_star
    @py_assert1 = node_e not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._backward_star\n}', ), (node_e, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_e) if 'node_e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_e) else 'node_e', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head3 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head3) if 'frozen_head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head3) else 'frozen_head3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail3 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail3) if 'frozen_tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail3) else 'frozen_tail3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    try:
        H.remove_node(node_a)
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_remove_nodes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    tail4 = set([node_c])
    head4 = set([node_e])
    frozen_tail4 = frozenset(tail4)
    frozen_head4 = frozenset(head4)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib),
     (
      tail2, head2),
     (
      tail3, head3),
     (
      tail4, head4)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H.remove_nodes([node_a, node_d])
    @py_assert3 = H._node_attributes
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._forward_star
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._forward_star\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._backward_star
    @py_assert1 = node_a not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._backward_star\n}', ), (node_a, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'e2'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail1) if 'frozen_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail1) else 'frozen_tail1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head1) if 'frozen_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head1) else 'frozen_head1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head2 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head2, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head2) if 'frozen_head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head2) else 'frozen_head2', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail2 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail2, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail2) if 'frozen_tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail2) else 'frozen_tail2', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._node_attributes
    @py_assert1 = node_d not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._node_attributes\n}', ), (node_d, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._forward_star
    @py_assert1 = node_d not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._forward_star\n}', ), (node_d, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._backward_star
    @py_assert1 = node_d not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._backward_star\n}', ), (node_d, @py_assert3)) % {'py0': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'e3'
    @py_assert3 = H._predecessors[frozen_head3]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert2 = H._predecessors[frozen_head3]
    @py_assert1 = frozen_tail3 not in @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py3)s', ), (frozen_tail3, @py_assert2)) % {'py0': @pytest_ar._saferepr(frozen_tail3) if 'frozen_tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail3) else 'frozen_tail3', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_remove_hyperedge():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H.remove_hyperedge('e1')
    @py_assert0 = 'e1'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail1) if 'frozen_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail1) else 'frozen_tail1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head1) if 'frozen_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head1) else 'frozen_head1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._forward_star[node_a]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._forward_star[node_b]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._backward_star[node_c]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._backward_star[node_d]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    try:
        H.remove_hyperedge('e1')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_remove_hyperedges():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H.remove_hyperedges(['e1', 'e3'])
    @py_assert0 = 'e1'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail1) if 'frozen_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail1) else 'frozen_tail1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head1 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head1, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head1) if 'frozen_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head1) else 'frozen_head1', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._forward_star[node_a]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._forward_star[node_b]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._backward_star[node_c]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e1'
    @py_assert3 = H._backward_star[node_d]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert4 = H._hyperedge_attributes
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s._hyperedge_attributes\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = H._successors
    @py_assert1 = frozen_tail3 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._successors\n}', ), (frozen_tail3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_tail3) if 'frozen_tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail3) else 'frozen_tail3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = H._predecessors
    @py_assert1 = frozen_head3 not in @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert1,), ('%(py0)s not in %(py4)s\n{%(py4)s = %(py2)s._predecessors\n}', ), (frozen_head3, @py_assert3)) % {'py0': @pytest_ar._saferepr(frozen_head3) if 'frozen_head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head3) else 'frozen_head3', 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert3 = H._forward_star[node_d]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'e3'
    @py_assert3 = H._backward_star[node_e]
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    return


def test_get_hyperedge_id():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    @py_assert1 = H.get_hyperedge_id
    @py_assert5 = @py_assert1(tail1, head1)
    @py_assert8 = 'e1'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_id\n}(%(py3)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(tail1) if 'tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail1) else 'tail1', 'py4': @pytest_ar._saferepr(head1) if 'head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head1) else 'head1', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = H.get_hyperedge_id
    @py_assert5 = @py_assert1(tail2, head2)
    @py_assert8 = 'e2'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_id\n}(%(py3)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(tail2) if 'tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail2) else 'tail2', 'py4': @pytest_ar._saferepr(head2) if 'head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head2) else 'head2', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert8 = None
    @py_assert1 = H.get_hyperedge_id
    @py_assert5 = @py_assert1(tail3, head3)
    @py_assert8 = 'e3'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_id\n}(%(py3)s, %(py4)s)\n} == %(py9)s',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(tail3) if 'tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail3) else 'tail3', 'py4': @pytest_ar._saferepr(head3) if 'head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head3) else 'head3', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert8 = None
    try:
        H.get_hyperedge_id(tail1, head2)
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_hyperedge_attribute():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    @py_assert1 = H.get_hyperedge_attribute
    @py_assert3 = 'e1'
    @py_assert5 = 'weight'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 6
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_attribute\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = H.get_hyperedge_attribute
    @py_assert3 = 'e1'
    @py_assert5 = 'color'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert10 = 'black'
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_attribute\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    @py_assert1 = H.get_hyperedge_attribute
    @py_assert3 = 'e1'
    @py_assert5 = 'sink'
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = @py_assert7 is False
    if not @py_assert9:
        @py_format11 = @pytest_ar._call_reprcompare(('is', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get_hyperedge_attribute\n}(%(py4)s, %(py6)s)\n} is %(py10)s', ), (@py_assert7, False)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    try:
        H.get_hyperedge_attribute('e5', 'weight')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    try:
        H.get_hyperedge_attribute('e1', 'source')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_hyperedge_tail():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    retrieved_tail1 = H.get_hyperedge_tail('e1')
    retrieved_tail2 = H.get_hyperedge_tail('e2')
    @py_assert1 = retrieved_tail1 == tail1
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (retrieved_tail1, tail1)) % {'py0': @pytest_ar._saferepr(retrieved_tail1) if 'retrieved_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved_tail1) else 'retrieved_tail1', 'py2': @pytest_ar._saferepr(tail1) if 'tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail1) else 'tail1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = retrieved_tail2 == tail2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (retrieved_tail2, tail2)) % {'py0': @pytest_ar._saferepr(retrieved_tail2) if 'retrieved_tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved_tail2) else 'retrieved_tail2', 'py2': @pytest_ar._saferepr(tail2) if 'tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail2) else 'tail2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_get_hyperedge_head():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    retrieved_head1 = H.get_hyperedge_head('e1')
    retrieved_head2 = H.get_hyperedge_head('e2')
    @py_assert1 = retrieved_head1 == head1
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (retrieved_head1, head1)) % {'py0': @pytest_ar._saferepr(retrieved_head1) if 'retrieved_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved_head1) else 'retrieved_head1', 'py2': @pytest_ar._saferepr(head1) if 'head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head1) else 'head1'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    @py_assert1 = retrieved_head2 == head2
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (retrieved_head2, head2)) % {'py0': @pytest_ar._saferepr(retrieved_head2) if 'retrieved_head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(retrieved_head2) else 'retrieved_head2', 'py2': @pytest_ar._saferepr(head2) if 'head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head2) else 'head2'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None
    return


def test_get_hyperedge_weight():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    weight_e1 = H.get_hyperedge_weight('e1')
    weight_e2 = H.get_hyperedge_weight('e2')
    @py_assert2 = 6
    @py_assert1 = weight_e1 == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (weight_e1, @py_assert2)) % {'py0': @pytest_ar._saferepr(weight_e1) if 'weight_e1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weight_e1) else 'weight_e1', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert2 = 1
    @py_assert1 = weight_e2 == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (weight_e2, @py_assert2)) % {'py0': @pytest_ar._saferepr(weight_e2) if 'weight_e2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(weight_e2) else 'weight_e2', 'py3': @pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    return


def test_get_node_attribute():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    @py_assert1 = H.get_node_attribute
    @py_assert4 = 'common'
    @py_assert6 = @py_assert1(node_a, @py_assert4)
    @py_assert8 = @py_assert6 is True
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attribute\n}(%(py3)s, %(py5)s)\n} is %(py9)s',), (@py_assert6, True)) % {'py9': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_node_attribute
    @py_assert4 = 'source'
    @py_assert6 = @py_assert1(node_a, @py_assert4)
    @py_assert8 = @py_assert6 is False
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attribute\n}(%(py3)s, %(py5)s)\n} is %(py9)s',), (@py_assert6, False)) % {'py9': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_node_attribute
    @py_assert4 = 'common'
    @py_assert6 = @py_assert1(node_b, @py_assert4)
    @py_assert8 = @py_assert6 is True
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attribute\n}(%(py3)s, %(py5)s)\n} is %(py9)s',), (@py_assert6, True)) % {'py9': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_node_attribute
    @py_assert4 = 'source'
    @py_assert6 = @py_assert1(node_b, @py_assert4)
    @py_assert8 = @py_assert6 is True
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('is',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attribute\n}(%(py3)s, %(py5)s)\n} is %(py9)s',), (@py_assert6, True)) % {'py9': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_node_attribute
    @py_assert4 = 'alt_name'
    @py_assert6 = @py_assert1(node_c, @py_assert4)
    @py_assert9 = 1337
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attribute\n}(%(py3)s, %(py5)s)\n} == %(py10)s',), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(node_c) if 'node_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_c) else 'node_c', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    try:
        H.get_node_attribute('D', 'common')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    try:
        H.get_node_attribute(node_a, 'alt_name')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_node_attributes():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    node_d = 'D'
    attrib_d = {'label': 'black', 'sink': True}
    H = DirectedHypergraph()
    H.add_node(node_a)
    H.add_node(node_b, source=True)
    H.add_node(node_c, attrib_c)
    H.add_node(node_d, attrib_d, sink=False)
    @py_assert1 = H.get_node_attributes
    @py_assert4 = @py_assert1(node_a)
    @py_assert7 = {}
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attributes\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = H.get_node_attributes
    @py_assert4 = @py_assert1(node_d)
    @py_assert7 = {'label': 'black', 'sink': False}
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_attributes\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None
    try:
        H.get_node_attributes('X')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_forward_star():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    hyperedges = [
     (
      tail1, head1), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges)
    @py_assert1 = H.get_forward_star
    @py_assert4 = @py_assert1(node_a)
    @py_assert8 = ['e1']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_forward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_forward_star
    @py_assert4 = @py_assert1(node_b)
    @py_assert8 = ['e1', 'e2']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_forward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_forward_star
    @py_assert4 = @py_assert1(node_c)
    @py_assert8 = ['e2']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_forward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_c) if 'node_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_c) else 'node_c', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_forward_star
    @py_assert4 = @py_assert1(node_d)
    @py_assert8 = ['e3']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_forward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_forward_star
    @py_assert4 = @py_assert1(node_e)
    @py_assert8 = set()
    @py_assert6 = @py_assert4 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_forward_star\n}(%(py3)s)\n} == %(py9)s\n{%(py9)s = %(py7)s()\n}',), (@py_assert4, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_e) if 'node_e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_e) else 'node_e', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    try:
        H.get_forward_star('F')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_backward_star():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    hyperedges = [
     (
      tail1, head1), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges)
    @py_assert1 = H.get_backward_star
    @py_assert4 = @py_assert1(node_a)
    @py_assert8 = ['e2']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_backward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_a) if 'node_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_a) else 'node_a', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_backward_star
    @py_assert4 = @py_assert1(node_b)
    @py_assert8 = set()
    @py_assert6 = @py_assert4 == @py_assert8
    if not @py_assert6:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_backward_star\n}(%(py3)s)\n} == %(py9)s\n{%(py9)s = %(py7)s()\n}',), (@py_assert4, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_b) if 'node_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_b) else 'node_b', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_backward_star
    @py_assert4 = @py_assert1(node_c)
    @py_assert8 = ['e1']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_backward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_c) if 'node_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_c) else 'node_c', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_backward_star
    @py_assert4 = @py_assert1(node_d)
    @py_assert8 = ['e1', 'e2']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_backward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_d) if 'node_d' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_d) else 'node_d', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    @py_assert1 = H.get_backward_star
    @py_assert4 = @py_assert1(node_e)
    @py_assert8 = ['e3']
    @py_assert10 = set(@py_assert8)
    @py_assert6 = @py_assert4 == @py_assert10
    if not @py_assert6:
        @py_format12 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_backward_star\n}(%(py3)s)\n} == %(py11)s\n{%(py11)s = %(py7)s(%(py9)s)\n}',), (@py_assert4, @py_assert10)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py11': @pytest_ar._saferepr(@py_assert10), 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(node_e) if 'node_e' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node_e) else 'node_e', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = None
    try:
        H.get_backward_star('F')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_get_successors():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    hyperedges = [
     (
      tail1, head1), (tail2, head2), (tail3, head3), (tail3, 'F')]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges)
    @py_assert0 = 'e1'
    @py_assert4 = H.get_successors
    @py_assert7 = @py_assert4(tail1)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_successors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(tail1) if 'tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail1) else 'tail1'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e2'
    @py_assert4 = H.get_successors
    @py_assert7 = @py_assert4(tail2)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_successors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(tail2) if 'tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail2) else 'tail2'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e3'
    @py_assert4 = H.get_successors
    @py_assert7 = @py_assert4(tail3)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_successors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(tail3) if 'tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail3) else 'tail3'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e4'
    @py_assert4 = H.get_successors
    @py_assert7 = @py_assert4(tail3)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_successors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(tail3) if 'tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail3) else 'tail3'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert1 = H.get_successors
    @py_assert3 = [node_a]
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = set()
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_successors\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s()\n}', ), (@py_assert5, @py_assert9)) % {'py8': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_get_predecessors():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    hyperedges = [
     (
      tail1, head1), (tail2, head2), (tail3, head3), (tail3, 'F')]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges)
    @py_assert0 = 'e1'
    @py_assert4 = H.get_predecessors
    @py_assert7 = @py_assert4(head1)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_predecessors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(head1) if 'head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head1) else 'head1'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e2'
    @py_assert4 = H.get_predecessors
    @py_assert7 = @py_assert4(head2)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_predecessors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(head2) if 'head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head2) else 'head2'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e3'
    @py_assert4 = H.get_predecessors
    @py_assert7 = @py_assert4(head3)
    @py_assert2 = @py_assert0 in @py_assert7
    if not @py_assert2:
        @py_format9 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py3)s.get_predecessors\n}(%(py6)s)\n}', ), (@py_assert0, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py6': @pytest_ar._saferepr(head3) if 'head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head3) else 'head3'}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert7 = None
    @py_assert0 = 'e4'
    @py_assert4 = H.get_predecessors
    @py_assert6 = 'F'
    @py_assert8 = @py_assert4(@py_assert6)
    @py_assert2 = @py_assert0 in @py_assert8
    if not @py_assert2:
        @py_format10 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py9)s\n{%(py9)s = %(py5)s\n{%(py5)s = %(py3)s.get_predecessors\n}(%(py7)s)\n}', ), (@py_assert0, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = H.get_predecessors
    @py_assert3 = [node_a]
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert9 = set()
    @py_assert7 = @py_assert5 == @py_assert9
    if not @py_assert7:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_predecessors\n}(%(py4)s)\n} == %(py10)s\n{%(py10)s = %(py8)s()\n}', ), (@py_assert5, @py_assert9)) % {'py8': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    return


def test_copy():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    new_H = H.copy()
    @py_assert1 = new_H._node_attributes
    @py_assert5 = H._node_attributes
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._node_attributes\n} == %(py6)s\n{%(py6)s = %(py4)s._node_attributes\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = new_H._hyperedge_attributes
    @py_assert5 = H._hyperedge_attributes
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._hyperedge_attributes\n} == %(py6)s\n{%(py6)s = %(py4)s._hyperedge_attributes\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = new_H._backward_star
    @py_assert5 = H._backward_star
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._backward_star\n} == %(py6)s\n{%(py6)s = %(py4)s._backward_star\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = new_H._forward_star
    @py_assert5 = H._forward_star
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._forward_star\n} == %(py6)s\n{%(py6)s = %(py4)s._forward_star\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = new_H._successors
    @py_assert5 = H._successors
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._successors\n} == %(py6)s\n{%(py6)s = %(py4)s._successors\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = new_H._predecessors
    @py_assert5 = H._predecessors
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._predecessors\n} == %(py6)s\n{%(py6)s = %(py4)s._predecessors\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_read_and_write():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H.write('test_directed_read_and_write.txt')
    new_H = DirectedHypergraph()
    new_H.read('test_directed_read_and_write.txt')
    @py_assert1 = H._node_attributes
    @py_assert3 = @py_assert1.keys
    @py_assert5 = @py_assert3()
    @py_assert9 = new_H._node_attributes
    @py_assert11 = @py_assert9.keys
    @py_assert13 = @py_assert11()
    @py_assert7 = @py_assert5 == @py_assert13
    if not @py_assert7:
        @py_format15 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s._node_attributes\n}.keys\n}()\n} == %(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s\n{%(py10)s = %(py8)s._node_attributes\n}.keys\n}()\n}', ), (@py_assert5, @py_assert13)) % {'py8': @pytest_ar._saferepr(new_H) if 'new_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_H) else 'new_H', 'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5), 'py12': @pytest_ar._saferepr(@py_assert11), 'py14': @pytest_ar._saferepr(@py_assert13), 'py10': @pytest_ar._saferepr(@py_assert9)}
        @py_format17 = 'assert %(py16)s' % {'py16': @py_format15}
        raise AssertionError(@pytest_ar._format_explanation(@py_format17))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = @py_assert13 = None
    for new_hyperedge_id in new_H.get_hyperedge_id_set():
        new_hyperedge_tail = new_H.get_hyperedge_tail(new_hyperedge_id)
        new_hyperedge_head = new_H.get_hyperedge_head(new_hyperedge_id)
        new_hyperedge_weight = new_H.get_hyperedge_weight(new_hyperedge_id)
        found_matching_hyperedge = False
        for hyperedge_id in H.get_hyperedge_id_set():
            hyperedge_tail = H.get_hyperedge_tail(hyperedge_id)
            hyperedge_head = H.get_hyperedge_head(hyperedge_id)
            hyperedge_weight = H.get_hyperedge_weight(hyperedge_id)
            if new_hyperedge_tail == hyperedge_tail and new_hyperedge_head == hyperedge_head and new_hyperedge_weight == hyperedge_weight:
                found_matching_hyperedge = True
                continue

        if not found_matching_hyperedge:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(found_matching_hyperedge) if 'found_matching_hyperedge' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(found_matching_hyperedge) else 'found_matching_hyperedge'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))

    remove('test_directed_read_and_write.txt')
    invalid_H = DirectedHypergraph()
    try:
        invalid_H.read('tests/data/invalid_directed_hypergraph.txt')
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except IOError:
        pass
    except BaseException as e:
        assert False, e

    return


def test_check_hyperedge_attributes_consistency():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H._check_consistency()
    new_H = H.copy()
    del new_H._hyperedge_attributes['e1']['weight']
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._hyperedge_attributes['e1']['tail'] = head1
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._hyperedge_attributes['e1']['head'] = tail1
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    del new_H._successors[frozen_tail1]
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    del new_H._predecessors[frozen_head1]
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._forward_star['A'].pop()
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._backward_star['C'].pop()
    try:
        new_H._check_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e


def test_check_node_attributes_consistency():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H._check_consistency()
    new_H = H.copy()
    new_H._node_attributes['E'] = {}
    try:
        new_H._check_node_attributes_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._node_attributes['E'] = {}
    new_H._forward_star['E'] = set()
    try:
        new_H._check_node_attributes_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._forward_star['A'].add('e10')
    try:
        new_H._check_node_attributes_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._backward_star['A'].add('e10')
    try:
        new_H._check_node_attributes_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e


def test_check_predecessor_successor_consistency():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H._check_consistency()
    new_H = H.copy()
    new_H._predecessors[frozenset(['X'])] = {}
    try:
        new_H._check_predecessor_successor_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._successors[frozenset(['X'])] = {}
    try:
        new_H._check_predecessor_successor_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_frozentail = frozenset('A')
    new_frozenhead = frozenset('C')
    new_H._successors[new_frozentail] = {}
    new_H._successors[new_frozentail][new_frozenhead] = 'e1'
    new_H._predecessors[new_frozenhead] = {}
    new_H._predecessors[new_frozenhead][new_frozentail] = 'e2'
    try:
        new_H._check_predecessor_successor_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e


def test_check_hyperedge_id_consistency():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H._check_consistency()
    new_H = H.copy()
    new_H._forward_star['X'] = set('e0')
    try:
        new_H._check_hyperedge_id_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._backward_star['X'] = set('e0')
    try:
        new_H._check_hyperedge_id_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._predecessors[frozen_head1][frozen_tail1] = 'e0'
    try:
        new_H._check_hyperedge_id_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._successors[frozen_tail1][frozen_head1] = 'e0'
    try:
        new_H._check_hyperedge_id_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e


def test_check_node_consistency():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    attrib_c = {'alt_name': 1337}
    common_attrib = {'common': True, 'source': False}
    node_list = [
     node_a, (node_b, {'source': True}), (node_c, attrib_c)]
    node_d = 'D'
    H = DirectedHypergraph()
    H.add_nodes(node_list, common_attrib)
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    attrib = {'weight': 6, 'color': 'black'}
    common_attrib = {'sink': False}
    hyperedges = [
     (
      tail1, head1, attrib), (tail2, head2)]
    hyperedge_names = H.add_hyperedges(hyperedges, common_attrib, color='white')
    H._check_consistency()
    new_H = H.copy()
    new_H._forward_star['X'] = {}
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._backward_star['X'] = {}
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H.add_hyperedge('X', 'Y')
    del new_H._node_attributes['X']
    del new_H._forward_star['X']
    del new_H._forward_star['Y']
    del new_H._backward_star['X']
    del new_H._backward_star['Y']
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H.add_hyperedge('X', 'Y')
    del new_H._node_attributes['Y']
    del new_H._forward_star['X']
    del new_H._forward_star['Y']
    del new_H._backward_star['X']
    del new_H._backward_star['Y']
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._predecessors[frozenset('X')] = {}
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e

    new_H = H.copy()
    new_H._successors[frozenset('X')] = {}
    new_H._predecessors[frozenset('X')] = {}
    try:
        new_H._check_node_consistency()
        if not False:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(False) if 'False' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(False) else 'False'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    except ValueError:
        pass
    except BaseException as e:
        assert False, e


def test_get_symmetric_image():
    node_a = 'A'
    node_b = 'B'
    node_c = 'C'
    node_d = 'D'
    node_e = 'E'
    tail1 = set([node_a, node_b])
    head1 = set([node_c, node_d])
    frozen_tail1 = frozenset(tail1)
    frozen_head1 = frozenset(head1)
    tail2 = set([node_b, node_c])
    head2 = set([node_d, node_a])
    frozen_tail2 = frozenset(tail2)
    frozen_head2 = frozenset(head2)
    tail3 = set([node_d])
    head3 = set([node_e])
    frozen_tail3 = frozenset(tail3)
    frozen_head3 = frozenset(head3)
    hyperedges = [
     (
      tail1, head1), (tail2, head2), (tail3, head3)]
    H = DirectedHypergraph()
    hyperedge_names = H.add_hyperedges(hyperedges)
    sym_H = H.get_symmetric_image()
    sym_H._check_consistency()
    @py_assert1 = sym_H._node_attributes
    @py_assert5 = H._node_attributes
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._node_attributes\n} == %(py6)s\n{%(py6)s = %(py4)s._node_attributes\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(sym_H) if 'sym_H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sym_H) else 'sym_H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = sym_H._hyperedge_attributes['e1']['tail']
    @py_assert2 = @py_assert0 == head1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, head1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head1) if 'head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head1) else 'head1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e1']['head']
    @py_assert2 = @py_assert0 == tail1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, tail1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail1) if 'tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail1) else 'tail1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e1']['__frozen_tail']
    @py_assert2 = @py_assert0 == frozen_head1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_head1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_head1) if 'frozen_head1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head1) else 'frozen_head1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e1']['__frozen_head']
    @py_assert2 = @py_assert0 == frozen_tail1
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_tail1)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_tail1) if 'frozen_tail1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail1) else 'frozen_tail1'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e2']['tail']
    @py_assert2 = @py_assert0 == head2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, head2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head2) if 'head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head2) else 'head2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e2']['head']
    @py_assert2 = @py_assert0 == tail2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, tail2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail2) if 'tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail2) else 'tail2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e2']['__frozen_tail']
    @py_assert2 = @py_assert0 == frozen_head2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_head2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_head2) if 'frozen_head2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head2) else 'frozen_head2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e2']['__frozen_head']
    @py_assert2 = @py_assert0 == frozen_tail2
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_tail2)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_tail2) if 'frozen_tail2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail2) else 'frozen_tail2'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e3']['tail']
    @py_assert2 = @py_assert0 == head3
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, head3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(head3) if 'head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head3) else 'head3'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e3']['head']
    @py_assert2 = @py_assert0 == tail3
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, tail3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tail3) if 'tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail3) else 'tail3'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e3']['__frozen_tail']
    @py_assert2 = @py_assert0 == frozen_head3
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_head3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_head3) if 'frozen_head3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_head3) else 'frozen_head3'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._hyperedge_attributes['e3']['__frozen_head']
    @py_assert2 = @py_assert0 == frozen_tail3
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, frozen_tail3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(frozen_tail3) if 'frozen_tail3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(frozen_tail3) else 'frozen_tail3'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = sym_H._forward_star[node_a]
    @py_assert4 = ['e2']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._forward_star[node_b]
    @py_assert4 = set()
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s()\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = sym_H._forward_star[node_c]
    @py_assert4 = ['e1']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._forward_star[node_d]
    @py_assert4 = ['e1', 'e2']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._forward_star[node_e]
    @py_assert4 = ['e3']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._backward_star[node_a]
    @py_assert4 = ['e1']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._backward_star[node_b]
    @py_assert4 = ['e1', 'e2']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._backward_star[node_c]
    @py_assert4 = ['e2']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._backward_star[node_d]
    @py_assert4 = ['e3']
    @py_assert6 = set(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = sym_H._backward_star[node_e]
    @py_assert4 = set()
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s()\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    return


def test_get_induced_subhypergraph():
    H = DirectedHypergraph()
    H.read('tests/data/basic_directed_hypergraph.txt')
    induce_on_nodes = H.get_node_set() - {'t'}
    induced_H = H.get_induced_subhypergraph(induce_on_nodes)
    induced_nodes = induced_H.get_node_set()
    @py_assert3 = H.get_node_set
    @py_assert5 = @py_assert3()
    @py_assert7 = {'t'}
    @py_assert9 = @py_assert5 - @py_assert7
    @py_assert1 = induced_nodes == @py_assert9
    if not @py_assert1:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == (%(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s.get_node_set\n}()\n} - %(py8)s)',), (induced_nodes, @py_assert9)) % {'py0': @pytest_ar._saferepr(induced_nodes) if 'induced_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(induced_nodes) else 'induced_nodes', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    hyperedges = [ (induced_H.get_hyperedge_tail(hyperedge_id), induced_H.get_hyperedge_head(hyperedge_id)) for hyperedge_id in induced_H.get_hyperedge_id_set()
                 ]
    for hyperedge in hyperedges:
        tail, head = hyperedge
        @py_assert2 = set(tail)
        @py_assert5 = @py_assert2 - induce_on_nodes
        @py_assert8 = set()
        @py_assert6 = @py_assert5 == @py_assert8
        if not @py_assert6:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('(%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} - %(py4)s) == %(py9)s\n{%(py9)s = %(py7)s()\n}',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py1': @pytest_ar._saferepr(tail) if 'tail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail) else 'tail', 'py3': @pytest_ar._saferepr(@py_assert2), 'py4': @pytest_ar._saferepr(induce_on_nodes) if 'induce_on_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(induce_on_nodes) else 'induce_on_nodes', 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert5 = @py_assert6 = @py_assert8 = None
        @py_assert2 = set(head)
        @py_assert5 = @py_assert2 - induce_on_nodes
        @py_assert8 = set()
        @py_assert6 = @py_assert5 == @py_assert8
        if not @py_assert6:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert6,), ('(%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} - %(py4)s) == %(py9)s\n{%(py9)s = %(py7)s()\n}',), (@py_assert5, @py_assert8)) % {'py9': @pytest_ar._saferepr(@py_assert8), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py1': @pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head', 'py3': @pytest_ar._saferepr(@py_assert2), 'py4': @pytest_ar._saferepr(induce_on_nodes) if 'induce_on_nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(induce_on_nodes) else 'induce_on_nodes', 'py7': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert2 = @py_assert5 = @py_assert6 = @py_assert8 = None
        @py_assert1 = H.has_hyperedge
        @py_assert5 = @py_assert1(tail, head)
        if not @py_assert5:
            @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.has_hyperedge\n}(%(py3)s, %(py4)s)\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py3': @pytest_ar._saferepr(tail) if 'tail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tail) else 'tail', 'py4': @pytest_ar._saferepr(head) if 'head' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(head) else 'head', 'py6': @pytest_ar._saferepr(@py_assert5)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert5 = None

    return


def test_is_B_hypergraph():
    H = DirectedHypergraph()
    H.read('tests/data/basic_directed_hypergraph.txt')
    @py_assert1 = H.is_B_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_B_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    @py_assert1 = H.is_B_hypergraph
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_B_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_B_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_B_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_B_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_B_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_is_F_hypergraph():
    H = DirectedHypergraph()
    H.read('tests/data/basic_directed_hypergraph.txt')
    @py_assert1 = H.is_F_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_F_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    @py_assert1 = H.is_F_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_F_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_F_hypergraph
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_F_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_F_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_F_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_is_BF_hypergraph():
    H = DirectedHypergraph()
    H.read('tests/data/basic_directed_hypergraph.txt')
    @py_assert1 = H.is_BF_hypergraph
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_BF_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    @py_assert1 = H.is_BF_hypergraph
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_BF_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_BF_hypergraph
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_BF_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    H = DirectedHypergraph()
    H.add_hyperedge(['a', 'b'], ['c'])
    H.add_hyperedge(['x'], ['y', 'z'])
    @py_assert1 = H.is_BF_hypergraph
    @py_assert3 = @py_assert1()
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_BF_hypergraph\n}()\n}' % {'py0': @pytest_ar._saferepr(H) if 'H' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(H) else 'H', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = @py_assert3 = None
    return