# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/check_menu_item_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1561 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .basic import GtkAdapter

class CheckMenuItemAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a Gtk.CheckMenuItem widget\n    '
    widget_types = ['check_menu']
    _check_widget_type = Gtk.CheckMenuItem
    _wid_read = GtkAdapter.static_to_class(Gtk.CheckMenuItem.get_active)
    _wid_write = GtkAdapter.static_to_class(Gtk.CheckMenuItem.set_active)
    _signal = 'toggled'