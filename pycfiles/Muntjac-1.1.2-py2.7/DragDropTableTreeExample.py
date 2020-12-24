# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dragndrop/DragDropTableTreeExample.py
# Compiled at: 2013-04-04 15:36:38
import re
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import HorizontalLayout, Table, Tree
from muntjac.event.dd.acceptcriteria.source_is import SourceIs
from muntjac.ui.tree import TreeDragMode, TargetItemAllowsChildren
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.ui.window import Notification
from muntjac.event.dd.acceptcriteria.and_ import And
from muntjac.ui.abstract_select import AcceptItem
from muntjac.ui.table import TableDragMode
from muntjac.data import container

class DragDropTableTreeExample(HorizontalLayout):
    """Demonstrate moving data back and forth between a table and a tree using
    drag and drop.

    The tree and the table use different data structures: The category is a
    separate node in the tree and each item just has a String, whereas the
    table contains items with both a name and a category. Data conversions
    between these representations are made during drop processing.
    """

    def __init__(self):
        super(DragDropTableTreeExample, self).__init__()
        self.setSpacing(True)
        self._tree = Tree('Drag from tree to table')
        self._table = Table('Drag from table to tree')
        self._table.setWidth('100%')
        self.initializeTree(SourceIs(self._table))
        self.initializeTable(SourceIs(self._tree))
        self.addComponent(self._tree)
        self.addComponent(self._table)

    def initializeTree(self, acceptCriterion):
        self._tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        for idd in self._tree.rootItemIds():
            self._tree.expandItemsRecursively(idd)

        self._tree.setDragMode(TreeDragMode.NODE)
        self._tree.setDropHandler(TreeDropHandler(self))

    def initializeTable(self, acceptCriterion):
        tableContainer = BeanItemContainer(Hardware)
        tableContainer.addItem(Hardware('Dell OptiPlex 380', 'Desktops'))
        tableContainer.addItem(Hardware('Benq T900HD', 'Monitors'))
        tableContainer.addItem(Hardware('Lenovo ThinkPad T500', 'Laptops'))
        self._table.setContainerDataSource(tableContainer)
        self._table.setVisibleColumns(['category', 'name'])
        self._table.setDragMode(TableDragMode.ROW)
        self._table.setDropHandler(TableDropHandler(self))

    @classmethod
    def getTreeNodeName(cls, source, sourceId):
        return source.getItem(sourceId).getItemProperty(ExampleUtil.hw_PROPERTY_NAME).getValue()


class TreeDropHandler(IDropHandler):

    def __init__(self, c):
        self._c = c

    def drop(self, dropEvent):
        t = dropEvent.getTransferable()
        sourceContainer = t.getSourceContainer()
        sourceItemId = t.getItemId()
        sourceItem = sourceContainer.getItem(sourceItemId)
        name = str(sourceItem.getItemProperty('name'))
        category = str(sourceItem.getItemProperty('category'))
        dropData = dropEvent.getTargetDetails()
        targetItemId = dropData.getItemIdOver()
        if targetItemId is not None and name is not None and category is not None:
            treeCategory = self._c.getTreeNodeName(self._c._tree, targetItemId)
            if category == treeCategory:
                newItemId = self._c._tree.addItem()
                self._c._tree.getItem(newItemId).getItemProperty(ExampleUtil.hw_PROPERTY_NAME).setValue(name)
                self._c._tree.setParent(newItemId, targetItemId)
                self._c._tree.setChildrenAllowed(newItemId, False)
                sourceContainer.removeItem(sourceItemId)
            else:
                message = name + ' is not a ' + re.sub('s$', '', treeCategory.lower())
                self.getWindow().showNotification(message, Notification.TYPE_WARNING_MESSAGE)
        return

    def getAcceptCriterion(self):
        return And(self.acceptCriterion, TargetItemAllowsChildren.get(), AcceptItem.ALL)


class TableDropHandler(IDropHandler):

    def __init__(self, c):
        self._c = c

    def drop(self, dropEvent):
        t = dropEvent.getTransferable()
        if not isinstance(t.getSourceContainer(), container.IHierarchical):
            return
        else:
            source = t.getSourceContainer()
            sourceItemId = t.getItemId()
            parentItemId = source.getParent(sourceItemId)
            hardwareMap = dict()
            if parentItemId is None:
                category = self._c.getTreeNodeName(source, sourceItemId)
                children = source.getChildren(sourceItemId)
                if children is not None:
                    for childId in children:
                        name = self._c.getTreeNodeName(source, childId)
                        hardwareMap[childId] = Hardware(name, category)

            else:
                category = self._c.getTreeNodeName(source, parentItemId)
                name = self._c.getTreeNodeName(source, sourceItemId)
                hardwareMap[sourceItemId] = Hardware(name, category)
            dropData = dropEvent.getTargetDetails()
            targetItemId = dropData.getItemIdOver()
            for sourceId, hardware in hardwareMap.iteritems():
                if targetItemId is not None:
                    dl = dropData.getDropLocation()
                    if dl == self.BOTTOM:
                        self.tableContainer.addItemAfter(targetItemId, hardware)
                    if dl == self.MIDDLE or dl == self.TOP:
                        prevItemId = self.tableContainer.prevItemId(targetItemId)
                        self.tableContainer.addItemAfter(prevItemId, hardware)
                else:
                    self.tableContainer.addItem(hardware)
                source.removeItem(sourceId)

            return

    def getAcceptCriterion(self):
        return And(self.acceptCriterion, AcceptItem.ALL)


class Hardware(object):

    def __init__(self, name, category):
        self._name = name
        self._category = category

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setCategory(self, category):
        self._category = category

    def getCategory(self):
        return self._category