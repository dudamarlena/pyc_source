# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/metrics/maxDiameter/FindMaxDiam.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1880 bytes
import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved

class MaxDiamOfTree:
    __doc__ = '\n    Returns max diameter for each method.\n    This value is sum of Height of highest two subtree + 1\n    '

    def __init__(self):
        pass

    def value(self, filename: str):
        tree = JavalangImproved(filename)
        nodes = tree.tree_to_nodes()
        traversed = []
        for each_noda in nodes:
            if type(each_noda.node) == javalang.tree.MethodDeclaration:
                traversed.append(diameter(each_noda.node))

        return max(traversed)


def depthOfTree(node):
    """
    Utility function that will return the depth of the tree
    """
    maxdepth = 0
    node_arr = node if isinstance(node, list) else [node]
    for child in node_arr:
        if not hasattr(child, 'children'):
            return 0
        for each_child in child.children:
            maxdepth = max(maxdepth, depthOfTree(each_child))

    return maxdepth + 1


def diameter(root):
    """
    Function to calculate the diameter of the tree
    """
    max1 = 0
    max2 = 0
    root_arr = root if isinstance(root, list) else [root]
    for child in root_arr:
        if not hasattr(child, 'children'):
            return 0
        for each_child in child.children:
            h = depthOfTree(each_child)
            if h > max1:
                max2 = max1
                max1 = h
            else:
                if h > max2:
                    max2 = h

    maxChildDia = 0
    for child in root_arr:
        if not hasattr(child, 'children'):
            return 0
        for each_child in child.children:
            maxChildDia = max(maxChildDia, diameter(each_child))

    return max(maxChildDia, max1 + max2 + 1)