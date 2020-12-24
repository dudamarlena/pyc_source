# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/trees/TreeSingleSelectExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.ExampleUtil import ExampleUtil
from muntjac.api import HorizontalLayout, Button, Tree, TextField, Alignment
from muntjac.ui import button
from muntjac.data.property import IValueChangeListener
from muntjac.event.action import Action
from muntjac.event import action
from muntjac.ui.abstract_select import AbstractSelect

class TreeSingleSelectExample(HorizontalLayout, IValueChangeListener, button.IClickListener, action.IHandler):
    _ACTION_ADD = Action('Add child item')
    _ACTION_DELETE = Action('Delete')

    def __init__(self):
        super(TreeSingleSelectExample, self).__init__()
        self.setSpacing(True)
        self._tree = Tree('Hardware Inventory')
        self.addComponent(self._tree)
        self._tree.setContainerDataSource(ExampleUtil.getHardwareContainer())
        self._tree.addListener(self, IValueChangeListener)
        self._tree.addActionHandler(self)
        self._tree.setImmediate(True)
        self._tree.setItemCaptionPropertyId(ExampleUtil.hw_PROPERTY_NAME)
        self._tree.setItemCaptionMode(AbstractSelect.ITEM_CAPTION_MODE_PROPERTY)
        for idd in self._tree.rootItemIds():
            self._tree.expandItemsRecursively(idd)

        self._editBar = HorizontalLayout()
        self._editBar.setMargin(False, False, False, True)
        self._editBar.setEnabled(False)
        self.addComponent(self._editBar)
        self._editor = TextField('Item name')
        self._editor.setImmediate(True)
        self._editBar.addComponent(self._editor)
        self._change = Button('Apply', self)
        self._editBar.addComponent(self._change)
        self._editBar.setComponentAlignment(self._change, Alignment.BOTTOM_LEFT)

    def valueChange(self, event):
        if event.getProperty().getValue() is not None:
            val = self._tree.getItem(event.getProperty().getValue()).getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            self._editor.setValue(val)
            self._editor.requestRepaint()
            self._editBar.setEnabled(True)
        else:
            self._editor.setValue('')
            self._editBar.setEnabled(False)
        return

    def buttonClick(self, event):
        if not self._editor.getValue() == '':
            item = self._tree.getItem(self._tree.getValue())
            name = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            name.setValue(self._editor.getValue())

    def getActions(self, target, sender):
        return [
         self._ACTION_ADD, self._ACTION_DELETE]

    def handleAction(self, a, sender, target):
        if a == self._ACTION_ADD:
            self._tree.setChildrenAllowed(target, True)
            self._tree.expandItem(target)
            itemId = self._tree.addItem()
            self._tree.setParent(itemId, target)
            self._tree.setChildrenAllowed(itemId, False)
            item = self._tree.getItem(itemId)
            name = item.getItemProperty(ExampleUtil.hw_PROPERTY_NAME)
            name.setValue('New Item')
        elif a == self._ACTION_DELETE:
            parent = self._tree.getParent(target)
            self._tree.removeItem(target)
            if parent is not None and len(self._tree.getChildren(parent)) == 0:
                self._tree.setChildrenAllowed(parent, False)
        return