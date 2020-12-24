# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/BinPy/tests/tree_tests.py
# Compiled at: 2014-04-21 09:30:38
from __future__ import print_function
from BinPy.Gates.tree import *
from BinPy.Gates.gates import *
from BinPy.Gates.connector import *
from BinPy.Combinational.combinational import *
from nose.tools import with_setup, nottest

def getTreeForDepthTesting(depth):
    g1 = AND(True, False)
    g2 = AND(True, False)
    g3 = AND(g1, g2)
    g4 = AND(True, False)
    g5 = AND(True, False)
    g6 = AND(g4, g5)
    g_final = AND(g3, g6)
    tree_inst = Tree(g_final, depth)
    tree_inst.backtrack()
    n1 = (
     g1, [True, False])
    n2 = (g2, [True, False])
    n4 = (g4, [True, False])
    n5 = (g5, [True, False])
    n3 = (
     g3, [n1, n2])
    n6 = (g6, [n4, n5])
    tree_testing = (g_final, [n3, n6])
    return (
     tree_inst, tree_testing)


def compareTrees(tree_inst, tree_testing, depth):
    if isinstance(tree_testing, tuple):
        assert tree_testing[0] == tree_inst.element or False
    if depth == 0:
        if len(tree_inst.sons) != 0:
            if not False:
                raise AssertionError
        else:
            for i in range(len(tree_testing[1])):
                compareTrees(tree_inst.sons[i], tree_testing[1][i], depth - 1)

    elif not (tree_testing == tree_inst.element or False):
        raise AssertionError


def backtrack_depth_test():
    for i in range(6):
        tree_inst, tree_testing = getTreeForDepthTesting(i)
        compareTrees(tree_inst, tree_testing, i)


def set_depth_test():
    tree_inst, tree_testing = getTreeForDepthTesting(0)
    for i in range(1, 6):
        tree_inst.setDepth(i)
        tree_inst.backtrack()
        compareTrees(tree_inst, tree_testing, i)


def not_following_cycles_test():
    c1 = Connector(True)
    g1 = AND(c1, True)
    g2 = AND(g1, False)
    g2.setOutput(c1)
    t_no_cycle = Tree(g2, 5, False)
    t_cycle = Tree(g2, 5, True)
    t_no_cycle.backtrack()
    t_cycle.backtrack()
    assert t_no_cycle.sons[0].sons[0].sons[0].sons == []
    assert t_cycle.sons[0].sons[0].sons[0].sons[0].element == g1