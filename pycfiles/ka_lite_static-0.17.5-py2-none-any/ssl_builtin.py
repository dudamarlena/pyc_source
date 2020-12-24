# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/cherrypy/cherrypy/wsgiserver/ssl_builtin.py
# Compiled at: 2018-07-11 18:15:31
"""A library for integrating Python's builtin ``ssl`` library with CherryPy.

The ssl module must be importable for SSL functionality.

To use this module, set ``CherryPyWSGIServer.ssl_adapter`` to an instance of
``BuiltinSSLAdapter``.
"""
try:
    import ssl
except ImportError:
    ssl = None

try:
    from _pyio import DEFAULT_BUFFER_SIZE
except ImportError:
    try:
        from io import DEFAULT_BUFFER_SIZE
    except ImportError:
        DEFAULT_BUFFER_SIZE = -1

import sys
from cherrypy import wsgiserver

class BuiltinSSLAdapter(wsgiserver.SSLAdapter):
    """A wrapper for integrating Python's builtin ssl module with CherryPy."""
    certificate = None
    private_key = None

    def __init__(self, certificate, private_key, certificate_chain=None):
        if ssl is None:
            raise ImportError('You must install the ssl module to use HTTPS.')
        self.certificate = certificate
        self.private_key = private_key
        self.certificate_chain = certificate_chain
        return

    def bind(self, sock):
        """Wrap and return the given socket."""
        return sock

    def wrap(self, sock):
        """Wrap and return the given socket, plus WSGI environ entries."""
        try:
            s = ssl.wrap_socket(sock, do_handshake_on_connect=True, server_side=True, certfile=self.certificate, keyfile=self.private_key, ssl_version=ssl.PROTOCOL_SSLv23)
        except ssl.SSLError:
            e = sys.exc_info()[1]
            if e.errno == ssl.SSL_ERROR_EOF:
                return (
                 None, {})
            if e.errno == ssl.SSL_ERROR_SSL:
                if e.args[1].endswith('http request'):
                    raise wsgiserver.NoSSLError
                elif e.args[1].endswith('unknown protocol'):
                    return (
                     None, {})
            raise

        return (
         s, self.get_environ(s))

    def get_environ(self, sock):
        """Create WSGI environ entries to be merged into each request."""
        cipher = sock.cipher()
        ssl_environ = {'wsgi.url_scheme': 'https', 
           'HTTPS': 'on', 
           'SSL_PROTOCOL': cipher[1], 
           'SSL_CIPHER': cipher[0]}
        return ssl_environ

    if sys.version_info >= (3, 0):

        def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
            return wsgiserver.CP_makefile(sock, mode, bufsize)

    else:

        def makefile(self, sock, mode='r', bufsize=DEFAULT_BUFFER_SIZE):
            return wsgiserver.CP_fileobject(sock, mode, bufsize)