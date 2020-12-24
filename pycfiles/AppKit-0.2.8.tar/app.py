# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nitipit/space/project/tinyhtml/venv/lib/python2.7/site-packages/appkit/app.py
# Compiled at: 2014-04-23 04:10:26
from __future__ import print_function, unicode_literals
from gi.repository import Gtk, Gdk, WebKit
import sys, os, multiprocessing
from flask import Flask
import socket
from urllib2 import urlopen, HTTPError, URLError

class App(Gtk.Application):
    """App
    Application class
    """

    def __init__(self, module=None):
        Gtk.Application.__init__(self)
        self.server = Flask(module)
        self.route = self.server.route
        self.root_dir = os.path.abspath(os.path.dirname(module))

    def do_startup(self):
        """Gtk.Application.run() will call this function()"""
        Gtk.Application.do_startup(self)
        gtk_window = Gtk.ApplicationWindow(application=self)
        gtk_window.set_title(b'AppKit')
        webkit_web_view = WebKit.WebView()
        webkit_web_view.load_uri(b'http://localhost:' + str(self.port))
        screen = Gdk.Screen.get_default()
        monitor_geometry = screen.get_primary_monitor()
        monitor_geometry = screen.get_monitor_geometry(monitor_geometry)
        settings = webkit_web_view.get_settings()
        settings.set_property(b'enable-universal-access-from-file-uris', True)
        settings.set_property(b'enable-file-access-from-file-uris', True)
        settings.set_property(b'default-encoding', b'utf-8')
        gtk_window.set_default_size(monitor_geometry.width * 1.0 / 2.0, monitor_geometry.height * 3.0 / 5.0)
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        gtk_window.add(scrollWindow)
        gtk_window.connect(b'delete-event', self._on_gtk_window_destroy)
        gtk_window.show_all()
        webkit_web_view.connect(b'notify::title', self._on_notify_title)
        self.gtk_window = gtk_window
        self.webkit_web_view = webkit_web_view

    def do_activate(self):
        """Gtk.Application.run() will call this function()
        after do_startup()
        """
        pass

    def _on_gtk_window_destroy(self, window, *args, **kwargs):
        self.server_process.terminate()

    def _on_notify_title(self, webkit_web_view, g_param_string, *args, **kwargs):
        print(b'on_notify_title')
        title = webkit_web_view.get_title()
        if title is not None:
            self.gtk_window.set_title(title)
        return

    def _run_server(self, publish=False, port=None, debug=False):
        if port is None:
            sock = socket.socket()
            sock.bind(('localhost', 0))
            port = sock.getsockname()[1]
            sock.close()
        if publish:
            host = b'0.0.0.0'
        else:
            host = b'localhost'
        process = multiprocessing.Process(target=self.server.run, args=(
         host, port, debug), kwargs={b'use_reloader': False})
        process.start()
        return (process, port)

    def _check_server(self, port=None):
        port = str(port)
        while True:
            try:
                urlopen(b'http://localhost:' + port)
                break
            except HTTPError as e:
                print(e)
                break
            except URLError as e:
                pass

    def run(self, publish=False, port=None, debug=False, *args, **kw):
        self.server_process, self.port = self._run_server(publish=publish, port=port, debug=debug)
        self._check_server(port=self.port)
        exit_status = super(App, self).run(sys.argv)
        sys.exit(exit_status)