# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/treetable/hierarchical_container_ordered_wrapper.py
# Compiled at: 2013-04-04 15:36:35
"""Helper for TreeTable."""
from muntjac.data.util.container_ordered_wrapper import ContainerOrderedWrapper
from muntjac.data.container import IHierarchical

class HierarchicalContainerOrderedWrapper(ContainerOrderedWrapper, IHierarchical):
    """Helper for TreeTable. Does the same thing as ContainerOrderedWrapper
    to fit into table but retains Hierarchical feature."""

    def __init__(self, toBeWrapped):
        super(HierarchicalContainerOrderedWrapper, self).__init__(toBeWrapped)
        self._hierarchical = toBeWrapped

    def areChildrenAllowed(self, itemId):
        return self._hierarchical.areChildrenAllowed(itemId)

    def getChildren(self, itemId):
        return self._hierarchical.getChildren(itemId)

    def getParent(self, itemId):
        return self._hierarchical.getParent(itemId)

    def hasChildren(self, itemId):
        return self._hierarchical.hasChildren(itemId)

    def isRoot(self, itemId):
        return self._hierarchical.isRoot(itemId)

    def rootItemIds(self):
        return self._hierarchical.rootItemIds()

    def setChildrenAllowed(self, itemId, areChildrenAllowed):
        return self._hierarchical.setChildrenAllowed(itemId, areChildrenAllowed)

    def setParent(self, itemId, newParentId):
        return self._hierarchical.setParent(itemId, newParentId)