# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/text_view_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3151 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .basic import GtkAdapter

class TextViewAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a TextView widget.\n    '
    widget_types = ['text_view']
    _check_widget_type = Gtk.TextView
    _prop_cast = False

    def _read_widget(self):
        """Returns the value currently stored into the widget."""
        return str((self._buffer.get_text)(*self._buffer.get_bounds()))

    def _write_widget(self, val):
        """Writes value into the widget. If specified, user setter
        is invoked."""
        with self._ignore_notifications():
            return self._buffer.set_text(val)

    _signal = 'changed'

    def __init__(self, controller, prop, widget, value_error=None, spurious=False, update=True):
        if prop.data_type == object:
            self._buffer = self._read_property()
        else:
            self._buffer = Gtk.TextBuffer()
        super(TextViewAdapter, self).__init__(controller, prop, widget, value_error=value_error,
          spurious=spurious,
          update=update)
        self._widget.set_buffer(self._buffer)

    def _connect_widget(self):
        """Called when the adapter is ready to connect to the widget"""
        if self._signal:
            self._signal_id = self._buffer.connect(self._signal, self._on_wid_changed, self._signal_args)
        if self._update:
            self.update_widget()

    def _disconnect_widget(self, widget=None):
        """Disconnects the widget"""
        if self._signal is not None:
            if self._signal_id is not None:
                self._buffer.disconnect(self._signal_id)

    def _set_property_value(self, val):
        """Private method that sets the property value stored in the model,
        without transformations."""
        return setattr(self._model, self._prop.label, val)