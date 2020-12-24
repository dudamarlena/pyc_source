# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/list_toolbar.py
# Compiled at: 2012-04-18 08:51:19
import gtk

class ListToolbar(gtk.Toolbar):
    """
    CLASS: ObserverToolbar
    DESCR:
    """

    def __init__(self, configuration_list):
        gtk.Toolbar.__init__(self)
        conf = configuration_list
        self.iconSize = gtk.ICON_SIZE_BUTTON
        self.set_border_width(0)
        self.set_style(gtk.TOOLBAR_ICONS)
        self.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        self.buttons = {}
        for item in conf:
            if type(item) == list:
                self.__add_button(item[0], item[1], item[2], item[3])
            elif item == '-':
                self.append_space()

        self.show_all()

    def __add_button(self, stock, title, tooltip, callback):
        iconw = gtk.Image()
        iconw.set_from_stock(stock, self.iconSize)
        button = self.append_item(title, tooltip, 'Private', iconw, callback)
        self.buttons[title] = button
        return button