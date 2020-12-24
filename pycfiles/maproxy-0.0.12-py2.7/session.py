# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\maproxy\session.py
# Compiled at: 2014-07-01 22:59:07
import tornado, socket, maproxy.proxyserver

class Session(object):
    """
    The Session class if the heart of the system.
    - We create the session when  a client connects to the server (proxy). this connection is "c2p"
    - We create a connection to the server (p2s)
    - Each connection (c2p,p2s) has a state (Session.State) , can be CLOSED,CONNECTING,CONNECTED
    - Initially, when c2p is created we :
        - create the p-s connection
        - start read from c2p
    - Completion Routings:
        - on_XXX_done_read:
          When we get data from one side, we initiate a "start_write" to the other side .
          Exception: if the target is not connected yet, we queue the data so we can send it later
        - on_p2s_connected:
          When p2s is connected ,we start read from the server . 
          if queued data is available (data that was sent from the c2p) we initiate a "start_write" immediately
        - on_XXX_done_write:
          When we're done "sending" data , we check if there's more data to send in the queue. 
          if there is - we initiate another "start_write" with the queued data
        - on_XXX_close:
          When one side closes the connection, we either initiate a "start_close" on the other side, or (if already closed) - remove the session
    - I/O routings:
        - XXX_start_read: simply start read from the socket (we assume and validate that only one read goes at a time)
        - XXX_start_write: if currently writing , add data to queue. if not writing - perform io_write...
        
    

    """

    class LoggerOptions:
        """
        Logging options - which messages/notifications we would like to log...
        The logging is for development&maintenance. In production set all to False
        """
        LOG_SESSION_ID = True
        LOG_NEW_SESSION_OP = False
        LOG_READ_OP = False
        LOG_WRITE_OP = False
        LOG_CLOSE_OP = False
        LOG_CONNECT_OP = False
        LOG_REMOVE_SESSION = False

    class State:
        """
        Each socket has a state.
        We will use the state to identify whether the connection is open or closed
        """
        CLOSED, CONNECTING, CONNECTED = range(3)

    def __init__(self):
        pass

    def new_connection(self, stream, address, proxy):
        assert isinstance(proxy, maproxy.proxyserver.ProxyServer)
        assert isinstance(stream, tornado.iostream.IOStream)
        self.logger_nesting_level = 0
        if Session.LoggerOptions.LOG_NEW_SESSION_OP:
            self.log('New Session')
        self.proxy = proxy
        self.c2p_reading = False
        self.c2p_writing = False
        self.p2s_writing = False
        self.p2s_reading = False
        self.c2p_stream = stream
        self.c2p_address = address
        self.c2p_state = Session.State.CONNECTED
        self.c2s_queued_data = []
        self.s2c_queued_data = []
        self.c2p_stream.set_nodelay(True)
        self.c2p_stream.set_close_callback(self.on_c2p_close)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        if self.proxy.server_ssl_options is not None:
            self.p2s_stream = tornado.iostream.SSLIOStream(s, ssl_options=self.proxy.server_ssl_options)
        else:
            self.p2s_stream = tornado.iostream.IOStream(s)
        self.p2s_stream.set_nodelay(True)
        self.p2s_stream.set_close_callback(self.on_p2s_close)
        self.p2s_state = self.p2s_state = Session.State.CONNECTING
        self.p2s_stream.connect((proxy.target_server, proxy.target_port), self.on_p2s_done_connect)
        self.c2p_start_read()
        return

    def log(self, msg):
        prefix = str(id(self)) + ':' if Session.LoggerOptions.LOG_SESSION_ID else ''
        prefix += self.logger_nesting_level * ' ' * 4
        logging.debug(prefix + msg)

    def logger(enabled=True):
        """
        We use this decorator to wrap functions and log the input/ouput of each function
        Since this decorator accepts a parameter, it must return an "inner" decorator....(Python stuff)
        """

        def inner_decorator(func):

            def log_wrapper(self, *args, **kwargs):
                msg = '%s (%s,%s)' % (func.__name__, args, kwargs)
                self.log(msg)
                self.logger_nesting_level += 1
                r = func(self, *args, **kwargs)
                self.logger_nesting_level -= 1
                self.log('%s -> %s' % (msg, str(r)))
                return r

            if enabled:
                return log_wrapper
            return func

        return inner_decorator

    @logger(LoggerOptions.LOG_READ_OP)
    def c2p_start_read(self):
        """
        Start read from client
        """
        assert not self.c2p_reading
        self.c2p_reading = True
        try:
            self.c2p_stream.read_until_close(lambda x: None, self.on_c2p_done_read)
        except tornado.iostream.StreamClosedError:
            self.c2p_reading = False

    @logger(LoggerOptions.LOG_READ_OP)
    def p2s_start_read(self):
        """
        Start read from server
        """
        assert not self.p2s_reading
        self.p2s_reading = True
        try:
            self.p2s_stream.read_until_close(lambda x: None, self.on_p2s_done_read)
        except tornado.iostream.StreamClosedError:
            self.p2s_reading = False

    @logger(LoggerOptions.LOG_READ_OP)
    def on_c2p_done_read(self, data):
        assert self.c2p_reading
        assert data
        self.p2s_start_write(data)

    @logger(LoggerOptions.LOG_READ_OP)
    def on_p2s_done_read(self, data):
        assert self.p2s_reading
        assert data
        self.c2p_start_write(data)

    @logger(LoggerOptions.LOG_WRITE_OP)
    def _c2p_io_write(self, data):
        if data is None:
            self.c2p_state = Session.State.CLOSED
            try:
                self.c2p_stream.close()
            except tornado.iostream.StreamClosedError:
                self.c2p_writing = False

        else:
            self.c2p_writing = True
            try:
                self.c2p_stream.write(data, callback=self.on_c2p_done_write)
            except tornado.iostream.StreamClosedError:
                self.c2p_writing = False

        return

    @logger(LoggerOptions.LOG_WRITE_OP)
    def _p2s_io_write(self, data):
        if data is None:
            self.p2s_state = Session.State.CLOSED
            try:
                self.p2s_stream.close()
            except tornado.iostream.StreamClosedError:
                self.p2s_writing = False

        else:
            self.p2s_writing = True
            try:
                self.p2s_stream.write(data, callback=self.on_p2s_done_write)
            except tornado.iostream.StreamClosedError:
                self.p2s_writing = False

        return

    @logger(LoggerOptions.LOG_WRITE_OP)
    def c2p_start_write(self, data):
        """
        Write to client.if there's a pending write-operation, add it to the S->C (s2c) queue
        """
        if self.c2p_state != Session.State.CONNECTED:
            return
        if not (self.c2p_writing or not self.s2c_queued_data):
            raise AssertionError
            self._c2p_io_write(data)
        else:
            self.s2c_queued_data.append(data)

    @logger(LoggerOptions.LOG_WRITE_OP)
    def p2s_start_write(self, data):
        """
        Write to the server.
        If not connected yet - queue the data
        If there's a pending write-operation , add it to the C->S (c2s) queue
        """
        if self.p2s_state == Session.State.CONNECTING:
            self.c2s_queued_data.append(data)
            return
        if self.p2s_state == Session.State.CLOSED:
            return
        if not self.p2s_state == Session.State.CONNECTED:
            raise AssertionError
            self.p2s_writing or self._p2s_io_write(data)
        else:
            self.c2s_queued_data.append(data)

    @logger(LoggerOptions.LOG_WRITE_OP)
    def on_c2p_done_write(self):
        """
        A start_write C->P  (write to client) is done .
        if there is queued-data to send - send it
        """
        assert self.c2p_writing
        if self.s2c_queued_data:
            self._c2p_io_write(self.s2c_queued_data.pop(0))
            return
        self.c2p_writing = False

    @logger(LoggerOptions.LOG_WRITE_OP)
    def on_p2s_done_write(self):
        """
        A start_write P->S  (write to server) is done .
        if there is queued-data to send - send it
        """
        assert self.p2s_writing
        if self.c2s_queued_data:
            self._p2s_io_write(self.c2s_queued_data.pop(0))
            return
        self.p2s_writing = False

    @logger(LoggerOptions.LOG_CLOSE_OP)
    def c2p_start_close(self, gracefully=True):
        """
        Close c->p connection
        if gracefully is True then we simply add None to the queue, and start a write-operation
        if gracefully is False then this is a "brutal" close:
            - mark the stream is closed
            - we "reset" (empty) the queued-data
            - if the other side (p->s) already closed, remove the session
        
        """
        if self.c2p_state == Session.State.CLOSED:
            return
        else:
            if gracefully:
                self.c2p_start_write(None)
                return
            self.c2p_state = Session.State.CLOSED
            self.s2c_queued_data = []
            self.c2p_stream.close()
            if self.p2s_state == Session.State.CLOSED:
                self.remove_session()
            return

    @logger(LoggerOptions.LOG_CLOSE_OP)
    def p2s_start_close(self, gracefully=True):
        """
        Close p->s connection
        if gracefully is True then we simply add None to the queue, and start a write-operation
        if gracefully is False then this is a "brutal" close:
            - mark the stream is closed
            - we "reset" (empty) the queued-data
            - if the other side (p->s) already closed, remove the session
        
        """
        if self.p2s_state == Session.State.CLOSED:
            return
        else:
            if gracefully:
                self.p2s_start_write(None)
                return
            self.p2s_state = Session.State.CLOSED
            self.c2s_queued_data = []
            self.p2s_stream.close()
            if self.c2p_state == Session.State.CLOSED:
                self.remove_session()
            return

    @logger(LoggerOptions.LOG_CLOSE_OP)
    def on_c2p_close(self):
        """
        Client closed the connection.
        we need to:
        1. update the c2p-state
        2. if there's no more data to the server (c2s_queued_data is empty) - we can close the p2s connection
        3. if p2s already closed - we can remove the session
        """
        self.c2p_state = Session.State.CLOSED
        if self.p2s_state == Session.State.CLOSED:
            self.remove_session()
        else:
            self.p2s_start_close(gracefully=True)

    @logger(LoggerOptions.LOG_CLOSE_OP)
    def on_p2s_close(self):
        """
        Server closed the connection.
        We need to update the satte, and if the client closed as well - delete the session
        """
        self.p2s_state = Session.State.CLOSED
        if self.c2p_state == Session.State.CLOSED:
            self.remove_session()
        else:
            self.c2p_start_close(gracefully=True)

    @logger(LoggerOptions.LOG_CONNECT_OP)
    def on_p2s_done_connect(self):
        assert self.p2s_state == Session.State.CONNECTING
        self.p2s_state = Session.State.CONNECTED
        self.p2s_start_read()
        assert not self.p2s_writing
        if self.c2s_queued_data:
            self.p2s_start_write(self.c2s_queued_data.pop(0))

    @logger(LoggerOptions.LOG_REMOVE_SESSION)
    def remove_session(self):
        self.proxy.remove_session(self)


class SessionFactory(object):
    """
    This is  the default session-factory. it simply returns a "Session" object
    """

    def __init__(self):
        pass

    def new(self, *args, **kwargs):
        """
        The caller needs a Session objet (constructed with *args,**kwargs).
        In this implementation we're simply creating a new object. you can enhance and create a pool or add logs..
        """
        return Session(*args, **kwargs)

    def delete(self, session):
        """
        Delete a session object
        """
        assert isinstance(session, Session)
        del session