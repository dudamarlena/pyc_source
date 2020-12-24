# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/models/tree.py
# Compiled at: 2016-11-04 17:43:46
# Size of source mod 2**32: 1201 bytes


class Node:
    __doc__ = '\n        Node is a container of one or many tokens or nodes\n    '

    def __init__(self, children=[], label=''):
        self.children = children
        self.label = label

    def get_children():
        return self.children

    def get_label():
        return self.label

    def is_a_leaf():
        if self.children:
            return False
        return True


class Tree:
    __doc__ = ' to store a tree structure for tokens\n    '

    def __init__(self, tree_id, tokens, nodes=[]):
        self.tree_id = tree_id
        self.tokens = tokens
        self.nodes = []

    def add_a_node(self):
        pass