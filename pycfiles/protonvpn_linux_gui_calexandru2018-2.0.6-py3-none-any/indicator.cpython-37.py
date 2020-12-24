# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/protonvpn_gtk/ui/indicator.py
# Compiled at: 2020-01-04 14:28:35
# Size of source mod 2**32: 1784 bytes
import os
from gi.repository import Gtk, GLib
import gi.repository as appindicator
CURRDIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(CURRDIR, '../../icons')
ICON_CONNECTED = os.path.join(ICON_DIR, 'proto.png')
ICON_DISCONNECTED = os.path.join(ICON_DIR, 'proto_red.png')

class IndicatorMenu(Gtk.Menu):

    def __init__(self, root):
        super().__init__()
        self.app = root
        menu_items = (
         (
          'Connect to the fastest', self.app.proton('connect_fastest')),
         (
          'Disconnect', self.app.proton('disconnect')),
         (
          'Status', self.app.main_win.cb_show),
         None,
         (
          'Exit', self.cb_exit, ''))
        for menu_item in menu_items:
            if menu_item is None:
                item = Gtk.SeparatorMenuItem()
            else:
                item = Gtk.MenuItem(label=(menu_item[0]))
                (item.connect)(*('activate', ), *menu_item[1:])
            self.append(item)

    def cb_exit(self, w, data):
        Gtk.main_quit()


class Indicator:

    def __init__(self, root):
        self.app = root
        self.ind = appindicator.Indicator.new(self.app.name, 'indicator-messages', appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.menu = IndicatorMenu(self.app)
        self.check_status(None)
        GLib.timeout_add_seconds(5, self.check_status, None)
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def check_status(self, _):
        connected = self.app.proton('is_connected')()
        icon = ICON_CONNECTED if connected else ICON_DISCONNECTED
        self.ind.set_icon_full(icon, 'protonvpn')
        return True