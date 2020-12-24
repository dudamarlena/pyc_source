# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doctormo/Projects/python/libs/gtkme/trunk/doc/examples/listview.py
# Compiled at: 2014-06-05 09:48:25
"""
Sample example application using GtkMe
"""
import os, sys, logging
sys.path.insert(1, '../../lib')
sys.path.insert(1, './lib')
from gtkme import Window, GtkApp, TreeView, ViewColumn, ViewSort, Separator

class ExampleTreeView(TreeView):
    """Show how easy it is to make a list of items with icons."""

    def get_markup(self, item):
        return item._foo

    def setup(self, widget):
        """Setup the treeview with one or many columns manually"""
        self.ViewColumn('Column Name')
        self.ViewColumn('Second Column', expand=True, text='second', template='<b>%s</b>', icon=('icon',
                                                                                                 'default-icon'), pad=0, size=12)
        self.ViewColumn('Third Column', expand=False, text=self.get_markup, template='<i>%s</i>', icon=lambda item: item.icon, pad=6, size=22)
        self.ViewSort(data=self.get_markup, ascending=True, contains='third')


class Item(object):
    """All List Items are Objects"""

    def __init__(self, name, second, icon):
        self._foo = name
        self.second = second
        self.icon = icon

    def __unicode__(self):
        return self._foo


class AppWindow(Window):
    """We need to load the window the list is in"""
    name = 'listapp'

    def load_widgets(self):
        self.a = self.load_listwidget(TreeView, 'automatic')
        self.b = self.load_listwidget(ExampleTreeView, 'manual')

    def load_listwidget(self, container, name):
        result = container(self.widget(name), selected=self.signal)
        result.add_item(Item('First Item', '1', 'gtk-quit'))
        result.add([
         Item('Second Item', '4', 'gtk-close'),
         Item('Third Item', '12', 'gtk-open'),
         Item('Fouth Item', '101011', 'find')])
        return result

    def signal(self, item):
        print "Item passed '%s' vs Item selected '%s'" % (unicode(item), unicode(self.a.selected))


class ListApp(GtkApp):
    glade_dir = './'
    app_name = 'listapp'
    windows = [AppWindow]


if __name__ == '__main__':
    try:
        app = ListApp(start_loop=True)
    except KeyboardInterrupt:
        logging.info('User Interputed')

    logging.debug('Exiting Application')