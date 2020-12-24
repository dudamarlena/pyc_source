# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/r/repo/aibolit/metrics/countLeaves/numberofleaves.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1219 bytes
import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List

class CountNumberOfLeaves:
    """CountNumberOfLeaves"""

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = JavalangImproved(filename)
        nodes = tree.tree_to_nodes()
        traversed = []
        for each_node in nodes:
            if type(each_node.node) == javalang.tree.MethodDeclaration:
                traversed.append(countLeaves(each_node.node.body))

        return sum(traversed)


def countLeaves(root):
    root_arr = root if isinstance(root, List) else [root]
    leaves = 0
    not_count = [None, '', set()]
    for node in root_arr:
        if not hasattr(node, 'children'):
            if node not in not_count:
                return leaves + 1
        if node in not_count:
            pass
        else:
            for each_child in node.children:
                leaves += countLeaves(each_child)

    return leaves