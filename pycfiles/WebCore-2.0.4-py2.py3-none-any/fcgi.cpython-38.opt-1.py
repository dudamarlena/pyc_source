# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/fcgi.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 813 bytes
"""A production quality flup-based FastCGI server."""
from __future__ import unicode_literals, print_function
try:
    from flup.server.fcgi import WSGIServer
except ImportError:
    print("You must install a 'flup' package such as 'flup6' to use FastCGI support.")
    raise
else:

    def serve(application, host='127.0.0.1', port=8080, socket=None, **options):
        """Basic FastCGI support via flup.
        
        This web server has many, many options. Please see the Flup project documentation for details.
        """
        if not socket:
            bindAddress = (
             host, int(port))
        else:
            bindAddress = socket
        WSGIServer(application, bindAddress=bindAddress, **options).run()