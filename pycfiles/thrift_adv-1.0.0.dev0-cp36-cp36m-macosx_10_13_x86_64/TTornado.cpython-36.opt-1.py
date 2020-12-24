# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/TTornado.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 6407 bytes
from __future__ import absolute_import
import logging, socket, struct
from .transport.TTransport import TTransportException, TTransportBase, TMemoryBuffer
from io import BytesIO
from collections import deque
from contextlib import contextmanager
from tornado import gen, iostream, ioloop, tcpserver, concurrent
__all__ = [
 'TTornadoServer', 'TTornadoStreamTransport']
logger = logging.getLogger(__name__)

class _Lock(object):

    def __init__(self):
        self._waiters = deque()

    def acquired(self):
        return len(self._waiters) > 0

    @gen.coroutine
    def acquire(self):
        blocker = self._waiters[(-1)] if self.acquired() else None
        future = concurrent.Future()
        self._waiters.append(future)
        if blocker:
            yield blocker
        raise gen.Return(self._lock_context())

    def release(self):
        assert self.acquired(), 'Lock not aquired'
        future = self._waiters.popleft()
        future.set_result(None)

    @contextmanager
    def _lock_context(self):
        try:
            yield
        finally:
            self.release()


class TTornadoStreamTransport(TTransportBase):
    __doc__ = 'a framed, buffered transport over a Tornado stream'

    def __init__(self, host, port, stream=None, io_loop=None):
        self.host = host
        self.port = port
        self.io_loop = io_loop or ioloop.IOLoop.current()
        self._TTornadoStreamTransport__wbuf = BytesIO()
        self._read_lock = _Lock()
        self.stream = stream

    def with_timeout(self, timeout, future):
        return gen.with_timeout(timeout, future, self.io_loop)

    @gen.coroutine
    def open(self, timeout=None):
        logger.debug('socket connecting')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = iostream.IOStream(sock)
        try:
            connect = self.stream.connect((self.host, self.port))
            if timeout is not None:
                yield self.with_timeout(timeout, connect)
            else:
                yield connect
        except (socket.error, IOError, ioloop.TimeoutError) as e:
            message = 'could not connect to {}:{} ({})'.format(self.host, self.port, e)
            raise TTransportException(type=(TTransportException.NOT_OPEN),
              message=message)

        raise gen.Return(self)

    def set_close_callback(self, callback):
        """
        Should be called only after open() returns
        """
        self.stream.set_close_callback(callback)

    def close(self):
        self.stream.set_close_callback(None)
        self.stream.close()

    def read(self, _):
        assert False, "you're doing it wrong"

    @contextmanager
    def io_exception_context(self):
        try:
            yield
        except (socket.error, IOError) as e:
            raise TTransportException(type=(TTransportException.END_OF_FILE),
              message=(str(e)))
        except iostream.StreamBufferFullError as e:
            raise TTransportException(type=(TTransportException.UNKNOWN),
              message=(str(e)))

    @gen.coroutine
    def readFrame(self):
        with (yield self._read_lock.acquire()):
            with self.io_exception_context():
                frame_header = yield self.stream.read_bytes(4)
                if len(frame_header) == 0:
                    raise iostream.StreamClosedError('Read zero bytes from stream')
                frame_length, = struct.unpack('!i', frame_header)
                frame = yield self.stream.read_bytes(frame_length)
                raise gen.Return(frame)

    def write(self, buf):
        self._TTornadoStreamTransport__wbuf.write(buf)

    def flush(self):
        frame = self._TTornadoStreamTransport__wbuf.getvalue()
        frame_length = struct.pack('!i', len(frame))
        self._TTornadoStreamTransport__wbuf = BytesIO()
        with self.io_exception_context():
            return self.stream.write(frame_length + frame)


class TTornadoServer(tcpserver.TCPServer):

    def __init__(self, processor, iprot_factory, oprot_factory=None, *args, **kwargs):
        (super(TTornadoServer, self).__init__)(*args, **kwargs)
        self._processor = processor
        self._iprot_factory = iprot_factory
        self._oprot_factory = oprot_factory if oprot_factory is not None else iprot_factory

    @gen.coroutine
    def handle_stream(self, stream, address):
        host, port = address[:2]
        trans = TTornadoStreamTransport(host=host, port=port, stream=stream, io_loop=(self.io_loop))
        oprot = self._oprot_factory.getProtocol(trans)
        try:
            while not trans.stream.closed():
                try:
                    frame = yield trans.readFrame()
                except TTransportException as e:
                    if e.type == TTransportException.END_OF_FILE:
                        break
                    else:
                        raise

                tr = TMemoryBuffer(frame)
                iprot = self._iprot_factory.getProtocol(tr)
                yield self._processor.process(iprot, oprot)

        except Exception:
            logger.exception('thrift exception in handle_stream')
            trans.close()

        logger.info('client disconnected %s:%d', host, port)