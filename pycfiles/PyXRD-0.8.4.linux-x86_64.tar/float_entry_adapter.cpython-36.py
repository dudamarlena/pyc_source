# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/float_entry_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2726 bytes
import re, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .entry_adapter import EntryAdapter

class FloatEntryAdapter(EntryAdapter):
    __doc__ = '\n        An adapter for a Gtk.Entry widget holding a float.\n    '
    widget_types = ['float_entry', 'float_input']
    _check_widget_type = Gtk.Entry
    _signal = 'changed'

    def __init__(self, *args, **kwargs):
        (super(FloatEntryAdapter, self).__init__)(*args, **kwargs)
        numeric_const_pattern = '\n        [-+]? # optional sign\n        (?:\n            (?: \\d* \\. \\d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc\n            |\n            (?: \\d+ \\.? ) # 1. 12. 123. etc 1 12 123 etc\n        )\n        # followed by optional exponent part if desired\n        (?: [Ee] [+-]? \\d+ ) ?\n        '
        self.rx = re.compile(numeric_const_pattern, re.VERBOSE)

    def _prop_read(self, *args):
        return str(*args)

    def _prop_write(self, *args):
        try:
            return float(*args)
        except ValueError:
            return self._get_property_value()

    def _on_wid_changed(self, widget, *args):
        with self._block_widget_signal():
            if self._ignoring_notifs:
                return
            self._validate_float(widget)
            (super(FloatEntryAdapter, self)._on_wid_changed)(widget, *args)

    def _validate_float(self, entry):
        entry_text = entry.get_text()
        newtext = self.rx.findall(entry_text)
        if len(newtext) > 0:
            entry.set_text(newtext[0])
        else:
            entry.set_text('')