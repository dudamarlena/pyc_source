# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/scale_adapter.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1533 bytes
from .basic import GtkAdapter
from .widgets.scale_entry import ScaleEntry

class ScaleEntryAdapter(GtkAdapter):
    __doc__ = '\n        An adapter for a ScaleEntry widget.\n    '
    widget_types = ['scale']
    _check_widget_type = ScaleEntry
    _wid_read = GtkAdapter.static_to_class(ScaleEntry.get_value)
    _wid_write = GtkAdapter.static_to_class(ScaleEntry.set_value)
    _signal = 'changed'