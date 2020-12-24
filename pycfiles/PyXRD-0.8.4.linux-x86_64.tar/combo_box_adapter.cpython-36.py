# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/combo_box_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3360 bytes
import logging
logger = logging.getLogger(__name__)
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ...support.utils import not_none
from .basic import GtkAdapter

class ComboBoxAdapter(GtkAdapter):
    __doc__ = '\n        An adapter that adapts a ComboBox widget to an property which has a \n        choices attribute containing dictionary with allowed (value, description)\n        pairs as keys and values.\n    '
    widget_types = ['option_list']
    _check_widget_type = Gtk.ComboBox
    _wid_read = lambda c, w, *a: (Gtk.ComboBox.get_active_iter)(w, *a)
    _wid_write = lambda c, w, *a: (Gtk.ComboBox.set_active_iter)(w, *a)
    _signal = 'changed'
    _prop_cast = False

    def _parse_prop(self, prop, model):
        prop, model = super(ComboBoxAdapter, self)._parse_prop(prop, model)
        if not isinstance(prop.choices, dict):
            raise ValueError("ComboBox widget handler requires a property with a 'choices' dictionary!")
        else:
            self._store = Gtk.ListStore(str, str)
            for key, value in prop.choices.items():
                self._store.append([str(key), str(value)])

        return (
         prop, model)

    def _prop_write(self, itr):
        if itr is not None:
            return self._store.get_value(itr, 0)

    def _prop_read(self, val):
        for row in self._store:
            if self._store.get_value(row.iter, 0) == str(val):
                return row.iter

    def _connect_widget(self):
        cell = Gtk.CellRendererText()
        self._widget.clear()
        self._widget.pack_start(cell, True)
        self._widget.add_attribute(cell, 'text', 1)
        cell.set_property('family', 'Monospace')
        cell.set_property('size-points', 10)
        self._widget.set_model(self._store)
        super(ComboBoxAdapter, self)._connect_widget()

    def disconnect(self, model=None, widget=None):
        widget = not_none(self._widget, widget)
        if widget is not None:
            widget.set_model(None)
        super(ComboBoxAdapter, self).disconnect(model=model, widget=widget)