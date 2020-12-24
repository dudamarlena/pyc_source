# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/frontend/combobox.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 4231 bytes
import os
import xdg.DesktopEntry as DesktopEntry
from gi.repository import Gtk, GdkPixbuf, GObject
from kazam.backend.prefs import *

class EditComboBox(Gtk.ComboBox):
    KDENLIVE_VERSION = [
     0, 8]
    if prefs.dist[2] == 'quantal' or prefs.dist[2] == 'raring':
        EDITORS = {'/usr/share/app-install/desktop/openshot:openshot.desktop':[],  '/usr/share/app-install/desktop/pitivi:pitivi.desktop':[
          '-i', '-a'], 
         '/usr/share/app-install/desktop/avidemux:avidemux-gtk.desktop':[],  '/usr/share/app-install/desktop/kdenlive:kde4__kdenlive.desktop':[
          '-i']}
    else:
        EDITORS = {'/usr/share/applications/openshot.desktop':[],  '/usr/share/applications/pitivi.desktop':[
          '-i', '-a'], 
         '/usr/share/applications/avidemux-gtk.desktop':[],  '/usr/share/applications/kde4/kdenlive.desktop':[
          '-i']}

    def __init__(self, icons):
        Gtk.ComboBox.__init__(self)
        self.icons = icons
        self.empty = True
        cr_pixbuf = Gtk.CellRendererPixbuf()
        self.pack_start(cr_pixbuf, True)
        self.add_attribute(cr_pixbuf, 'pixbuf', 0)
        cr_text = Gtk.CellRendererText()
        self.pack_start(cr_text, True)
        self.add_attribute(cr_text, 'text', 1)
        self.box_model = Gtk.ListStore(GdkPixbuf.Pixbuf, str, GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)
        self.set_model(self.box_model)
        self._populate()
        self.set_active(0)
        self.set_sensitive(True)
        self.show()

    def get_active_value(self):
        i = self.get_active()
        model = self.get_model()
        model_iter = model.get_iter(i)
        return (model.get_value(model_iter, 2),
         model.get_value(model_iter, 3))

    def _populate(self):
        for item in self.EDITORS:
            if os.path.isfile(item):
                args = self.EDITORS[item]
                desktop_entry = DesktopEntry(item)
                command = desktop_entry.getExec()
                command = command.split(' ')[0]
                name = desktop_entry.getName()
                icon_name = desktop_entry.getIcon()
                self._add_item(icon_name, name, command, args)

        if len(self.get_model()):
            self.empty = False
        else:
            self.empty = True

    def _add_item(self, icon_name, name, command, args):
        liststore = self.get_model()
        try:
            pixbuf = self.icons.load_icon(icon_name, 16, Gtk.IconLookupFlags.GENERIC_FALLBACK)
        except:
            pixbuf = self.icons.load_icon('application-x-executable', 16, Gtk.IconLookupFlags.GENERIC_FALLBACK)

        liststore.append([pixbuf, name, command, args])

    def _version_is_gte(self, required_version, current_version):
        i = 0
        for digit in current_version:
            required_digit = required_version[i]
            current_digit = int(digit)
            if current_digit < required_digit:
                return False

        return True