# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/trees/TreeMultiSelectExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import VerticalLayout, Tree, Button
from muntjac.ui import button
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.data.property import IValueChangeListener
from muntjac.ui.abstract_select import AbstractSelect

class TreeMultiSelectExample(VerticalLayout, action.IHandler):
    _ACTION_ADD = Action('Add child item')
    _ACTION_DELETE = Action('Delete')
    _ACTIONS = [_ACTION_ADD, _ACTION_DELETE]

    def __init__(self):
        super(TreeMultiSelectExample, self).__init__()
        self.setSpacing(True)
        self._tree = Tree('Hardware Inventory', ExampleUtil.getHardwareContainer())
        self._tree.setMultiSelect(True)
        self._tree.setImmediate(True)
        self._tree.addListener(TreeListener(self), IValueChangeListener)
        self._tree.addActionHandler(self)
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        for idd in self._tree.rootItemIds():
            self._tree.expandItemsRecursively(idd)

        self._deleteButton = Button('Delete', DeleteListener(self))
        self._deleteButton.setEnabled(False)
        self.addComponent(self._deleteButton)
        self.addComponent(self._tree)

    def getActions(self, target, sender):
        return self._ACTIONS

    def handleAction(self, a, sender, target):
        if a == self._ACTION_ADD:
            self._tree.setChildrenAllowed(target, True)
            itemId = self._tree.addItem()
            self._tree.setChildrenAllowed(itemId, False)
            newItemName = 'New Item # %d' % itemId
            item = self._tree.getItem(itemId)
            p = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            p.setValue(newItemName)
            self._tree.setParent(itemId, target)
            self._tree.expandItem(target)
        elif a == self._ACTION_DELETE:
            parent = self._tree.getParent(target)
            self._tree.removeItem(target)
            if parent is not None and len(self._tree.getChildren(parent)) == 0:
                self._tree.setChildrenAllowed(parent, False)
        return


class TreeListener(IValueChangeListener):

    def __init__(self, c):
        self._c = c

    def valueChange(self, event):
        t = event.getProperty()
        enabled = t.getValue() is not None and len(t.getValue()) > 0
        self._c._deleteButton.setEnabled(enabled)
        return


class DeleteListener(button.IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        toDelete = list(self._c._tree.getValue())
        for i in range(len(toDelete)):
            self._c.handleAction(self._c._ACTION_DELETE, self._c._tree, toDelete[i])