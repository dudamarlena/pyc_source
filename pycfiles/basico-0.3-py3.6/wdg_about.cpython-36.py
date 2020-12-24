# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/widgets/wdg_about.py
# Compiled at: 2019-03-16 08:33:40
# Size of source mod 2**32: 2774 bytes
"""
# -*- coding: utf-8 -*-
# File: wdg_about.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: About Widget
"""
from html import escape
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from basico.core.mod_wdg import BasicoWidget
from basico.core.mod_env import APP

class About(BasicoWidget, Gtk.ScrolledWindow):
    __doc__ = '\n    About class\n    '

    def __init__(self, app):
        super().__init__(app, __class__.__name__)
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.set_hexpand(True)
        self.set_vexpand(True)
        viewport = Gtk.Viewport()
        widget = Gtk.VBox()
        viewport.add(widget)
        widget.set_hexpand(True)
        widget.set_vexpand(True)
        label = Gtk.Label()
        label.modify_font(Pango.FontDescription('Monospace 92'))
        widget.pack_start(label, False, False, 6)
        label = Gtk.Label()
        label.set_markup('<b>%s %s</b>' % (APP['short'].capitalize(), APP['version']))
        label.modify_font(Pango.FontDescription('Monospace 48'))
        widget.pack_start(label, False, False, 6)
        label = Gtk.Label()
        label.set_markup('%s' % APP['name'])
        label.modify_font(Pango.FontDescription('Arial 24'))
        widget.pack_start(label, False, False, 6)
        label = Gtk.Label()
        label.set_markup('<i>\n\n%s\n\n</i>' % APP['license'])
        label.modify_font(Pango.FontDescription('Monospace 10'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_line_wrap(True)
        widget.pack_start(label, False, False, 6)
        linkbutton = Gtk.LinkButton(uri='http://t00mlabs.net', label='t00mlabs.net')
        widget.pack_start(linkbutton, False, False, 6)
        label = Gtk.Label()
        label.set_markup(APP['copyright'])
        label.modify_font(Pango.FontDescription('Monospace 10'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_line_wrap(True)
        widget.pack_start(label, False, False, 6)
        label = Gtk.Label()
        label.set_markup('\n%s' % escape(APP['authors'][0]))
        label.modify_font(Pango.FontDescription('Monospace 10'))
        label.set_justify(Gtk.Justification.CENTER)
        label.set_line_wrap(True)
        label.set_selectable(True)
        widget.pack_start(label, False, False, 6)
        self.add(viewport)
        self.show_all()