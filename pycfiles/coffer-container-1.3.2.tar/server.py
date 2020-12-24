# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gordo/.virtualenvs/coffer/lib/python2.7/site-packages/coffer/server.py
# Compiled at: 2015-01-05 15:15:54
__doc__ = '\nThis module contains some utilities to quickly run a coffer server (that is,\nsending files)\n'
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