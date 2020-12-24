# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kitt/plugin_wnck.py
# Compiled at: 2013-05-21 16:22:01
from kivy.logger import Logger
log = Logger.getChild('KiTT')
import gtk, sys, dbus, subprocess, os, wnck
from actions import Actions

def workspace_up():
    while gtk.events_pending():
        gtk.main_iteration()

    self.screen.get_workspace_neighbor(self.screen.get_active_workspace(), wnck.MOTION_LEFT).activate(0)
    return True


def workspace_down():
    while gtk.events_pending():
        gtk.main_iteration()

    self.screen.get_workspace_neighbor(self.screen.get_active_workspace(), wnck.MOTION_RIGHT).activate(0)
    return True


ACTIONS = dict(workspace_up=workspace_up, workspace_down=workspace_down)