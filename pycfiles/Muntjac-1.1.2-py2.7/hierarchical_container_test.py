# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/data/util/hierarchical_container_test.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.data.util.abstract_hierarchical_container_test import AbstractHierarchicalContainerTest
from muntjac.data.container import IFilter
from muntjac.data.util.hierarchical_container import HierarchicalContainer

class TestHierarchicalContainer(AbstractHierarchicalContainerTest):

    def testBasicOperations(self):
        self._testBasicContainerOperations(HierarchicalContainer())

    def testFiltering(self):
        self._testContainerFiltering(HierarchicalContainer())

    def testSorting(self):
        self._testContainerSorting(HierarchicalContainer())

    def testOrdered(self):
        self._testContainerOrdered(HierarchicalContainer())

    def testHierarchicalSorting(self):
        self._testHierarchicalSorting(HierarchicalContainer())

    def testSortingAndFiltering(self):
        self._testContainerSortingAndFiltering(HierarchicalContainer())

    def testRemovingItemsFromFilteredContainer(self):
        container = HierarchicalContainer()
        self.initializeHierarchicalContainer(container)
        container.setIncludeParentsWhenFiltering(True)
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'ab', False, False)
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com.vaadin.ui', p1)
        container.removeItem('com.vaadin.ui.TabSheet')
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertIsNone(p1, 'Parent should be null, is ' + str(p1))
        container.removeAllItems()
        p1 = container.getParent('com.vaadin.terminal.gwt.client.Focusable')
        self.assertIsNone(p1, 'Parent should be null, is ' + str(p1))

    def testParentWhenRemovingFilterFromContainer(self):
        container = HierarchicalContainer()
        self.initializeHierarchicalContainer(container)
        container.setIncludeParentsWhenFiltering(True)
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'ab', False, False)
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com.vaadin.ui', p1)
        p1 = container.getParent('com.vaadin.terminal.gwt.client.ui.VPopupCalendar')
        self.assertIsNone(p1)
        container.removeAllContainerFilters()
        p1 = container.getParent('com.vaadin.terminal.gwt.client.ui.VPopupCalendar')
        self.assertEquals('com.vaadin.terminal.gwt.client.ui', p1)

    def testChangeParentInFilteredContainer(self):
        container = HierarchicalContainer()
        self.initializeHierarchicalContainer(container)
        container.setIncludeParentsWhenFiltering(True)
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'Tab', False, False)
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com.vaadin.ui', p1)
        container.setParent('com.vaadin.ui.TabSheet', 'com.vaadin')
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com.vaadin', p1)
        container.setParent('com.vaadin.ui.TabSheet', 'com')
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com', p1)
        container.setParent('com.vaadin.ui.TabSheet', None)
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertIsNone(p1)
        container.setParent('com.vaadin.ui.TabSheet', 'com')
        p1 = container.getParent('com.vaadin.ui.TabSheet')
        self.assertEquals('com', p1)
        return

    def testHierarchicalFilteringWithParents(self):
        container = HierarchicalContainer()
        self.initializeHierarchicalContainer(container)
        container.setIncludeParentsWhenFiltering(True)
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, 'ab', False, False)
        expectedSize = 29
        expectedRoots = 1
        self.validateHierarchicalContainer(container, 'com', 'com.vaadin.ui.TabSheet', 'com.vaadin.terminal.gwt.client.Focusable', 'blah', True, expectedSize, expectedRoots, True)
        container.removeAllContainerFilters()
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, '.gwt.client.', False, False)
        packages = 6
        classes = 112
        expectedSize = packages + classes
        expectedRoots = 1
        self.validateHierarchicalContainer(container, 'com', 'com.vaadin.terminal.gwt.client.WidgetSet', 'com.vaadin.terminal.gwt.client.ui.VSplitPanelVertical', 'blah', True, expectedSize, expectedRoots, True)
        container.addContainerFilter(self.SIMPLE_NAME, 'm', False, False)
        expectedSize = 25
        expectedRoots = 1
        self.validateHierarchicalContainer(container, 'com', 'com.vaadin.terminal.gwt.client.ui.VUriFragmentUtility', 'com.vaadin.terminal.gwt.client.ui.layout.ChildComponentContainer', 'blah', True, expectedSize, expectedRoots, True)

    def testRemoveLastChild(self):
        c = HierarchicalContainer()
        c.addItem('root')
        self.assertEquals(False, c.hasChildren('root'))
        c.addItem('child')
        c.setParent('child', 'root')
        self.assertEquals(True, c.hasChildren('root'))
        c.removeItem('child')
        self.assertFalse(c.containsId('child'))
        self.assertIsNone(c.getChildren('root'))
        self.assertIsNone(c.getChildren('child'))
        self.assertFalse(c.hasChildren('child'))
        self.assertFalse(c.hasChildren('root'))

    def testRemoveLastChildFromFiltered(self):
        c = HierarchicalContainer()
        c.addItem('root')
        self.assertEquals(False, c.hasChildren('root'))
        c.addItem('child')
        c.setParent('child', 'root')
        self.assertEquals(True, c.hasChildren('root'))

        class DummyFilter(IFilter):

            def passesFilter(self, itemId, item):
                return True

            def appliesToProperty(self, propertyId):
                return True

        c.addContainerFilter(DummyFilter())
        c.removeItem('child')
        self.assertFalse(c.containsId('child'))
        self.assertIsNone(c.getChildren('root'))
        self.assertIsNone(c.getChildren('child'))
        self.assertFalse(c.hasChildren('child'))
        self.assertFalse(c.hasChildren('root'))

    def testHierarchicalFilteringWithoutParents(self):
        container = HierarchicalContainer()
        self.initializeHierarchicalContainer(container)
        container.setIncludeParentsWhenFiltering(False)
        container.addContainerFilter(self.SIMPLE_NAME, 'ab', False, False)
        expectedSize = 20
        expectedRoots = 20
        self.validateHierarchicalContainer(container, 'com.vaadin.data.BufferedValidatable', 'com.vaadin.ui.TabSheet', 'com.vaadin.terminal.gwt.client.ui.VTabsheetBase', 'blah', True, expectedSize, expectedRoots, False)
        container.removeAllContainerFilters()
        container.addContainerFilter(self.FULLY_QUALIFIED_NAME, '.gwt.client.', False, False)
        packages = 3
        classes = 110
        expectedSize = packages + classes
        expectedRoots = 36
        self.validateHierarchicalContainer(container, 'com.vaadin.terminal.gwt.client.ApplicationConfiguration', 'com.vaadin.terminal.gwt.client.WidgetSet', 'com.vaadin.terminal.gwt.client.ui.VOptionGroup', 'blah', True, expectedSize, expectedRoots, False)
        container.addContainerFilter(self.SIMPLE_NAME, 'P', False, False)
        expectedSize = 13
        expectedRoots = expectedSize
        self.validateHierarchicalContainer(container, 'com.vaadin.terminal.gwt.client.Paintable', 'com.vaadin.terminal.gwt.client.ui.VTabsheetPanel', 'com.vaadin.terminal.gwt.client.ui.VPopupCalendar', 'blah', True, expectedSize, expectedRoots, False)