# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dragndrop/DragDropTreeSortingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Tree
from muntjac.ui.tree import TreeDragMode
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.dd.acceptcriteria.accept_all import AcceptAll
from muntjac.event.data_bound_transferable import DataBoundTransferable
from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import VerticalDropLocation

class DragDropTreeSortingExample(VerticalLayout):

    def __init__(self):
        super(DragDropTreeSortingExample, self).__init__()
        self.setSpacing(True)
        tree = Tree("Tree sortable using drag'n'drop")
        container = ExampleUtil.getHardwareContainer()
        tree.setContainerDataSource(container)
        tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        tree.setItemIconPropertyId(ExampleUtil.hw_PROPERTY_ICON)
        for itemId in tree.getItemIds():
            tree.setChildrenAllowed(itemId, True)

        for idd in tree.rootItemIds():
            tree.expandItemsRecursively(idd)

        tree.setDragMode(TreeDragMode.NODE)
        tree.setDropHandler(TreeSortDropHandler(tree, container))
        self.addComponent(tree)


class TreeSortDropHandler(IDropHandler):

    def __init__(self, tree, container):
        """Tree must use L{HierarchicalContainer}.

        @param tree
        """
        self._tree = tree

    def getAcceptCriterion(self):
        return AcceptAll.get()

    def drop(self, dropEvent):
        t = dropEvent.getTransferable()
        if t.getSourceComponent() != self._tree or not isinstance(t, DataBoundTransferable):
            return
        dropData = dropEvent.getTargetDetails()
        sourceItemId = t.getItemId()
        targetItemId = dropData.getItemIdOver()
        location = dropData.getDropLocation()
        self.moveNode(sourceItemId, targetItemId, location)

    def moveNode(self, sourceItemId, targetItemId, location):
        """Move a node within a tree onto, above or below another node
        depending on the drop location.

        @param sourceItemId
                   id of the item to move
        @param targetItemId
                   id of the item onto which the source node should be moved
        @param location
                   VerticalDropLocation indicating where the source node was
                   dropped relative to the target node
        """
        container = self._tree.getContainerDataSource()
        if location == VerticalDropLocation.MIDDLE:
            if container.setParent(sourceItemId, targetItemId) and container.hasChildren(targetItemId):
                container.moveAfterSibling(sourceItemId, None)
        elif location == VerticalDropLocation.TOP:
            parentId = container.getParent(targetItemId)
            if container.setParent(sourceItemId, parentId):
                container.moveAfterSibling(sourceItemId, targetItemId)
                container.moveAfterSibling(targetItemId, sourceItemId)
        elif location == VerticalDropLocation.BOTTOM:
            parentId = container.getParent(targetItemId)
            if container.setParent(sourceItemId, parentId):
                container.moveAfterSibling(sourceItemId, targetItemId)
        return