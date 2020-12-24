# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/hierarchical_container.py
# Compiled at: 2013-04-04 15:36:37
"""A specialized container whose contents can be accessed like it was a
tree-like structure."""
from muntjac.util import OrderedSet
from muntjac.data.container import IContainer, IHierarchical
from muntjac.data.util.indexed_container import IndexedContainer

class HierarchicalContainer(IndexedContainer, IHierarchical, IContainer):
    """A specialized Container whose contents can be accessed like it was a
    tree-like structure.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    """

    def __init__(self):
        super(HierarchicalContainer, self).__init__()
        self._noChildrenAllowed = set()
        self._parent = dict()
        self._filteredParent = None
        self._children = dict()
        self._filteredChildren = None
        self._roots = list()
        self._filteredRoots = None
        self._includeParentsWhenFiltering = True
        self._contentChangedEventsDisabled = False
        self._contentsChangedEventPending = None
        self._filterOverride = None
        return

    def areChildrenAllowed(self, itemId):
        if itemId in self._noChildrenAllowed:
            return False
        return self.containsId(itemId)

    def getChildren(self, itemId):
        if self._filteredChildren is not None:
            c = self._filteredChildren.get(itemId)
        else:
            c = self._children.get(itemId)
        if c is None:
            return
        else:
            return list(c)

    def getParent(self, itemId):
        if self._filteredParent is not None:
            return self._filteredParent.get(itemId)
        else:
            return self._parent.get(itemId)

    def hasChildren(self, itemId):
        if self._filteredChildren is not None:
            return itemId in self._filteredChildren
        else:
            return itemId in self._children
            return

    def isRoot(self, itemId):
        if self._filteredRoots is not None:
            if itemId not in self._filteredRoots:
                return False
        elif itemId in self._parent:
            return False
        return self.containsId(itemId)

    def rootItemIds(self):
        if self._filteredRoots is not None:
            return list(self._filteredRoots)
        else:
            return list(self._roots)
            return

    def setChildrenAllowed(self, itemId, childrenAllowed):
        """Sets the given Item's capability to have children. If the Item
        identified with the itemId already has children and the
        areChildrenAllowed is false this method fails and C{False}
        is returned; the children must be first explicitly removed with
        L{setParent} or L{IContainer.removeItem}.

        @param itemId:
                   the ID of the Item in the container whose child capability
                   is to be set.
        @param childrenAllowed:
                   the boolean value specifying if the Item can have children
                   or not.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        if not self.containsId(itemId):
            return False
        if childrenAllowed:
            if itemId in self._noChildrenAllowed:
                self._noChildrenAllowed.remove(itemId)
        else:
            self._noChildrenAllowed.add(itemId)
        return True

    def setParent(self, itemId, newParentId):
        """Sets the parent of an Item. The new parent item must exist and be
        able to have children. (C{canHaveChildren(newParentId) == True}). It
        is also possible to detach a node from the hierarchy (and thus make
        it root) by setting the parent C{None}.

        @param itemId:
                   the ID of the item to be set as the child of the Item
                   identified with newParentId.
        @param newParentId:
                   the ID of the Item that's to be the new parent of the Item
                   identified with itemId.
        @return: C{True} if the operation succeeded, C{False} if not
        """
        if not self.containsId(itemId):
            return False
        else:
            oldParentId = self._parent.get(itemId)
            if newParentId is None and oldParentId is None or newParentId is not None and newParentId == oldParentId:
                return True
            if newParentId is None:
                l = self._children.get(oldParentId)
                if l is not None:
                    l.remove(itemId)
                    if len(l) == 0:
                        del self._children[oldParentId]
                self._roots.append(itemId)
                del self._parent[itemId]
                if self.hasFilters():
                    self.doFilterContainer(self.hasFilters())
                self.fireItemSetChange()
                return True
            if not self.containsId(newParentId) or newParentId in self._noChildrenAllowed:
                return False
            o = newParentId
            while o is not None and o != itemId:
                o = self._parent.get(o)

            if o is not None:
                return False
            self._parent[itemId] = newParentId
            pcl = self._children.get(newParentId)
            if pcl is None:
                pcl = list()
                self._children[newParentId] = pcl
            pcl.append(itemId)
            if oldParentId is None:
                self._roots.remove(itemId)
            else:
                l = self._children.get(oldParentId)
                if l is not None:
                    l.remove(itemId)
                    if len(l) == 0:
                        del self._children[oldParentId]
            if self.hasFilters():
                self.doFilterContainer(self.hasFilters())
            self.fireItemSetChange()
            return True

    def hasFilters(self):
        return self._filteredRoots is not None

    def moveAfterSibling(self, itemId, siblingId):
        """Moves a node (an Item) in the container immediately after a sibling
        node. The two nodes must have the same parent in the container.

        @param itemId:
                   the identifier of the moved node (Item)
        @param siblingId:
                   the identifier of the reference node (Item), after which the
                   other node will be located
        """
        parent2 = self.getParent(itemId)
        if parent2 is None:
            childrenList = self._roots
        else:
            childrenList = self._children.get(parent2)
        if siblingId is None:
            childrenList.remove(itemId)
            childrenList.insert(0, itemId)
        else:
            oldIndex = childrenList.index(itemId)
            indexOfSibling = childrenList.index(siblingId)
            if indexOfSibling != -1 and oldIndex != -1:
                if oldIndex > indexOfSibling:
                    newIndex = indexOfSibling + 1
                else:
                    newIndex = indexOfSibling
                del childrenList[oldIndex]
                childrenList.insert(newIndex, itemId)
            else:
                raise ValueError('Given identifiers do not have the same parent.')
        self.fireItemSetChange()
        return

    def addItem(self, itemId=None):
        if itemId is None:
            self.disableContentsChangeEvents()
            itemId = super(HierarchicalContainer, self).addItem()
            if itemId is None:
                return
            if itemId not in self._roots:
                self._roots.append(itemId)
                if self._filteredRoots is not None:
                    if self.passesFilters(itemId):
                        self._filteredRoots.append(itemId)
            self.enableAndFireContentsChangeEvents()
            return itemId
        else:
            self.disableContentsChangeEvents()
            item = super(HierarchicalContainer, self).addItem(itemId)
            if item is None:
                return
            self._roots.append(itemId)
            if self._filteredRoots is not None:
                if self.passesFilters(itemId):
                    self._filteredRoots.append(itemId)
            self.enableAndFireContentsChangeEvents()
            return item
            return

    def fireItemSetChange(self, event=None):
        if event is not None:
            if self.contentsChangeEventsOn():
                super(HierarchicalContainer, self).fireItemSetChange(event)
            else:
                self._contentsChangedEventPending = True
        else:
            super(HierarchicalContainer, self).fireItemSetChange()
        return

    def contentsChangeEventsOn(self):
        return not self._contentChangedEventsDisabled

    def disableContentsChangeEvents(self):
        self._contentChangedEventsDisabled = True

    def enableAndFireContentsChangeEvents(self):
        self._contentChangedEventsDisabled = False
        if self._contentsChangedEventPending:
            self.fireItemSetChange()
        self._contentsChangedEventPending = False

    def removeAllItems(self):
        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeAllItems()
        if success:
            del self._roots[:]
            self._parent.clear()
            self._children.clear()
            self._noChildrenAllowed.clear()
            if self._filteredRoots is not None:
                self._filteredRoots = None
            if self._filteredChildren is not None:
                self._filteredChildren = None
            if self._filteredParent is not None:
                self._filteredParent = None
        self.enableAndFireContentsChangeEvents()
        return success

    def removeItem(self, itemId):
        self.disableContentsChangeEvents()
        success = super(HierarchicalContainer, self).removeItem(itemId)
        if success:
            if itemId in self._roots:
                self._roots.remove(itemId)
                if self._filteredRoots is not None:
                    self._filteredRoots.remove(itemId)
            childNodeIds = self._children.pop(itemId, None)
            if childNodeIds is not None:
                if self._filteredChildren is not None:
                    del self._filteredChildren[itemId]
                for childId in childNodeIds:
                    self.setParent(childId, None)

            parentItemId = self._parent.get(itemId)
            if parentItemId is not None:
                c = self._children.get(parentItemId)
                if c is not None:
                    c.remove(itemId)
                    if len(c) == 0:
                        del self._children[parentItemId]
                    if self._filteredChildren is not None:
                        f = self._filteredChildren.get(parentItemId)
                        if f is not None:
                            f.remove(itemId)
                            if len(f) == 0:
                                del self._filteredChildren[parentItemId]
            if itemId in self._parent:
                del self._parent[itemId]
            if self._filteredParent is not None:
                del self._filteredParent[itemId]
            if itemId in self._noChildrenAllowed:
                self._noChildrenAllowed.remove(itemId)
        self.enableAndFireContentsChangeEvents()
        return success

    def removeItemRecursively(self, *args):
        """Removes the Item identified by given itemId and all its children
        from the given Container.

        @see: L{removeItem}
        @param args: tuple of the form
                - (itemId)
                  - the identifier of the Item to be removed
                - (container, itemId)
                  - the container where the item is to be removed
                  - the identifier of the Item to be removed
        @return: true if the operation succeeded
        """
        nargs = len(args)
        if nargs == 1:
            itemId, = args
            self.disableContentsChangeEvents()
            removeItemRecursively = self.removeItemRecursively(self, itemId)
            self.enableAndFireContentsChangeEvents()
            return removeItemRecursively
        else:
            if nargs == 2:
                container, itemId = args
                success = True
                children2 = container.getChildren(itemId)
                if children2 is not None:
                    arry = list(children2)
                    for i in range(len(arry)):
                        removeItemRecursively = self.removeItemRecursively(container, arry[i])
                        if not removeItemRecursively:
                            success = False

                if success:
                    success = container.removeItem(itemId)
                return success
            return

    def doSort(self):
        super(HierarchicalContainer, self).doSort()
        self._roots.sort(cmp=self.getItemSorter())
        for childList in self._children.values():
            childList.sort(cmp=self.getItemSorter())

    def isIncludeParentsWhenFiltering(self):
        """Used to control how filtering works. @see
        L{setIncludeParentsWhenFiltering} for more information.

        @return: true if all parents for items that match the filter are
                included when filtering, false if only the matching items
                are included
        """
        return self._includeParentsWhenFiltering

    def setIncludeParentsWhenFiltering(self, includeParentsWhenFiltering):
        """Controls how the filtering of the container works. Set this to true
        to make filtering include parents for all matched items in addition to
        the items themselves. Setting this to false causes the filtering to
        only include the matching items and make items with excluded parents
        into root items.

        @param includeParentsWhenFiltering:
                   true to include all parents for items that match the filter,
                   false to only include the matching items
        """
        self._includeParentsWhenFiltering = includeParentsWhenFiltering
        if self._filteredRoots is not None:
            self.doFilterContainer(True)
        return

    def doFilterContainer(self, hasFilters):
        if not hasFilters:
            self._filteredRoots = None
            self._filteredChildren = None
            self._filteredParent = None
            return super(HierarchicalContainer, self).doFilterContainer(hasFilters)
        else:
            self._filteredRoots = list()
            self._filteredChildren = dict()
            self._filteredParent = dict()
            if self._includeParentsWhenFiltering:
                includedItems = set()
                for rootId in self._roots:
                    if self.filterIncludingParents(rootId, includedItems):
                        self._filteredRoots.append(rootId)
                        self.addFilteredChildrenRecursively(rootId, includedItems)

                self._filterOverride = includedItems
                super(HierarchicalContainer, self).doFilterContainer(hasFilters)
                self._filterOverride = None
                return True
            super(HierarchicalContainer, self).doFilterContainer(hasFilters)
            filteredItemIds = OrderedSet(self.getItemIds())
            for itemId in filteredItemIds:
                itemParent = self._parent.get(itemId)
                if itemParent is None or itemParent not in filteredItemIds:
                    self._filteredRoots.append(itemId)
                else:
                    self.addFilteredChild(itemParent, itemId)

            return True
            return

    def addFilteredChild(self, parentItemId, childItemId):
        """Adds the given childItemId as a filteredChildren for the
        parentItemId and sets it filteredParent.
        """
        parentToChildrenList = self._filteredChildren.get(parentItemId)
        if parentToChildrenList is None:
            parentToChildrenList = list()
            self._filteredChildren[parentItemId] = parentToChildrenList
        self._filteredParent[childItemId] = parentItemId
        parentToChildrenList.append(childItemId)
        return

    def addFilteredChildrenRecursively(self, parentItemId, includedItems):
        """Recursively adds all items in the includedItems list to the
        filteredChildren map in the same order as they are in the children map.
        Starts from parentItemId and recurses down as long as child items that
        should be included are found.

        @param parentItemId:
                   The item id to start recurse from. Not added to a
                   filteredChildren list
        @param includedItems:
                   Set containing the item ids for the items that should be
                   included in the filteredChildren map
        """
        childList = self._children.get(parentItemId)
        if childList is None:
            return
        else:
            for childItemId in childList:
                if childItemId in includedItems:
                    self.addFilteredChild(parentItemId, childItemId)
                    self.addFilteredChildrenRecursively(childItemId, includedItems)

            return

    def filterIncludingParents(self, itemId, includedItems):
        """Scans the itemId and all its children for which items should be
        included when filtering. All items which passes the filters are
        included. Additionally all items that have a child node that should be
        included are also themselves included.

        @return: true if the itemId should be included in the filtered
                container.
        """
        toBeIncluded = self.passesFilters(itemId)
        childList = self._children.get(itemId)
        if childList is not None:
            for childItemId in self._children.get(itemId):
                toBeIncluded = toBeIncluded | self.filterIncludingParents(childItemId, includedItems)

        if toBeIncluded:
            includedItems.add(itemId)
        return toBeIncluded

    def passesFilters(self, itemId):
        if self._filterOverride is not None:
            return itemId in self._filterOverride
        else:
            return super(HierarchicalContainer, self).passesFilters(itemId)
            return