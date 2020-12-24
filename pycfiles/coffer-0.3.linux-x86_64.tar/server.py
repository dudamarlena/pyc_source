# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gordo/.virtualenvs/coffer/lib/python2.7/site-packages/coffer/server.py
# Compiled at: 2015-01-05 15:15:54
"""
This module contains some utilities to quickly run a coffer server (that is,
sending files)
"""
from gevent.wsgi import WSGIServer
import gevent.monkey
from webapp import create_app
from zeroconf_utils import announce

def serve(app):
    gevent.monkey.patch_all()
    if app.config['DEBUG']:
        from werkzeug.debug import DebuggedApplication
        app = DebuggedApplication(app)
    http_server = WSGIServer(('0.0.0.0', 0), app)
    http_server.start()
    return http_server


def send(filenames, conf):
    app = create_app(filenames)
    app.config.update(conf)
    http_server = serve(app)
    address, port = http_server.address
    announce(address, port)
    gevent.wait(count=1)