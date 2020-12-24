# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/rulz/lib/python3.7/site-packages/rulz/tests/test_dependencies.py
# Compiled at: 2019-05-04 09:26:18
# Size of source mod 2**32: 1635 bytes
from functools import partial
from rulz import get_graph, get_group, get_subgraphs, plugin, run_graph
plugin = partial(plugin, group=__name__)

@plugin()
def one():
    return 1


@plugin()
def two():
    return 2


@plugin()
def three():
    return 3


@plugin()
def four():
    return 3


@plugin(one, two)
def add(a, b):
    return a + b


@plugin(three, four)
def seven(a, b):
    return a + b


@plugin()
def boom():
    raise Exception('Boom!')


@plugin(one, [two, boom])
def at_least_one(a, b, c):
    return a + b


@plugin(one, [boom, two])
def at_least_one_again(a, b, c):
    return a + c


@plugin(one, two, optional=[add])
def six(a, b, c):
    return a + b + c


@plugin(one, two, optional=[boom])
def three_opt(a, b, c):
    return a + b


def test_requirements():
    results = run_graph(get_graph(add))
    assert results[add] == 3


def test_at_least_one():
    results = run_graph(get_graph(at_least_one))
    assert results[at_least_one] == 3
    assert boom not in results


def test_at_least_one_again():
    results = run_graph(get_graph(at_least_one_again))
    assert results[at_least_one_again] == 3
    assert boom not in results


def test_optional_good():
    results = run_graph(get_graph(six))
    assert results[six] == 6


def test_optional_opt():
    results = run_graph(get_graph(three_opt))
    assert results[three_opt] == 3


def test_exception():
    results = run_graph(get_graph(boom))
    assert boom not in results
    assert boom in results.exceptions


def test_get_subgraphs():
    graph = get_group(__name__)
    sub_graphs = list(get_subgraphs(graph))
    assert len(sub_graphs) == 2