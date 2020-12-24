# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/menu_bar_ids.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.menu_bar import ICommand, MenuBar

class MenuBarIds(TestCase, ICommand):

    def setUp(self):
        self._menuBar = MenuBar()
        self._menuFile = self._menuBar.addItem('File', self)
        self._menuEdit = self._menuBar.addItem('Edit', self)
        self._menuEditCopy = self._menuEdit.addItem('Copy', self)
        self._menuEditCut = self._menuEdit.addItem('Cut', self)
        self._menuEditPaste = self._menuEdit.addItem('Paste', self)
        self._menuEdit.addSeparator()
        self._menuEditFind = self._menuEdit.addItem('Find...', self)
        self._menuFileOpen = self._menuFile.addItem('Open', self)
        self._menuFileSave = self._menuFile.addItem('Save', self)
        self._menuFile.addSeparator()
        self._menuFileExit = self._menuFile.addItem('Exit', self)
        self._menuItems = set()
        self._menuItems.add(self._menuFile)
        self._menuItems.add(self._menuEdit)
        self._menuItems.add(self._menuEditCopy)
        self._menuItems.add(self._menuEditCut)
        self._menuItems.add(self._menuEditPaste)
        self._menuItems.add(self._menuEditFind)
        self._menuItems.add(self._menuFileOpen)
        self._menuItems.add(self._menuFileSave)
        self._menuItems.add(self._menuFileExit)
        self._lastSelectedItem = None
        return

    def testMenubarIdUniqueness(self):
        self.assertUniqueIds(self._menuBar)
        self._menuBar.removeItem(self._menuFile)
        file2 = self._menuBar.addItem('File2', self)
        file3 = self._menuBar.addItem('File3', self)
        file2sub = file2.addItem('File2 sub menu', self)
        self._menuItems.add(file2)
        self._menuItems.add(file2sub)
        self._menuItems.add(file3)
        self.assertUniqueIds(self._menuBar)

    @classmethod
    def assertUniqueIds(cls, *args):
        nargs = len(args)
        if nargs == 1:
            menuBar, = args
            ids = set()
            for item in menuBar.getItems():
                cls.assertUniqueIds(ids, item)

        elif nargs == 2:
            ids, item = args
            idd = item.getId()
            print 'Item ' + item.getText() + ', id: ' + str(idd)
            assert idd not in ids
            ids.add(idd)
            if item.getChildren() is not None:
                for subItem in item.getChildren():
                    cls.assertUniqueIds(ids, subItem)

        else:
            raise ValueError
        return

    def menuSelected(self, selectedItem):
        self.assertEquals('lastSelectedItem was not cleared before selecting an item', self._lastSelectedItem)
        self._lastSelectedItem = selectedItem