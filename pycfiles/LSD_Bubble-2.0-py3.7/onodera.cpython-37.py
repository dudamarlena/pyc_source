# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/detecter/onodera.py
# Compiled at: 2019-02-26 14:28:54
# Size of source mod 2**32: 874 bytes


def onodera(g, reporter):
    for s in g:
        dag = onodera_detect(s, g)
        if dag:
            reporter.rep(dag)


def onodera_detect(s, g):
    dag = []
    nextset = set()
    visited = set()
    seen = set()
    nextset.add(s)
    seen.add(s)
    while len(nextset):
        v = nextset.pop()
        seen.remove(v)
        visited.add(v)
        dag.append(v)
        if not g.out_degree(v):
            return
        for u in g.successors(v):
            if u == s:
                return
                seen.add(u)
                if parentsvisited(u, g, visited):
                    nextset.add(u)

        if len(nextset) == 1 and len(seen) == 1:
            t = nextset.pop()
            dag.append(t)
            return dag


def parentsvisited(u, g, visited):
    for w in g.predecessors(u):
        if w not in visited:
            return False

    return True