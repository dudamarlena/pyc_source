# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pastegevent/server.py
# Compiled at: 2010-02-14 16:54:54
"""Entry point for PasteDeploy."""
from gevent import reinit
from gevent.wsgi import WSGIServer
from gevent.monkey import patch_all
__all__ = [
 'server_factory',
 'server_factory_patched']

def server_factory(global_conf, host, port):
    port = int(port)

    def serve(app):
        reinit()
        WSGIServer((host, port), app).serve_forever()

    return serve


def server_factory_patched(global_conf, host, port):
    port = int(port)

    def serve(app):
        reinit()
        patch_all(dns=False)
        WSGIServer((host, port), app).serve_forever()

    return serve