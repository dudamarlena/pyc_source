# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/widgets/wdg_browser.py
# Compiled at: 2019-03-13 14:44:54
# Size of source mod 2**32: 1486 bytes
"""
# File: browser.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Web browser module
"""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit

class BasicoBrowser(Gtk.VBox):

    def __init__(self, *args, **kwargs):
        (super(BasicoBrowser, self).__init__)(*args, **kwargs)
        self.webview = WebKit.WebView()
        settings = self.webview.get_settings()
        settings.set_property('enable-developer-extras', True)
        settings.set_property('enable-default-context-menu', True)
        settings.set_property('default-encoding', 'utf-8')
        settings.set_property('enable-private-browsing', True)
        settings.set_property('enable-html5-local-storage', True)
        settings.set_property('enable-plugins', True)
        self.webview.set_full_content_zoom(True)
        self.show()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.webview)
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        self.pack_start(scrolled_window, True, True, 0)
        scrolled_window.show_all()

    def load_url(self, url):
        self.webview.load_uri(url)