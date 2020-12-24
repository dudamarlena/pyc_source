# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/application/icons.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1123 bytes
from pkg_resources import resource_filename
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf

def get_icon_list():
    return [
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_16x16.png')),
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_24x24.png')),
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_32x32.png')),
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_48x48.png')),
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_64x64.png')),
     GdkPixbuf.Pixbuf.new_from_file(resource_filename(__name__, 'icons/pyxrd_icon_128x128.png'))]