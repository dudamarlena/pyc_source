# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/menubar/MenuBarCheckableItemsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, MenuBar
from muntjac.ui.menu_bar import ICommand

class MenuBarCheckableItemsExample(VerticalLayout):

    def __init__(self):
        super(MenuBarCheckableItemsExample, self).__init__()
        self._menubar = MenuBar()
        menuCommand = MenuCommand(self)
        f = self._menubar.addItem('File', None)
        f.addItem('New...', menuCommand)
        f.addItem('Open...', menuCommand)
        f.addSeparator()
        f.addItem('Save', menuCommand)
        f.addSeparator()
        saveOnExit = f.addItem('Save on exit', menuCommand)
        saveOnExit.setCheckable(True)
        saveOnExit.setChecked(True)
        f.addSeparator()
        f.addItem('Exit', menuCommand)
        settings = self._menubar.addItem('Settings', None)
        setting1 = settings.addItem('Allow settings to be changed by all users', menuCommand)
        setting1.setCheckable(True)
        setting1.setChecked(True)
        setting2 = settings.addItem('Convert XML files automatically', menuCommand)
        setting2.setCheckable(True)
        setting3 = settings.addItem('Convert files automatically', menuCommand)
        setting3.setCheckable(True)
        settings.addSeparator()
        settings.addItem('More settings...', menuCommand)
        self.addComponent(self._menubar)
        return


class MenuCommand(ICommand):

    def __init__(self, c):
        self._c = c

    def menuSelected(self, selectedItem):
        if selectedItem.isCheckable():
            self._c.getWindow().showNotification("'" + selectedItem.getText() + "' was set to " + ('true' if selectedItem.isChecked() else 'false'))
        else:
            self._c.getWindow().showNotification("Non-selectable item '" + selectedItem.getText() + "' was clicked")