# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\maproxy\proxyserver.py
# Compiled at: 2014-07-01 22:58:09
import tornado, tornado.tcpserver, maproxy.session

class ProxyServer(tornado.tcpserver.TCPServer):
    """
    TCP Proxy Server .

    """

    def __init__(self, target_server, target_port, client_ssl_options=None, server_ssl_options=None, session_factory=maproxy.session.SessionFactory(), *args, **kwargs):
        """
        ProxyServer initializer functin (constructor) .
        Input Parameters:
            target_server           : the proxied-server IP
            target_port             : the proxied-server port
            client_ssl_options      : Configure this proxy as SSL terminator  (decrypt all data).
                                      Standard Tornado's SSL options dictionary
                                      (e.g.: keyfile and certfile to specify Server-Certificate)
            server_ssl_options      : Encrypt all outgoing data with SSL. this variables has 3 options:
                                      1. True:       enable SSL . default settings
                                      2. False/None: disalbe SSL
                                      3. Standard Tornado's SSL options dictionary
                                         (e.g.: keyfile and certfile to specify Client-Certificate)
            args,kwargs             : will be passed directly to the Tornado engine
        """
        assert (
         session_factory, issubclass(session_factory.__class__, maproxy.session.SessionFactory))
        self.session_factory = session_factory
        self.target_server = target_server
        self.target_port = target_port
        self.client_ssl_options = client_ssl_options
        self.server_ssl_options = server_ssl_options
        if self.server_ssl_options is True:
            self.server_ssl_options = {}
        if self.server_ssl_options is False:
            self.server_ssl_options = None
        if self.client_ssl_options is False:
            self.client_ssl_options = None
        self.SessionsList = []
        super(ProxyServer, self).__init__(ssl_options=self.client_ssl_options, *args, **kwargs)
        return

    def handle_stream(self, stream, address):
        """
        The proxy will call this function for every new connection as a callback
        This is the Session starting point: we initiate a new session and add it to the sessions-list
        """
        assert isinstance(stream, tornado.iostream.IOStream)
        session = self.session_factory.new()
        session.new_connection(stream, address, self)
        self.SessionsList.append(session)

    def remove_session(self, session):
        assert isinstance(session, maproxy.session.Session)
        assert session.p2s_state == maproxy.session.Session.State.CLOSED
        assert session.c2p_state == maproxy.session.Session.State.CLOSED
        self.SessionsList.remove(session)
        self.session_factory.delete(session)

    def get_connections_count(self):
        return len(self.SessionsList)