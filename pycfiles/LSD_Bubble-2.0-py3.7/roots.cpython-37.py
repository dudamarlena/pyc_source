# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/LSD/dag_creation/roots.py
# Compiled at: 2019-01-19 14:22:30
# Size of source mod 2**32: 499 bytes


def choose_root(c):
    """Choose a or a b'' as root. The root is connected with a"""
    if c.source_connected():
        pass
    else:
        for predecessor in c.predecessors(c.b):
            for successor in c.successors(predecessor):
                if successor != c.b:
                    c.connect2source(successor)


def choose_random_root(c):
    """Choose a arbitrary root.
    To be deterministic the minimum vertex identifier is used"""
    r = next(iter(c))
    c.connect2source(r)