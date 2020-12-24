# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/Tree.py
# Compiled at: 2017-09-08 07:44:18
"""Represents a simple tree.

Created on 6 Mar 2014

@author: paulross
"""

class Tree(object):
    """Represents a simple tree of objects."""

    def __init__(self, obj):
        """Constructor, takes any object."""
        self._obj = obj
        self._children = []

    @property
    def obj(self):
        return self._obj

    @property
    def children(self):
        return self._children

    @property
    def youngestChild(self):
        """The latest child to be added, may raise IndexError if no children."""
        return self._children[(-1)]

    def __len__(self):
        return len(self._children)

    def __str__(self):
        return str(self.branches())

    def addChild(self, obj):
        self._children.append(Tree(obj))

    def branches(self):
        """Returns all the possible branches through the tree as a list of lists
        of self._obj."""
        return self._branches(None)

    def _branches(self, thisBranch):
        if thisBranch is None:
            thisBranch = []
        thisBranch.append(self._obj)
        myBranches = [thisBranch[:]]
        for aChild in self._children:
            myBranches.extend(aChild._branches(thisBranch))

        thisBranch.pop()
        return myBranches


class DuplexAdjacencyList(object):
    """Represents a set of parent/child relationships (and their inverse) as
    Adjacency Lists."""

    def __init__(self):
        self._mapPc = {}
        self._mapCp = {}

    def __str__(self):
        rList = [
         'Parent -> Children:']
        for p in sorted(self._mapPc.keys()):
            rList.append('%s -> %s' % (p, self._mapPc[p]))

        return ('\n').join(rList)

    def add(self, parent, child):
        self._add(self._mapPc, parent, child)
        self._add(self._mapCp, child, parent)

    def _add(self, theMap, k, v):
        try:
            theMap[k].append(v)
        except KeyError:
            theMap[k] = [
             v]

    @property
    def allParents(self):
        """Returns an unordered list of objects that have at least one child."""
        return self._mapPc.keys()

    @property
    def allChildren(self):
        """Returns an unordered list of objects that have at least one parent."""
        return self._mapCp.keys()

    def hasParent(self, parent):
        """Returns True if the given parent has any children."""
        return parent in self._mapPc

    def hasChild(self, child):
        """Returns True if the given child has any parents."""
        return child in self._mapCp

    def children(self, parent):
        """Returns all immediate children of a given parent."""
        return self._mapPc[parent][:]

    def parents(self, child):
        """Returns all immediate parents of a given child."""
        return self._mapCp[child][:]

    def treeParentChild(self, theObj):
        """Returns a Tree() object where the links are the relationships
        between parent and child.
        Cycles are not reproduced i.e. if a -> b and b -> c and c-> a then
        treeParentChild('a') returns ['a', 'b', 'c',]
        treeParentChild('b') returns ['b', 'c', 'a',]
        treeParentChild('c') returns ['c', 'a', 'c',]
        """
        if theObj not in self._mapPc:
            raise ValueError('"%s" not in Parent/Child map' % theObj)
        return self._treeFromEither(theObj, self._mapPc)

    def treeChildParent(self, theObj):
        """Returns a Tree() object where the links are the relationships
        between child and parent.
        Cycles are not reproduced i.e. if a -> b and b -> c and c-> a then
        treeChildParent('a') returns ['a', 'c', 'b',]
        treeChildParent('b') returns ['b', 'a', 'c',]
        treeChildParent('c') returns ['c', 'b', 'a',]
        """
        if theObj not in self._mapCp:
            raise ValueError('"%s" not in Child/Parent map' % theObj)
        return self._treeFromEither(theObj, self._mapCp)

    def _treeFromEither(self, theObj, theMap):
        assert theObj in theMap
        retTree = Tree(theObj)
        myStack = [theObj]
        self._treeFromMap(theMap, myStack, retTree)
        assert len(myStack) == 1 and myStack[0] == theObj
        return retTree

    def _treeFromMap(self, theMap, theStack, theTree):
        if theStack[(-1)] in theMap:
            for val in theMap[theStack[(-1)]]:
                if val not in theStack:
                    theStack.append(val)
                    theTree.addChild(val)
                    self._treeFromMap(theMap, theStack, theTree.youngestChild)
                    v = theStack.pop()
                    assert v == val