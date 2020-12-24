# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/gevent_.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 423 bytes
"""Gevent-based WSGI server adapter."""
from __future__ import unicode_literals, print_function
from gevent.pywsgi import WSGIServer

def serve(application, host='127.0.0.1', port=8080):
    """Gevent-based WSGI-HTTP server."""
    WSGIServer((host, int(port)), application).serve_forever()