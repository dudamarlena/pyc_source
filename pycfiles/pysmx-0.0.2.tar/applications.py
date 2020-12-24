# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvttestapp2/applications.py
# Compiled at: 2010-05-30 09:35:01
from os import path
from beaker.middleware import SessionMiddleware
from paste.registry import RegistryManager
from paste.cascade import Cascade
from pysmvt import config, settings
from pysmvt.application import Application, WSGIApplication
from pysmvt import routing
from werkzeug import SharedDataMiddleware, DebuggedApplication
import settings as settingsmod

def make_wsgi(profile='Default', **kwargs):
    config.appinit(settingsmod, profile, **kwargs)
    app = WSGIApplication()
    app = SessionMiddleware(app, **dict(settings.beaker))
    app = RegistryManager(app)
    for appname in config.appslist(reverse=True):
        app_py_mod = __import__(appname)
        fs_static_path = path.join(path.dirname(app_py_mod.__file__), 'static')
        static_map = {routing.add_prefix('/'): fs_static_path}
        app = SharedDataMiddleware(app, static_map)

    if settings.debugger.enabled:
        app = DebuggedApplication(app, evalex=settings.debugger.interactive)
    return app


def make_console(profile='Default', **kwargs):
    config.appinit(settingsmod, profile, **kwargs)
    return Application()