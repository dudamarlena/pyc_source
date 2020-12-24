# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/eventlet_.py
# Compiled at: 2016-04-25 13:24:08
# Size of source mod 2**32: 548 bytes
"""Eventlet-based WSGI server adapter."""
from __future__ import unicode_literals, print_function
from eventlet import listen
from eventlet.wsgi import server

def serve(application, host='127.0.0.1', port=8080):
    """Eventlet-based WSGI-HTTP server.
        
        For a more fully-featured Eventlet-capable interface, see also [Spawning](http://pypi.python.org/pypi/Spawning/).
        """
    server(listen(host, int(port)), application)