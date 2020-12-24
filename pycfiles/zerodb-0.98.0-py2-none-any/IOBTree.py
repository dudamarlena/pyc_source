# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/trees/IOBTree.py
# Compiled at: 2015-12-09 01:37:29
from BTrees.Interfaces import IIntegerObjectBTreeModule as IBTreeInterface
import BTrees.IOBTree as TreeModule
from zope.interface import moduleProvides
max_internal_size = 1740
max_leaf_size = 870

class BTree(TreeModule.BTree):
    max_internal_size = max_internal_size
    max_leaf_size = max_leaf_size


class TreeSet(TreeModule.TreeSet):
    max_internal_size = max_internal_size
    max_leaf_size = max_leaf_size


Set = TreeModule.Set
Bucket = TreeModule.Bucket
difference = TreeModule.difference
union = TreeModule.union
intersection = TreeModule.intersection
multiunion = TreeModule.multiunion
moduleProvides(IBTreeInterface)