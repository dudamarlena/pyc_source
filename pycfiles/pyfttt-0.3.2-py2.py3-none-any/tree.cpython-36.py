# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/common/tree.py
# Compiled at: 2018-04-14 08:55:22
# Size of source mod 2**32: 1579 bytes
__doc__ = '\nTree data structure\n'
from pyFTS import *
from functools import reduce
import numpy as np

class FLRGTreeNode:
    """FLRGTreeNode"""

    def __init__(self, value):
        self.isRoot = False
        self.children = []
        self.value = value

    def appendChild(self, child):
        self.children.append(child)

    def getChildren(self):
        for child in self.children:
            yield child

    def paths(self, acc=[]):
        if len(self.children) == 0:
            yield [
             self.value] + acc
        for child in self.children:
            for leaf_path in child.paths([self.value] + acc):
                yield leaf_path

    def getStr(self, k):
        if self.isRoot:
            tmp = str(self.value)
        else:
            tmp = '\\' + '-' * k + str(self.value)
        for child in self.getChildren():
            tmp = tmp + '\n' + child.getStr(k + 1)

        return tmp

    def __str__(self):
        return self.getStr(0)


class FLRGTree:
    """FLRGTree"""

    def __init__(self):
        self.root = FLRGTreeNode(None)


def flat(dados):
    for inst in dados:
        if isinstance(inst, (list, tuple)):
            x = flat(inst)
            for k in x:
                yield k

        else:
            yield inst


def build_tree_without_order(node, lags, level):
    if level not in lags:
        return
    for s in lags[level]:
        node.appendChild(FLRGTreeNode(s))

    for child in node.getChildren():
        build_tree_without_order(child, lags, level + 1)