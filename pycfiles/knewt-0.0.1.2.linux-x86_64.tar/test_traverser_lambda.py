# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sven/0/_sdks/python/sven-2.7/lib/python2.7/site-packages/knewt/test_traverser_lambda.py
# Compiled at: 2017-11-19 11:01:46
from krt import Graph, Traverser
import pytest

def test_cycles_expects_excpetion():
    g = Graph()
    g.add_path(['a', 'b', 'c', 'a'])
    t = Traverser()
    t.grouper_add('cycle', lambda n, e, contxt: (n, e))
    with pytest.raises(Exception):
        t.dfs(g)


def test_cycles_expects_excpetion():
    g = Graph()
    g.add_path(['a', 'b', 'c', 'a'])
    t = Traverser()
    t.grouper_add('cycle', lambda n, e, contxt: (n, e))
    t.dfs(g, ignore_cycles=True)


def test_context_path_assertion():
    g = Graph()
    g.add_path(['a', 'b', 'c'])
    g.add_path(['e', 'b', 'g'])
    select_e = lambda n, e, context: (n, e) if 'e' in context[Traverser.PATH] else (None, None)
    t = Traverser()
    t.grouper_add('path_contains', select_e)
    t.dfs(g)
    assert len(t.groups()['path_contains']) == 1
    assert 'path_contains' in t.groups()
    assert t.groups()['path_contains'][0].edges == set([('e', 'b'), ('b', 'g'), ('b', 'c')])


def test_dfs_all():
    g = Graph()
    g.add_path(['a', 'b', 'c'])
    select_all = lambda n, e, context: (
     n, e)
    t = Traverser()
    t.grouper_add('main', select_all)
    t.dfs(g)
    assert len(t.groups()['main']) > 0