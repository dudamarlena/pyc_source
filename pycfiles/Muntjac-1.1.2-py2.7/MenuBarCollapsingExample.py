# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/menubar/MenuBarCollapsingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout
from muntjac.ui.menu_bar import MenuBar, ICommand
from muntjac.terminal.external_resource import ExternalResource

class MenuBarCollapsingExample(VerticalLayout):

    def __init__(self):
        super(MenuBarCollapsingExample, self).__init__()
        self._menubar = MenuBar()
        menuCommand = MenuCommand(self)
        self._menubar.setWidth('50%')
        f = self._menubar.addItem('File', None)
        newItem = f.addItem('New', None)
        f.addItem('Open f...', menuCommand)
        f.addSeparator()
        newItem.addItem('File', menuCommand)
        newItem.addItem('Folder', menuCommand)
        newItem.addItem('Project...', menuCommand)
        f.addItem('Close', menuCommand)
        f.addItem('Close All', menuCommand)
        f.addSeparator()
        f.addItem('Save', menuCommand)
        f.addItem('Save As...', menuCommand)
        f.addItem('Save All', menuCommand)
        for i in range(5):
            self._menubar.addItem('Item %d' % i, menuCommand).setEnabled(False)

        edit = self._menubar.addItem('Edit', None)
        edit.addItem('Undo', menuCommand)
        edit.addItem('Redo', menuCommand).setEnabled(False)
        edit.addSeparator()
        edit.addItem('Cut', menuCommand)
        edit.addItem('Copy', menuCommand)
        edit.addItem('Paste', menuCommand)
        edit.addSeparator()
        find = edit.addItem('Find/Replace', menuCommand)
        find.addItem('Google Search', SearchCommand(self))
        find.addSeparator()
        find.addItem('Find/Replace...', menuCommand)
        find.addItem('Find Next', menuCommand)
        find.addItem('Find Previous', menuCommand)
        view = self._menubar.addItem('View', None)
        view.addItem('Show/Hide Status Bar', menuCommand)
        view.addItem('Customize Toolbar...', menuCommand)
        view.addSeparator()
        view.addItem('Actual Size', menuCommand)
        view.addItem('Zoom In', menuCommand)
        view.addItem('Zoom Out', menuCommand)
        for i in range(5):
            self._menubar.addItem('Item %d' % i, menuCommand).setEnabled(False)

        self.addComponent(self._menubar)
        return


class SearchCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        er = ExternalResource('http://www.google.com')
        self._c.getWindow().open(er)


class MenuCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        self._c.getWindow().showNotification('Action ' + selectedItem.getText())