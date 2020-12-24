# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/controllers/dialog_controller.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1039 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk
from pyxrd.generic.controllers.base_controller import BaseController

class DialogController(BaseController):
    __doc__ = '\n        Simple controller which has a DialogView subclass instance as view.\n    '

    def on_btn_ok_clicked(self, event):
        self.on_cancel()
        return True

    def on_keypress(self, widget, event):
        if event.keyval == Gdk.keyval_from_name('Escape'):
            self.on_cancel()
            return True

    def on_window_edit_dialog_delete_event(self, event, args=None):
        self.on_cancel()
        return True

    def on_cancel(self):
        self.view.hide()