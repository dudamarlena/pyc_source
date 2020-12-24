# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/admin/menu.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui

class Menu(object):
    """A menu is a part of the main menu shown on the main window.  Each Menu
contains a list of items the user select.  Such a menu item is either a Menu
itself, an Action object or None to insert a separator.
    """

    def __init__(self, verbose_name, items, icon=None):
        self.verbose_name = verbose_name
        self.icon = icon
        self.items = items

    def get_verbose_name(self):
        return self.verbose_name

    def get_icon(self):
        return self.icon

    def get_items(self):
        return self.items

    def render(self, gui_context, parent):
        """
        :return: a :class:`QtGui.QMenu` object
        """
        menu = QtGui.QMenu(unicode(self.get_verbose_name()), parent)
        for item in self.get_items():
            if item == None:
                menu.addSeparator()
                continue
            rendered_item = item.render(gui_context, menu)
            if isinstance(rendered_item, QtGui.QMenu):
                menu.addMenu(rendered_item)
            elif isinstance(rendered_item, QtGui.QAction):
                menu.addAction(rendered_item)
            else:
                raise Exception('Cannot handle menu items of type %s' % type(rendered_item))

        return menu