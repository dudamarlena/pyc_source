# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/table/TableStylingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Table, Link, Button, Alignment
from muntjac.ui import button
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.ui.table import IColumnGenerator, ICellStyleGenerator
from muntjac.terminal.external_resource import ExternalResource
from muntjac.event.item_click_event import IItemClickListener, ItemClickEvent
ACTION_RED = Action('red')
ACTION_BLUE = Action('blue')
ACTION_GREEN = Action('green')
ACTION_NONE = Action('none')
ACTIONS = [ACTION_RED, ACTION_GREEN, ACTION_BLUE, ACTION_NONE]

class TableStylingExample(VerticalLayout):

    def __init__(self):
        super(TableStylingExample, self).__init__()
        self.setSpacing(True)
        self._table = Table()
        self._markedRows = dict()
        self._markedCells = dict()
        self.addComponent(self._table)
        self._table.setStyleName('contacts')
        self._table.setWidth('100%')
        self._table.setPageLength(7)
        self._table.setContainerDataSource(ExampleUtil.getPersonContainer())
        self._table.addGeneratedColumn('Email', TableColumnGenerator(self))
        self._table.setColumnReorderingAllowed(True)
        self._table.setColumnCollapsingAllowed(True)
        self._table.addActionHandler(TableActionHandler(self))
        self._table.setCellStyleGenerator(TableStyleGenerator(self))
        self._table.addListener(TableClickListener(self), IItemClickListener)
        self._table.setWriteThrough(False)
        editButton = Button('Edit')
        self.addComponent(editButton)
        editButton.addListener(EditListener(self, editButton), button.IClickListener)
        self.setComponentAlignment(editButton, Alignment.TOP_RIGHT)


class TableColumnGenerator(IColumnGenerator):

    def __init__(self, c):
        self._c = c

    def generateCell(self, source, itemId, columnId):
        item = self._c._table.getItem(itemId)
        fn = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_FIRSTNAME).getValue()
        ln = item.getItemProperty(ExampleUtil.PERSON_PROPERTY_LASTNAME).getValue()
        email = fn.lower() + '.' + ln.lower() + '@example.com'
        emailLink = Link(email, ExternalResource('mailto:' + email))
        return emailLink


class TableActionHandler(action.IHandler):

    def __init__(self, c):
        self._c = c

    def getActions(self, target, sender):
        return ACTIONS

    def handleAction(self, a, sender, target):
        if target in self._c._markedRows:
            del self._c._markedRows[target]
        if a != ACTION_NONE:
            self._c._markedRows[target] = a.getCaption()
        self._c._table.requestRepaint()


class TableStyleGenerator(ICellStyleGenerator):

    def __init__(self, c):
        self._c = c

    def getStyle(self, itemId, propertyId):
        if propertyId is None:
            return self._c._markedRows.get(itemId)
        else:
            if propertyId == 'Email':
                return 'email'
            else:
                cells = self._c._markedCells.get(itemId)
                if cells is not None and propertyId in cells:
                    return 'marked'
                return

            return


class TableClickListener(IItemClickListener):

    def __init__(self, c):
        self._c = c

    def itemClick(self, event):
        if event.getButton() == ItemClickEvent.BUTTON_RIGHT:
            pass
        if event.isDoubleClick():
            itemId = event.getItemId()
            propertyId = event.getPropertyId()
            cells = self._c._markedCells.get(itemId)
            if cells is None:
                cells = set()
                self._c._markedCells[itemId] = cells
            if propertyId in cells:
                cells.remove(propertyId)
            else:
                cells.add(propertyId)
            self._c._table.requestRepaint()
        return


class EditListener(button.IClickListener):

    def __init__(self, c, editButton):
        self._c = c
        self._editButton = editButton

    def buttonClick(self, event):
        self._c._table.setEditable(not self._c._table.isEditable())
        if self._c._table.isEditable():
            self._editButton.setCaption('Save')
        else:
            self._editButton.setCaption('Edit')