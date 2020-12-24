# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/requests-toolbelt/requests_toolbelt/adapters/socket_options.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 4789 bytes
"""The implementation of the SocketOptionsAdapter."""
import socket, warnings, sys, requests
from requests import adapters
from .._compat import connection
from .._compat import poolmanager
from .. import exceptions as exc

class SocketOptionsAdapter(adapters.HTTPAdapter):
    __doc__ = "An adapter for requests that allows users to specify socket options.\n\n    Since version 2.4.0 of requests, it is possible to specify a custom list\n    of socket options that need to be set before establishing the connection.\n\n    Example usage::\n\n        >>> import socket\n        >>> import requests\n        >>> from requests_toolbelt.adapters import socket_options\n        >>> s = requests.Session()\n        >>> opts = [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)]\n        >>> adapter = socket_options.SocketOptionsAdapter(socket_options=opts)\n        >>> s.mount('http://', adapter)\n\n    You can also take advantage of the list of default options on this class\n    to keep using the original options in addition to your custom options. In\n    that case, ``opts`` might look like::\n\n        >>> opts = socket_options.SocketOptionsAdapter.default_options + opts\n\n    "
    if connection is not None:
        default_options = getattr(connection.HTTPConnection, 'default_socket_options', [
         (
          socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)])
    else:
        default_options = []
        warnings.warn(exc.RequestsVersionTooOld, 'This version of Requests is only compatible with a version of urllib3 which is too old to support setting options on a socket. This adapter is functionally useless.')

    def __init__(self, **kwargs):
        self.socket_options = kwargs.pop('socket_options', self.default_options)
        (super(SocketOptionsAdapter, self).__init__)(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        if requests.__build__ >= 132096:
            self.poolmanager = poolmanager.PoolManager(num_pools=connections,
              maxsize=maxsize,
              block=block,
              socket_options=(self.socket_options))
        else:
            super(SocketOptionsAdapter, self).init_poolmanager(connections, maxsize, block)


class TCPKeepAliveAdapter(SocketOptionsAdapter):
    __doc__ = "An adapter for requests that turns on TCP Keep-Alive by default.\n\n    The adapter sets 4 socket options:\n\n    - ``SOL_SOCKET`` ``SO_KEEPALIVE`` - This turns on TCP Keep-Alive\n    - ``IPPROTO_TCP`` ``TCP_KEEPINTVL`` 20 - Sets the keep alive interval\n    - ``IPPROTO_TCP`` ``TCP_KEEPCNT`` 5 - Sets the number of keep alive probes\n    - ``IPPROTO_TCP`` ``TCP_KEEPIDLE`` 60 - Sets the keep alive time if the\n      socket library has the ``TCP_KEEPIDLE`` constant\n\n    The latter three can be overridden by keyword arguments (respectively):\n\n    - ``idle``\n    - ``interval``\n    - ``count``\n\n    You can use this adapter like so::\n\n       >>> from requests_toolbelt.adapters import socket_options\n       >>> tcp = socket_options.TCPKeepAliveAdapter(idle=120, interval=10)\n       >>> s = requests.Session()\n       >>> s.mount('http://', tcp)\n\n    "

    def __init__(self, **kwargs):
        socket_options = kwargs.pop('socket_options', SocketOptionsAdapter.default_options)
        idle = kwargs.pop('idle', 60)
        interval = kwargs.pop('interval', 20)
        count = kwargs.pop('count', 5)
        socket_options = socket_options + [
         (
          socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
        if getattr(socket, 'TCP_KEEPINTVL', None) is not None:
            socket_options += [
             (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL,
              interval)]
        else:
            if sys.platform == 'darwin':
                TCP_KEEPALIVE = getattr(socket, 'TCP_KEEPALIVE', 16)
                socket_options += [(socket.IPPROTO_TCP, TCP_KEEPALIVE, interval)]
        if getattr(socket, 'TCP_KEEPCNT', None) is not None:
            socket_options += [(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, count)]
        if getattr(socket, 'TCP_KEEPIDLE', None) is not None:
            socket_options += [(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, idle)]
        (super(TCPKeepAliveAdapter, self).__init__)(socket_options=socket_options, **kwargs)