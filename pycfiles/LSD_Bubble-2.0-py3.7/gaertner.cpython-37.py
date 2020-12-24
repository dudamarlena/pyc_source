# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/detecter/gaertner.py
# Compiled at: 2019-01-31 04:58:01
# Size of source mod 2**32: 1268 bytes
"""The package to detect superbubbles in a DAG"""
from LSD.detecter.outvalues import out_child2, out_parent2

def dag_superbubble(g, order, reporter):
    """Detect all superbubbles in a DAG."""

    def report(i, o):
        reporter.rep(order[i:o + 1])

    stack = []
    out_parent_map = []

    def f(pos):
        return len(order) - pos - 1

    t = None
    for k in range(len(order) - 1, -1, -1):
        v = order[k]
        child = out_child2(v, g, order)
        if child == k + 1:
            stack.append(t)
            t = k + 1
        else:
            while t is not None and t < child:
                t2 = stack.pop()
                if t2 is not None:
                    out_parent_map[f(t2)] = min(out_parent_map[f(t)], out_parent_map[f(t2)])
                t = t2

        if t is not None:
            if out_parent_map[f(t)] == k:
                report(k, t)
                t2 = stack.pop()
                if t2 is not None:
                    out_parent_map[f(t2)] = min(out_parent_map[f(t)], out_parent_map[f(t2)])
                t = t2
            out_parent_map.append(out_parent2(v, g, order))
            if t is not None:
                out_parent_map[f(t)] = min(out_parent_map[f(t)], out_parent_map[f(k)])