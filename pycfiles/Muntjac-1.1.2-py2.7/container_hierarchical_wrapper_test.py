# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/data/util/container_hierarchical_wrapper_test.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.data.util.abstract_hierarchical_container_test import AbstractHierarchicalContainerTest
from muntjac.data.util.container_hierarchical_wrapper import ContainerHierarchicalWrapper
from muntjac.data.util.indexed_container import IndexedContainer

class TestContainerHierarchicalWrapper(AbstractHierarchicalContainerTest):

    def testBasicOperations(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testBasicContainerOperations(container)

    def testHierarchicalContainer(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testHierarchicalContainer(container)

    def testRemoveSubtree(self):
        container = ContainerHierarchicalWrapper(IndexedContainer())
        self._testRemoveHierarchicalWrapperSubtree(container)

    def _testRemoveHierarchicalWrapperSubtree(self, container):
        self.initializeHierarchicalContainer(container)
        container.removeItemRecursively('org')
        packages = 21
        expectedSize = len(self.sampleData) + packages - 1
        self.validateContainer(container, 'com', 'com.vaadin.util.SerializerHelper', 'com.vaadin.terminal.ApplicationResource', 'blah', True, expectedSize)
        rootIds = container.rootItemIds()
        self.assertEquals(1, len(rootIds))