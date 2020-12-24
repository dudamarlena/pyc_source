# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/arrow_adapter.py
# Compiled at: 2020-03-07 03:51:48
# Size of source mod 2**32: 1546 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .basic import GtkAdapter

class ArrowAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a Gtk.Arrow widget\n    '
    widget_types = ['arrow']
    _check_widget_type = Gtk.Arrow
    _wid_read = lambda a: a.get_property('arrow-type')
    _wid_write = lambda a, v: a.set(v, a.get_property('shadow-type'))
    _signal = 'changed'