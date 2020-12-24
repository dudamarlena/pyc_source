# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/frontend/about_dialog.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 2874 bytes
from gettext import gettext as _
from gi.repository import Gtk
from kazam.version import *
AUTHORS = '\nAndrew Higginson <rugby471@gmail.com>\nDavid Klasinc <bigwhale@lubica.net>\n'
ARTISTS = '\nMatthew Paul Thomas <mpt@canonical.com>\nGeorgi Karavasilev <kokoto-java@ubuntu.com>\nFrank Souza <franksouza183@gmail.com>\nSam Hewitt <snwh@ubuntu.com>\nRobert McKenna <ttk1opc@yahoo.com>\nAndrew Higginson <rugby471@gmail.com>\n'
LICENSE = '\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'

def AboutDialog(icons):
    dialog = Gtk.AboutDialog()
    dialog.set_program_name(_('Kazam') + ' - "' + CODENAME + '"')
    dialog.set_comments(_('Record a video of activity on your screen or capture a screenshot.'))
    dialog.set_license(LICENSE)
    dialog.set_version(VERSION)
    dialog.set_copyright('© 2010 Andrew Higginson, © 2012 David Klasinc')
    dialog.set_website('http://launchpad.net/kazam')
    dialog.set_authors(AUTHORS.split('\n'))
    dialog.set_artists(ARTISTS.split('\n'))
    try:
        icon = icons.load_icon('kazam', 96, Gtk.IconLookupFlags.GENERIC_FALLBACK)
        dialog.set_logo(icon)
    except:
        pass

    dialog.show_all()
    dialog.set_position(Gtk.WindowPosition.CENTER)
    dialog.run()
    dialog.hide()