# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/adapters/gtk_support/toolkit_functions.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1768 bytes
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

def add_idle_call(func, *args):
    source = GLib.MainContext.default().find_source_by_id((GLib.idle_add)(func, *args, **{'priority': GLib.PRIORITY_HIGH_IDLE}))
    return source


def remove_source(source):
    return source.destroy()


def add_timeout_call(timeout, func, *args):
    source = GLib.MainContext.default().find_source_by_id((GLib.timeout_add)(timeout, func, *args, **{'priority': GLib.PRIORITY_HIGH}))
    return source


def start_event_loop():
    return Gtk.main()


def stop_event_loop():
    return Gtk.main_quit()