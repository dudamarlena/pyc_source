# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/widgets/wdg_statusbar.py
# Compiled at: 2019-03-22 16:56:02
# Size of source mod 2**32: 1552 bytes
"""
# File: wdg_statusbar.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Statusbar Widget
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from basico.core.mod_env import ROOT, USER_DIR, APP, LPATH, GPATH, FILE
from basico.core.mod_wdg import BasicoWidget

class Statusbar(BasicoWidget, Gtk.HBox):

    def __init__(self, app):
        super().__init__(app, __class__.__name__)
        Gtk.HBox.__init__(self)
        self.get_services()
        self.setup()

    def setup(self):
        vbox = Gtk.VBox()
        viewport = Gtk.Viewport()
        viewport.set_shadow_type(Gtk.ShadowType.NONE)
        separator = Gtk.Separator()
        self.statusbar = self.srvgui.add_widget('gtk_label_statusbar', Gtk.Label())
        self.statusbar.set_property('ellipsize', Pango.EllipsizeMode.MIDDLE)
        self.statusbar.set_property('selectable', True)
        self.statusbar.set_property('margin-left', 6)
        self.statusbar.set_property('margin-right', 6)
        self.statusbar.set_property('margin-top', 0)
        self.statusbar.set_property('margin-bottom', 6)
        self.statusbar.set_xalign(0.0)
        viewport.add(self.statusbar)
        vbox.pack_start(separator, True, False, 0)
        vbox.pack_start(viewport, True, False, 0)
        self.add(vbox)

    def get_services(self):
        self.srvgui = self.get_service('GUI')

    def message(self, message):
        self.statusbar.set_markup('<b>%s</b>' % message)