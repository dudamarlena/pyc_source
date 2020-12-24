# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/migrations/topological_sort.py
# Compiled at: 2019-02-14 00:35:17


def topological_sort_as_sets(dependency_graph):
    """Variation of Kahn's algorithm (1962) that returns sets.

    Takes a dependency graph as a dictionary of node => dependencies.

    Yields sets of items in topological order, where the first set contains
    all nodes without dependencies, and each following set contains all
    nodes that may depend on the nodes only in the previously yielded sets.
    """
    todo = dependency_graph.copy()
    while todo:
        current = {node for node, deps in todo.items() if len(deps) == 0 if len(deps) == 0}
        if not current:
            raise ValueError(('Cyclic dependency in graph: {}').format((', ').join(repr(x) for x in todo.items())))
        yield current
        todo = {node:dependencies - current for node, dependencies in todo.items() if node not in current}


def stable_topological_sort(l, dependency_graph):
    result = []
    for layer in topological_sort_as_sets(dependency_graph):
        for node in l:
            if node in layer:
                result.append(node)

    return result