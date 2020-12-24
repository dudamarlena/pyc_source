# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/_gtk_color_utils.py
# Compiled at: 2020-03-07 03:51:48
# Size of source mod 2**32: 1592 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk

def _parse_color_string(value):
    """Converts a hex-formatted (e.g. #FFFFFF) string to a Gdk color object"""
    color = Gdk.RGBA()
    color.parse(value)
    return color


def _parse_color_value(value):
    """Converts a Gdk color object to a hex-formatted string (e.g. #FFFFFF)"""
    return '#%02x%02x%02x' % (int(value.red * 255), int(value.green * 255), int(value.blue * 255))