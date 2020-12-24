# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/entry_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1545 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .basic import GtkAdapter

class EntryAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a Gtk.Entry widget\n    '
    widget_types = ['entry', 'input']
    _check_widget_type = Gtk.Entry
    _wid_read = lambda c, w: Gtk.Entry.get_text(w)
    _wid_write = lambda c, w, v: Gtk.Entry.set_text(w, str(v))
    _signal = 'changed'