# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroClient.py
# Compiled at: 2009-07-07 11:29:42
"""
Python Remote Objects support - Client side.

"""
import socket, VisionEgg, logging, Pyro.core

class PyroClient:
    """Simplifies getting PyroControllers from a remote computer."""

    def __init__(self, server_hostname='', server_port=7766):
        """Initialize Pyro client."""
        Pyro.core.initClient()
        try:
            self.server_hostname = socket.getfqdn(server_hostname)
        except Exception, x:
            logger = logging.getLogger('VisionEgg.PyroClient')
            logger.warning('while getting fully qualified domain name: %s: %s' % (
             str(x.__class__), str(x)))
            self.server_hostname = server_hostname

        self.server_port = server_port

    def get(self, name):
        """Return a remote Pyro object being served by Pyro server."""
        URI = 'PYROLOC://%s:%d/%s' % (self.server_hostname, self.server_port, name)
        return Pyro.core.getProxyForURI(URI)