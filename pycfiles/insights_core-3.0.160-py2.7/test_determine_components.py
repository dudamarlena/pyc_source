# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_determine_components.py
# Compiled at: 2019-05-16 13:41:33
from insights import dr

class needs(dr.ComponentType):
    group = 'needs'


@needs()
def one():
    return 1


@needs()
def two():
    return 2


@needs(one, two)
def report(a, b):
    return a + b


def test_single_component():
    graph = dr.get_dependency_graph(report)
    components = dr._determine_components(report)
    assert graph == components


def test_list_of_components():
    graph = dr.get_dependency_graph(report)
    components = dr._determine_components([one, two, report])
    assert graph == components


def test_group():
    graph = dr.get_dependency_graph(report)
    components = dr._determine_components('needs')
    assert graph == components


def test_type():
    graph = dr.get_dependency_graph(report)
    components = dr._determine_components(needs)
    assert graph == components