# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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