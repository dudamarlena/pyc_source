# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/color_button_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1751 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .basic import GtkAdapter
from ._gtk_color_utils import _parse_color_string, _parse_color_value

class ColorButtonAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a Gtk.Label widget\n    '
    widget_types = ['color', 'color_button']
    _check_widget_type = Gtk.ColorButton
    _wid_read = lambda s, w: w.get_rgba()
    _wid_write = lambda s, w, v: w.set_rgba(v) if w.get_realized() else None
    _signal = 'color-set'
    _prop_read = lambda s, *a: _parse_color_string(*a)
    _prop_write = lambda s, *a: _parse_color_value(*a)