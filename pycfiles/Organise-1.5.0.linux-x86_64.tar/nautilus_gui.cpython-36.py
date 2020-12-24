# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/scripts/nautilus_gui.py
# Compiled at: 2018-12-11 06:38:32
# Size of source mod 2**32: 722 bytes
import os
from gi import require_version
require_version('Gtk', '3.0')
require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):

    def menu_activate_cb(self, menu, file):
        os.system('organise -p {}'.format(file.get_location().get_path()))

    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        else:
            file = files[0]
            item = Nautilus.MenuItem(name='OrganiseExtension::Organise_Files',
              label='Organise',
              tip='Organise your folder')
            item.connect('activate', self.menu_activate_cb, file)
            return [
             item]