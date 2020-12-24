# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/dialogs/message_dialog.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2261 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .utils import run_dialog

class MessageDialog(Gtk.MessageDialog):
    accept_responses = (
     Gtk.ResponseType.ACCEPT,
     Gtk.ResponseType.YES,
     Gtk.ResponseType.APPLY,
     Gtk.ResponseType.OK)

    def __init__(self, message, parent=None, type=Gtk.MessageType.INFO, flags=Gtk.DialogFlags.DESTROY_WITH_PARENT, buttons=Gtk.ButtonsType.NONE, persist=False, title=None):
        super(MessageDialog, self).__init__(parent=parent,
          type=type,
          flags=flags,
          buttons=buttons)
        self.persist = persist
        self.set_markup(message)
        if title is not None:
            self.set_title(title)

    def run(self, *args, **kwargs):
        kwargs['destroy'] = not self.persist
        return run_dialog(self, *args, **kwargs)