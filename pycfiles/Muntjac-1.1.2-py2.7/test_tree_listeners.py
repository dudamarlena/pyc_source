# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/test_tree_listeners.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.tree import IExpandListener, ICollapseListener, Tree

class TestTreeListeners(TestCase, IExpandListener, ICollapseListener):

    def setUp(self):
        TestCase.setUp(self)
        self._expandCalled = 0
        self._collapseCalled = 0
        self._lastExpanded = 0
        self._lastCollapsed = 0

    def testExpandListener(self):
        tree = self.createTree(10, 20, False)
        tree.addListener(self, IExpandListener)
        rootIds = list(tree.rootItemIds())
        self.assertEquals(10, len(rootIds))
        self.assertEquals(10 + 200 + 10, len(tree))
        tree.expandItem(rootIds[0])
        self.assertEquals(1, self._expandCalled)
        self.assertEquals(rootIds[0], self._lastExpanded)
        self._expandCalled = 0
        tree.expandItemsRecursively(rootIds[1])
        self.assertEquals(2, self._expandCalled)
        c = list(tree.getChildren(rootIds[1]))
        self.assertEquals(c[4], self._lastExpanded)
        self._expandCalled = 0
        tree.expandItem(rootIds[0])
        self.assertEquals(0, self._expandCalled)

    def createTree(self, rootItems, children, expand):
        """Creates a tree with "rootItems" roots, each with "children"
        children, each with 1 child.
        """
        tree = Tree()
        for i in range(rootItems):
            rootId = 'root ' + str(i)
            tree.addItem(rootId)
            if expand:
                tree.expandItemsRecursively(rootId)
            else:
                tree.collapseItemsRecursively(rootId)
            for j in range(children):
                childId = 'child ' + str(i) + '/' + str(j)
                tree.addItem(childId)
                tree.setParent(childId, rootId)
                tree.setChildrenAllowed(childId, False)
                if j == 4:
                    tree.setChildrenAllowed(childId, True)
                    grandChildId = tree.addItem()
                    tree.setParent(grandChildId, childId)
                    tree.setChildrenAllowed(grandChildId, False)
                    if expand:
                        tree.expandItemsRecursively(childId)
                    else:
                        tree.collapseItemsRecursively(childId)

        return tree

    def testCollapseListener(self):
        tree = self.createTree(7, 15, True)
        tree.addListener(self, ICollapseListener)
        rootIds = list(tree.rootItemIds())
        self.assertEquals(7, len(rootIds))
        self.assertEquals(7 + 105 + 7, len(tree))
        tree.collapseItem(rootIds[0])
        self.assertEquals(1, self._collapseCalled)
        self.assertEquals(rootIds[0], self._lastCollapsed)
        self._collapseCalled = 0
        tree.collapseItemsRecursively(rootIds[1])
        self.assertEquals(2, self._collapseCalled)
        c = list(tree.getChildren(rootIds[1]))
        self.assertEquals(c[4], self._lastCollapsed)
        self._collapseCalled = 0
        tree.collapseItem(rootIds[0])
        self.assertEquals(0, self._collapseCalled)

    def nodeExpand(self, event):
        self._lastExpanded = event.getItemId()
        self._expandCalled += 1

    def nodeCollapse(self, event):
        self._lastCollapsed = event.getItemId()
        self._collapseCalled += 1