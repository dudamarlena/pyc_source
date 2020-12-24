# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/beanstalk/_libeventconn.py
# Compiled at: 2015-07-11 09:52:37
import socket, sys, protohandler

class Command(object):

    def __init__(callback, command, handler):
        self.callback = callback
        self.comand = command
        self.handler = handler


class LibeventConn(object):
    """LibeventConn -- Like other connection types in pybeanstalk, is
    intended to only handle the beanstalk related connections. This connection
    works much the same as ServerConn, and its initialization variables are
    the same.

    The connection object also has a few special properties:
    result_callback -- callable object, must take at least one argument,
                       a response (or job if job is set and the protocol
                       interaction returns a job), which will be the default
                       callback.
    result_callback_args -- a tuple which will be passed as *args to the
                            result_callback when it is called
    error_callback -- a callable that takes 3 arguments, which are the
                      results of a sys.exc_info() call

    To use the protocol, it works just like the ServerConn, but each function
    takes extra keyword options, for the callbacks, which override the connection
    defaults (but otherwise work the same) above.

    NOTE: I haven't included the convenience of the tube and watchlist
    properties in this connection type because I am still unsure of the best
    way to handle them.
    """
    import event
    WAIT = 0
    IN_INTERACTION = 1
    MIN_TIME = 1e-07

    def __init__(self, server, port, job=None):
        self.server = server
        self.port = port
        self._make_socket()
        self.job = None
        self.phase = self.WAIT
        self.interaction = None
        self.phase = self.WAIT
        self.result_callback = None
        self.result_callback_args = ()
        self.error_callback = None
        self.__current_Callbacks = None
        return

    def _make_socket(self):
        self._socket = socket.socket(socket.AF_INET)
        self._socket.connect((self.server, self.port))

    def fileno(self):
        return self._socket.fileno()

    def __write(self, idata):
        line = idata['line']
        if 'sent' not in idata:
            idata['sent'] = 0
        idata['sent'] += self._socket.send(line[idata['sent']:])
        if idata['sent'] == len(line):
            self.event.read(self._socket, self.__read, idata)
            return
        else:
            return True
            return

    def __read(self, idata):
        ec = idata['callbacks'][1]
        try:
            handler = idata['handler']
            recv = self._socket.recv(handler.remaining)
            resp = handler(recv)
            if resp:
                self.phase = self.WAIT
                self.event.timeout(self.MIN_TIME, self.__callback, resp, idata)
                return
            return True
        except:
            ec(*sys.exc_info())

        return

    def __callback(self, response, idata):
        rc, ec, args = idata['callbacks']
        try:
            try:
                rc(response, *args)
            except:
                raise

        finally:
            self.__current_Callbacks = None

        return

    def _do_interaction(self, idata):
        self.phase = self.IN_INTERACTION
        self.event.write(self._socket, self.__write, idata)

    def _setup_callbacks(self, d):
        if 'result_callback' in d:
            rc = d.pop('result_callback')
            rca = d.pop('result_callback_args') if 'result_callback_args' in d else tuple()
        else:
            rc = self.result_callback
            rca = self.result_callback_args
        if 'error_callback' in d:
            ec = d.pop('error_callback')
        else:
            ec = self.error_callback
        if not (rc and ec):
            raise ConnectionError('Callbacks missing')
        return (
         rc, ec, rca)

    def __getattr__(self, attr):

        def caller(callback, *args, **kw):
            cmd = Command(callback, *getattr(protohandler, 'process_%s' % (attr,))(*args, **kw))
            return self._do_interaction(idata)

        return caller