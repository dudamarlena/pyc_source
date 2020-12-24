# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/waitress_.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 639 bytes
"""The recommended development HTTP server."""
from __future__ import unicode_literals, print_function
try:
    from waitress import serve as serve_
except ImportError:
    print("You must install the 'waitress' package.")
    raise
else:

    def serve(application, host='127.0.0.1', port=8080, threads=4, **kw):
        """The recommended development HTTP server.
        
        Note that this server performs additional buffering and will not honour chunked encoding breaks.
        """
        serve_(application, host=host, port=int(port), threads=int(threads), **kw)