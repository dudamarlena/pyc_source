# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dragndrop/DragDropServerValidationExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.event.dd.acceptcriteria.server_side_criterion import ServerSideCriterion
from muntjac.terminal.gwt.client.ui.dd.vertical_drop_location import VerticalDropLocation
from muntjac.api import HorizontalLayout, Table
from muntjac.ui.table import TableDragMode
from muntjac.event.dd.drop_handler import IDropHandler
from muntjac.event.data_bound_transferable import DataBoundTransferable

class DragDropServerValidationExample(HorizontalLayout):

    def __init__(self):
        super(DragDropServerValidationExample, self).__init__()
        self.setSpacing(True)
        self._table = Table('Drag persons onto their relatives')
        self._table.setWidth('100%')
        self._container = ExampleUtil.getPersonContainer()
        self._table.setContainerDataSource(self._container)
        self._table.setDragMode(TableDragMode.ROW)
        self._table.setDropHandler(TableDropHandler(self))
        self.addComponent(self._table)

    def getFullName(self, itemId):
        item = self._container.getItem(itemId)
        if item is None:
            return
        else:
            fn = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
            ln = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
            return fn + ' ' + ln

    def getLastName(self, itemId):
        item = self._container.getItem(itemId)
        if item is None:
            return
        else:
            return item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()


class TableDropHandler(IDropHandler):

    def __init__(self, example):
        self._example = example

    def drop(self, dropEvent):
        t = dropEvent.getTransferable()
        sourceItemId = t.getItemId()
        dropData = dropEvent.getTargetDetails()
        targetItemId = dropData.getItemIdOver()
        self.getWindow().showNotification(self.getFullName(sourceItemId) + ' is related to ' + self.getFullName(targetItemId))

    def getAcceptCriterion(self):
        return RelativeCriterion(self._example)


class RelativeCriterion(ServerSideCriterion):

    def __init__(self, example):
        super(RelativeCriterion, self).__init__()
        self._example = example

    def accept(self, dragEvent):
        if dragEvent.getTransferable().getSourceComponent() != self._example._table or not isinstance(dragEvent.getTransferable(), DataBoundTransferable):
            return False
        dropData = dragEvent.getTargetDetails()
        if not VerticalDropLocation.MIDDLE == dropData.getDropLocation():
            return False
        else:
            t = dragEvent.getTransferable()
            sourceItemId = t.getItemId()
            targetItemId = dropData.getItemIdOver()
            if sourceItemId == targetItemId:
                return False
            sourceLastName = self._example.getLastName(sourceItemId)
            targetLastName = self._example.getLastName(targetItemId)
            if sourceLastName is not None and sourceLastName == targetLastName:
                return True
            return False