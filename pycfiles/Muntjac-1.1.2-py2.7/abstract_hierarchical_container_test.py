# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/data/util/abstract_hierarchical_container_test.py
# Compiled at: 2013-04-04 15:36:37
import re
from muntjac.test.server.data.util.abstract_container_test import AbstractContainerTest

class AbstractHierarchicalContainerTest(AbstractContainerTest):

    def validateHierarchicalContainer(self, container, expectedFirstItemId, expectedLastItemId, itemIdInSet, itemIdNotInSet, checkGetItemNull, expectedSize, expectedRootSize, rootsHaveChildren):
        """@param container:
                   The container to validate
        @param expectedFirstItemId:
                   Expected first item id
        @param expectedLastItemId:
                   Expected last item id
        @param itemIdInSet:
                   An item id that is in the container
        @param itemIdNotInSet:
                   An item id that is not in the container
        @param checkGetItemNull:
                   true if getItem() should return null for itemIdNotInSet,
                   false to skip the check (container.containsId() is checked
                   in any case)
        @param expectedSize:
                   Expected number of items in the container. Not related to
                   hierarchy.
        @param expectedTraversalSize:
                   Expected number of items found when traversing from the
                   roots down to all available nodes.
        @param expectedRootSize:
                   Expected number of root items
        @param rootsHaveChildren:
                   true if all roots have children, false otherwise (skips
                   some asserts)
        """
        self.validateContainer(container, expectedFirstItemId, expectedLastItemId, itemIdInSet, itemIdNotInSet, checkGetItemNull, expectedSize)
        rootIds = container.rootItemIds()
        self.assertEquals(expectedRootSize, len(rootIds))
        for rootId in rootIds:
            self.assertTrue(container.containsId(rootId))
            self.assertEquals(container.getParent(rootId), None)
            self.assertTrue(container.isRoot(rootId))
            if rootsHaveChildren:
                self.assertTrue(container.areChildrenAllowed(rootId))
                children = container.getChildren(rootId)
                self.assertNotEquals(children, None, rootId + ' should have children')
                self.assertTrue(len(children) > 0, rootId + ' should have children')
                for childId in children:
                    self.assertEquals(container.getParent(childId), rootId)

        self.assertFalse(container.isRoot(itemIdNotInSet))
        self.assertFalse(container.hasChildren(itemIdNotInSet))
        self.assertFalse(container.areChildrenAllowed(itemIdNotInSet))
        self.assertFalse(container.removeItem(itemIdNotInSet))
        self.assertEquals(expectedSize, self.countNodes(container))
        self.validateHierarchy(container)
        return

    def countNodes(self, container, itemId=None):
        if itemId is None:
            totalNodes = 0
            for rootId in container.rootItemIds():
                totalNodes += self.countNodes(container, rootId)

            return totalNodes
        nodes = 1
        children = container.getChildren(itemId)
        if children is not None:
            for idd in children:
                nodes += self.countNodes(container, idd)

        return nodes
        return

    def validateHierarchy(self, container, itemId=None, parentId=None):
        if itemId is None and parentId is None:
            for rootId in container.rootItemIds():
                self.validateHierarchy(container, rootId, None)

        else:
            children = container.getChildren(itemId)
            self.assertEquals(container.getParent(itemId), parentId)
            if not container.areChildrenAllowed(itemId):
                self.assertFalse(container.hasChildren(itemId))
                self.assertTrue(children is None or len(children) == 0)
                return
        if children is not None:
            for idd in children:
                self.validateHierarchy(container, idd, itemId)

        return

    def _testHierarchicalContainer(self, container):
        self.initializeHierarchicalContainer(container)
        packages = 24
        expectedSize = len(self.sampleData) + packages
        self.validateHierarchicalContainer(container, 'com', 'org.vaadin.test.LastClass', 'com.vaadin.terminal.ApplicationResource', 'blah', True, expectedSize, 2, True)

    def _testHierarchicalSorting(self, container):
        sortable = container
        self.initializeHierarchicalContainer(container)
        self.assertTrue(self.FULLY_QUALIFIED_NAME in sortable.getSortableContainerPropertyIds())
        self.assertTrue(self.REVERSE_FULLY_QUALIFIED_NAME in sortable.getSortableContainerPropertyIds())
        sortable.sort([self.FULLY_QUALIFIED_NAME], [True])
        packages = 24
        expectedSize = len(self.sampleData) + packages
        self.validateHierarchicalContainer(container, 'com', 'org.vaadin.test.LastClass', 'com.vaadin.terminal.ApplicationResource', 'blah', True, expectedSize, 2, True)
        sortable.sort([self.REVERSE_FULLY_QUALIFIED_NAME], [True])
        self.validateHierarchicalContainer(container, 'com.vaadin.terminal.gwt.server.ApplicationPortlet2', 'com.vaadin.data.util.ObjectProperty', 'com.vaadin.terminal.ApplicationResource', 'blah', True, expectedSize, 2, True)

    def initializeHierarchicalContainer(self, container):
        container.removeAllItems()
        propertyIds = list(container.getContainerPropertyIds())
        for propertyId in propertyIds:
            container.removeContainerProperty(propertyId)

        container.addContainerProperty(self.FULLY_QUALIFIED_NAME, str, '')
        container.addContainerProperty(self.SIMPLE_NAME, str, '')
        container.addContainerProperty(self.REVERSE_FULLY_QUALIFIED_NAME, str, None)
        container.addContainerProperty(self.ID_NUMBER, int, None)
        for i in range(len(self.sampleData)):
            idd = self.sampleData[i]
            paths = re.split('\\.', idd)
            path = paths[0]
            if container.addItem(path) is not None:
                self.assertTrue(container.setChildrenAllowed(path, False))
                item = container.getItem(path)
                item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(path)
                item.getItemProperty(self.SIMPLE_NAME).setValue(self.getSimpleName(path))
                item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME).setValue(self.reverse(path))
                item.getItemProperty(self.ID_NUMBER).setValue(1)
            for j in range(1, len(paths)):
                parent = path
                path = path + '.' + paths[j]
                if container.addItem(path) is not None:
                    self.assertTrue(container.setChildrenAllowed(path, False))
                    item = container.getItem(path)
                    item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(path)
                    item.getItemProperty(self.SIMPLE_NAME).setValue(self.getSimpleName(path))
                    item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME).setValue(self.reverse(path))
                    item.getItemProperty(self.ID_NUMBER).setValue(1)
                self.assertTrue(container.setChildrenAllowed(parent, True))
                self.assertTrue(container.setParent(path, parent), 'Failed to set ' + parent + ' as parent for ' + path)

            item = container.getItem(idd)
            self.assertNotEquals(item, None)
            parent = idd[:idd.rfind('.')]
            self.assertTrue(container.setParent(idd, parent))
            item.getItemProperty(self.FULLY_QUALIFIED_NAME).setValue(self.sampleData[i])
            item.getItemProperty(self.SIMPLE_NAME).setValue(self.getSimpleName(self.sampleData[i]))
            item.getItemProperty(self.REVERSE_FULLY_QUALIFIED_NAME).setValue(self.reverse(self.sampleData[i]))
            item.getItemProperty(self.ID_NUMBER).setValue(i % 2)

        return