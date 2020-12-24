# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/dag_creation/sung.py
# Compiled at: 2019-01-19 15:13:11
# Size of source mod 2**32: 1222 bytes
from LSD.colors import GREY, BLACK

def construct_sung_graph(c):
    """Construct the sung graph. That is also a DAG.
    In this procedure the DFS tree is constructed indirectly."""
    r = c.successors(c.a)[0]
    c.set_color(r, GREY)
    stack = [(r, iter(c.successors(r)))]
    while stack:
        parent, children = stack[(-1)]
        try:
            child = next(children)
            if child == c.b:
                c.g.add_edge('{v}_2'.format(v=parent), c.b)
                c.g.remove_edge(parent, child)
            else:
                if c.has_no_color(child):
                    c.set_color(child, GREY)
                    stack.append((child, iter(c.successors(child))))
                    c.g.add_edge('{v}_2'.format(v=parent), '{v}_2'.format(v=child))
                else:
                    if c.get_color(child) == GREY:
                        c.g.remove_edge(parent, child)
                        c.g.add_edge(parent, '{v}_2'.format(v=child))
                    else:
                        c.g.add_edge('{v}_2'.format(v=parent), '{v}_2'.format(v=child))
        except StopIteration:
            c.set_color(parent, BLACK)
            stack.pop()

    for v in c:
        v2 = '{v}_2'.format(v=v)
        if c.g.out_degree(v2) == 0:
            c.connect2sink(v2)
            break