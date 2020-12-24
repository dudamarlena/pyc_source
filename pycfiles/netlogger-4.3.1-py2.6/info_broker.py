# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/info_broker.py
# Compiled at: 2010-09-29 19:35:32
"""
Information broker, server and client.
"""
__rcsid__ = '$Id: info_broker.py 26531 2010-09-29 23:35:31Z dang $'
__author__ = 'Dan Gunter'
import asynchat, asyncore, logging
from cPickle import dumps, loads
import socket
from struct import pack, unpack
import sys
from netlogger import dispatch
from netlogger import nlapi, nllog
from netlogger.parsers.base import NLSimpleParser
RECORD_DELIM = '\n'
QUERY_DELIM = '<EOF>'
MAX_BUF = 65536
FANIN_PORT = 14380
FANOUT_PORT = 15380

class DataServer(asyncore.dispatcher, nllog.DoesLogging):
    """Accept connections for streamed log data.
    """

    def __init__(self, port=FANIN_PORT):
        asyncore.dispatcher.__init__(self)
        nllog.DoesLogging.__init__(self)
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)


class InputServer(DataServer):
    """Accept incoming NetLogger data streams.
    """

    def set_output(self, outp):
        self.outp = outp

    def handle_accept(self):
        (channel, addr) = self.accept()
        ic = InputChannel(channel, self.outp)


class InputChannel(asynchat.async_chat, nllog.DoesLogging):
    """Process (NetLogger) data streams.
    """

    def __init__(self, sock, outp):
        asynchat.async_chat.__init__(self, sock)
        nllog.DoesLogging.__init__(self)
        if self._dbg:
            self._count = 0
        self.set_terminator(RECORD_DELIM)
        self.ibuf = []
        self.outp = outp

    def collect_incoming_data(self, data):
        self.ibuf.append(data)

    def found_terminator(self):
        buf = ('').join(self.ibuf)
        self.outp.put(buf)
        self.ibuf = []
        if self._dbg:
            self._count += 1
            self.log.debug('buf_read', count=self._count, size=len(buf), contents=buf)


class OutputServer(DataServer):
    """Accept incoming connections for data, and send
    all items to each connection.
    """

    def __init__(self, port=FANOUT_PORT):
        DataServer.__init__(self, port)
        self.dispatcher = dispatch.Dispatcher()
        self.dispatcher.set_prehandle(self.npickle)
        self.parser = NLSimpleParser()

    def handle_accept(self):
        """Accept a new connection.
        Create an output channel for it.
        """
        (channel, addr) = self.accept()
        handler = dispatch.EventPrefixMatchHandler()
        self.dispatcher.register(handler)
        handler._channel = OutputChannel(channel, handler, self.channel_closed)

    def channel_closed(self, channel):
        """Called by the channel when it closes so the parent
        can clean up its state for dispatching events.
        """
        self.dispatcher.remove(channel.handler)

    def put(self, buf):
        """Put a buffer of data into the queue.
        """
        record = self.parser.parseLine(buf, strip=False)
        self.dispatcher.dispatch(record)

    def npickle(self, record):
        """Pickle a record for network transmission.
        """
        bytes = dumps(record, 1)
        blen = pack('!i', len(bytes))
        return blen + bytes


class OutputChannel(asynchat.async_chat, nllog.DoesLogging):
    """Connection between client and information broker.
    Client first sends a filter, then starts
    getting matching data streamed back to it.
    """

    def __init__(self, sock, handler, on_close):
        """Constructor.

        :Parameters:
          sock - Socket for output
          handler - dispatch.EventPrefixMatchHandler, that still needs
                    the proper prefix set (has an empty one).
          on_close - Callable to invoke with self, on close of this channel
        """
        asynchat.async_chat.__init__(self, sock)
        nllog.DoesLogging.__init__(self)
        self.on_close = on_close
        self.handler = handler
        self.handler.set_method(self.write)
        self.headers = []
        self.set_terminator(QUERY_DELIM)
        if self._dbg:
            self._count = 0

    def collect_incoming_data(self, data):
        self.headers.append(data)

    def found_terminator(self):
        query = ('').join(self.headers)
        for prefix in query.split():
            self.handler.add_prefix(prefix)

        self.headers = []

    def write(self, buf):
        _blen = len(buf)
        while 1:
            r = self.send(buf)
            if r == len(buf):
                break
            buf = buf[r:]

        if self._dbg:
            self._count += 1
            self.log.debug('buf_write', size=_blen, count=self._count, channel__id=str(self))

    def handle_close(self):
        self.on_close(self)
        asynchat.async_chat.handle_close(self)


class Client(asyncore.dispatcher, nllog.DoesLogging):
    """Connect to OutputServer, send "queries" and
    route the results to a user-provided output stream.
    """

    def __init__(self, host, port, ostrm=None, query_text=''):
        nllog.DoesLogging.__init__(self)
        asyncore.dispatcher.__init__(self)
        self.ostrm = ostrm or sys.stdout
        self.addr = (host, port)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(self.addr)
        self.buffer = query_text + QUERY_DELIM
        self.output_buffer = ''
        (self.need_hdr, self.need_data) = (4, 0)
        (self.hdr_bytes, self.data_bytes) = ('', '')

    def handle_connect(self):
        pass

    def handle_error(self):
        raise

    def handle_close(self):
        self.close()

    def handle_read(self):
        """Read a header (4 bytes integer) plus data
        """
        if self._trace:
            self.log.trace('handle_read.start', need_hdr=self.need_hdr, need_data=self.need_data)
        if self.need_hdr > 0:
            buf = self.recv(self.need_hdr)
            if not buf:
                return
            self.hdr_bytes += buf
            self.need_hdr -= len(buf)
            if self.need_hdr == 0:
                self.need_data = unpack('!i', self.hdr_bytes)[0]
                if self._trace:
                    self.log.trace('handle_read.header', value=self.need_data)
                self.hdr_bytes = ''
            elif self._trace:
                self.log.trace('handle_read.partial_hdr', need_hdr=self.need_hdr)
        else:
            if self._trace:
                self.log.trace('handle_read.body.start', length=self.need_data)
            buf = self.recv(self.need_data)
            if not buf:
                return
            self.data_bytes += buf
            self.need_data -= len(buf)
            if self._trace:
                self.log.trace('handle_read.body.end', length=len(buf), remain=self.need_data)
            if self.need_data == 0:
                if self._trace:
                    self.log.trace('handle_read.write_bytes', value=self.data_bytes)
                self.ostrm.write(self.data_bytes)
                (self.need_data, self.data_bytes) = (0, '')
                self.need_hdr = 4

    def readable(self):
        if self._trace:
            self.log.trace('readable')
        return True

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


def run_clients():
    """Run all clients until stopped.
    """
    asyncore.loop()


class StreamConsumer(nllog.DoesLogging):
    """Act like an output stream, parsing the
    buffers and invoking a method with the results.
    """

    def __init__(self, result_fn, **result_kw):
        """Constructor.

        Args:
          - result_fn - Function to call, with data
          - result_kw - Additional info. to pass to result_fn().
        """
        self.result_fn = result_fn
        self._kw = result_kw
        nllog.DoesLogging.__init__(self)

    def write(self, buf):
        if not buf:
            return
        if self._trace:
            self.log.trace('write.buf.start', size=len(buf))
        record = loads(buf)
        self.result_fn(record, **self._kw)
        if self._trace:
            self.log.trace('write.buf.end', size=len(buf))


def run_server(input_listen_port, output_listen_port):
    output_server = OutputServer(output_listen_port)
    input_server = InputServer(input_listen_port)
    input_server.set_output(output_server)
    asyncore.loop()


def client_got_data(data):
    print 'client got event: %s' % data['event']


def run_client(host, port, expr):
    Client(host, port, query_text=expr, ostrm=sys.stderr)
    Client(host, port, query_text=expr, ostrm=StreamConsumer(client_got_data))
    run_clients()


def __test(mode, args):
    if mode == '-c':
        host, port = args[0], int(args[1])
        if len(args) > 1:
            expr = (' ').join(args[2:])
        else:
            expr = ''
        run_client(host, port, expr)
    elif mode == '-s':
        ports = (
         int(args[0]), int(args[1]))
        run_server(*ports)
    else:
        raise ValueError('bad mode')


if __name__ == '__main__':
    import logging
    nllog.get_root_logger().setLevel(logging.INFO)
    nllog.get_root_logger().addHandler(logging.StreamHandler())
    prog = sys.argv[0]
    try:
        mode = sys.argv[1]
        args = sys.argv[2:]
        __test(mode, args)
    except (IndexError, ValueError), Err:
        print 'server: %s -s input-listen-port output-listen-port' % prog
        print 'client: %s -c host port expr..' % prog