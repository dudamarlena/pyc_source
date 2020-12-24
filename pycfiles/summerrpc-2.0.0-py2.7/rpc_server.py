# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/rpc_server.py
# Compiled at: 2018-08-01 16:34:15
__all__ = [
 'RpcServerBuilder', 'RpcServer', 'Runner']
__authors__ = ['Tim Chow']
from .rpc_server_imports import *
LOGGER = logging.getLogger(__name__)
_EWOULDBLOCK = (socket.errno.EAGAIN, socket.errno.EWOULDBLOCK)

class RpcServerBuilder(object):

    def __init__(self):
        self._server_socket = None
        self._exporter = None
        self._transport = RecordTransport()
        self._serializer = PickleSerializer()
        self._max_connections = 15000
        self._concurrent_request_per_connection = 10
        self._max_buffer_size = 104857600
        self._ioloop = IOLoop.current()
        self._thread_pool_size = 2 * multiprocessing.cpu_count() + 1
        self._process_pool_size = None
        self._max_idle_time = 28800
        self._registry = None
        return

    def with_server_socket(self, server_socket):
        if not isinstance(server_socket, ServerSocket):
            raise TypeError('expect ServerSocket, not %s' % type(server_socket).__name__)
        if server_socket.gettimeout() != 0.0:
            raise RuntimeError('server_socket must be non-blocking')
        self._server_socket = server_socket
        return self

    def with_exporter(self, exporter):
        if not isinstance(exporter, Exporter):
            raise TypeError('expect Exporter, not %s' % type(exporter).__name__)
        self._exporter = exporter
        return self

    def with_transport(self, transport):
        if not isinstance(transport, Transport):
            raise TypeError('expect Transport, not %s' % type(transport).__name__)
        self._transport = transport
        return self

    def with_serializer(self, serializer):
        if not isinstance(serializer, Serializer):
            raise TypeError('expect Serializer, not %s' % type(serializer).__name__)
        self._serializer = serializer
        return self

    def with_max_connections(self, max_connections):
        if not isinstance(max_connections, int):
            raise TypeError('expect int, not %s' % type(max_connections).__name__)
        if max_connections <= 0:
            raise ValueError('max_connections should be more than 0')
        self._max_connections = max_connections
        return self

    def with_concurrent_request_per_connection(self, crpc):
        if not isinstance(crpc, int):
            raise TypeError('expect int, not %s' % type(crpc).__name__)
        if crpc <= 0:
            raise ValueError('concurrent_request_per_connection should be more than 0')
        self._concurrent_request_per_connection = crpc
        return self

    def with_max_buffer_size(self, max_buffer_size):
        if not isinstance(max_buffer_size, int):
            raise TypeError('expect int, not %s' % type(max_buffer_size).__name__)
        if max_buffer_size <= 0:
            raise ValueError('max_buffer_size should be more than 0')
        self._max_buffer_size = max_buffer_size
        return self

    def with_ioloop(self, ioloop):
        if not isinstance(ioloop, IOLoop):
            raise TypeError('expect IOLoop, not %s' % type(ioloop).__name__)
        self._ioloop = ioloop
        return self

    def with_thread_pool_size(self, size):
        if not isinstance(size, (int, types.NoneType)):
            raise TypeError('expect int or None, not %s' % type(size).__name__)
        if size is not None and size <= 0:
            raise ValueError('thread_pool_size should be more than 0')
        self._thread_pool_size = size
        return self

    def with_process_pool_size(self, size):
        if not isinstance(size, int):
            raise TypeError('expect int, not %s' % type(size).__name__)
        if size <= 0:
            raise ValueError('process_pool_size should be more than 0')
        self._process_pool_size = size
        return self

    def with_max_idle_time(self, max_idle_time):
        if not isinstance(max_idle_time, int):
            raise TypeError('expect int, not %s' % type(max_idle_time).__name__)
        if max_idle_time <= 0:
            raise ValueError('max_idle_time should be more than 0')
        self._max_idle_time = max_idle_time
        return self

    def with_registry(self, registry):
        if not isinstance(registry, Registry):
            raise TypeError('expect Registry, not %s' % type(registry).__name__)
        self._registry = registry
        return self

    @property
    def server_socket(self):
        return self._server_socket

    @property
    def exporter(self):
        return self._exporter

    @property
    def transport(self):
        return self._transport

    @property
    def serializer(self):
        return self._serializer

    @property
    def max_connections(self):
        return self._max_connections

    @property
    def concurrent_request_per_connection(self):
        return self._concurrent_request_per_connection

    @property
    def max_buffer_size(self):
        return self._max_buffer_size

    @property
    def ioloop(self):
        return self._ioloop

    @property
    def thread_pool_size(self):
        return self._thread_pool_size

    @property
    def process_pool_size(self):
        return self._process_pool_size

    @property
    def max_idle_time(self):
        return self._max_idle_time

    @property
    def registry(self):
        return self._registry

    def build(self):
        if self.server_socket is None or self.exporter is None:
            raise RuntimeError('server socket and exporter must be provided')
        return RpcServer(self.max_connections, self.max_buffer_size, self.ioloop, self.server_socket, self.thread_pool_size, self.process_pool_size, self.transport, self.serializer, self.exporter, self.concurrent_request_per_connection, self.max_idle_time, self.registry)


class RpcServer(object):

    def __init__(self, max_connections, max_buffer_size, ioloop, server_socket, thread_pool_size, process_pool_size, transport, serializer, exporter, concurrent_request_per_connection, max_idle_time, registry):
        self._max_connections = max_connections
        self._max_buffer_size = max_buffer_size
        self._ioloop = ioloop
        self._server_socket = server_socket
        self._thread_pool_size = thread_pool_size
        self._process_pool_size = process_pool_size
        self._transport = transport
        self._serializer = serializer
        self._exporter = exporter
        self._concurrent_request_per_connection = concurrent_request_per_connection
        self._max_idle_time = max_idle_time
        self._lru_cache = LRUCache(max_connections)
        self._started = False
        self._start_lock = threading.Lock()
        self._closed = False
        self._close_lock = threading.Lock()
        self._current_connections = 0
        self._thread_pool = None
        self._process_pool = None
        self._registry = registry
        return

    @property
    def started(self):
        return self._started

    @property
    def closed(self):
        return self._closed

    def _on_connection_close(self, fd, addr):
        LOGGER.debug('disconnect from: %s' % str(addr))
        self._current_connections = max(self._current_connections - 1, 0)
        LOGGER.debug('current connections: %d' % self._current_connections)
        if fd in self._lru_cache:
            LOGGER.debug('remove fd: %d from lru cache' % fd)
            del self._lru_cache[fd]

    def _accept_connection(self, server_socket, ioloop, fd, events):
        while True:
            if self._current_connections >= self._max_connections:
                logger.info('max connections reached, current connections: %d' % self._current_connections)
                return
            try:
                sock, addr = server_socket.accept()
            except socket.error as ex:
                if ex.errno in _EWOULDBLOCK:
                    break
                raise
            else:
                sock.setblocking(False)
                self._current_connections = self._current_connections + 1
                stream = IOStream(sock, max_buffer_size=self._max_buffer_size)
                fd = sock.fileno()
                stream.set_close_callback(partial(self._on_connection_close, fd, addr))
                self._lru_cache[fd] = [stream, self._ioloop.time()]
                Runner(stream, sock, addr, self._transport, self._serializer, self._exporter, self._thread_pool, self._process_pool, self._ioloop, self._concurrent_request_per_connection, self._lru_cache)

    def _close_deactive_connections(self):
        u"""关闭不活跃连接"""
        entry = self._lru_cache.head.prev
        while entry is not self._lru_cache.head:
            current_time = self._ioloop.time()
            if current_time - entry.value[1] <= self._max_idle_time:
                break
            LOGGER.info('closing deactive connection: %d' % entry.key)
            if not entry.value[0].closed():
                entry.value[0].close()
            entry = entry.prev

        when = self._max_idle_time
        if entry is not self._lru_cache.head:
            when = entry.value[1] + self._max_idle_time - self._ioloop.time()
            when = max(when, 0)
            LOGGER.debug('invoke _close_deactive_connections after %f' % when)
        self._ioloop.call_later(when, self._close_deactive_connections)

    def _register_if_necessary(self):
        if self._registry is None:
            return
        else:
            host, port = self._server_socket.getsockname()
            res = RegisterEntrySet()
            for class_name, method_name, method in self._exporter.iter_method():
                url = URLBuilder().with_scheme(self._transport.get_name()).with_host(host).with_port(port).with_path('/%s/%s' % (class_name, method_name)).with_argument('serializer', self._serializer.get_name()).with_argument('max_connections', str(self._max_connections)).with_argument('max_idle_time', str(self._max_idle_time)).with_argument('max_buffer_size', str(self._max_buffer_size)).with_argument('concurrent_request_per_connection', str(self._concurrent_request_per_connection)).with_argument('thread_pool_size', str(self._thread_pool_size)).build(quote_url=True)
                res.with_entry(url, '{"pid":%d}' % os.getpid())

            self._registry.register(res)
            return

    def start(self):
        if self._closed:
            raise RuntimeError('%s already closed' % self.__class__.__name__)
        if self._started:
            return
        else:
            with self._start_lock:
                if self._started:
                    return
                self._started = True
            if self._thread_pool_size is not None and self._thread_pool is None:
                self._thread_pool = ThreadPoolExecutor(max_workers=self._thread_pool_size)
            if self._process_pool_size is not None and self._process_pool is None:
                self._process_pool = ProcessPoolExecutor(max_workers=self._process_pool_size)
            self._ioloop.add_handler(self._server_socket, partial(self._accept_connection, self._server_socket, self._ioloop), IOLoop.READ)
            self._ioloop.call_later(self._max_idle_time, self._close_deactive_connections)
            self._register_if_necessary()
            try:
                try:
                    self._ioloop.start()
                except BaseException:
                    traceback.print_exc()
                    self._close_if_necessary()

            finally:
                LOGGER.info('close all fds')
                self._ioloop.close(all_fds=True)

            return

    def close(self):
        self._close_if_necessary()

    def _close_if_necessary(self):
        if self._closed:
            return
        else:
            with self._close_lock:
                if self._closed:
                    return
                if self._registry is not None:
                    self._registry.close()
                    self._registry = None
                self._ioloop.stop()
                thread_pool = self._thread_pool
                self._thread_pool = None
                if thread_pool is not None:
                    thread_pool.shutdown()
                process_pool = self._process_pool
                self._process_pool = None
                if process_pool is not None:
                    process_pool.shutdown()
                self._closed = True
                self._started = False
            return


def WRAPPER(obj, method_name, *a, **kw):
    return getattr(obj, method_name)(*a, **kw)


class Runner(object):

    def __init__(self, stream, sock, addr, transport, serializer, exporter, thread_pool, process_pool, ioloop, concurrent_request_per_connection, lru_cache):
        LOGGER.debug('accept connection from: %s' % str(addr))
        self._stream = stream
        self._fd = sock.fileno()
        self._transport = transport
        self._serializer = serializer
        self._exporter = exporter
        self._thread_pool = thread_pool
        self._process_pool = process_pool
        self._ioloop = ioloop
        self._concurrent_request_per_connection = concurrent_request_per_connection
        self._current_concurrency = 0
        self._lru_cache = lru_cache
        self.run()

    @gen.coroutine
    def run(self):
        while not self._stream.closed():
            try:
                try:
                    tid, buff = yield self._transport.read(self._stream)
                    request = self._serializer.loads(buff)
                    if not isinstance(request, Request):
                        LOGGER.error('expect Request, not %s' % type(request).__name__)
                        self._stream.close()
                        break
                except UnsatisfiableReadError:
                    LOGGER.error('read operation unsatisfied')
                    self._stream.close()
                    break
                except StreamClosedError:
                    LOGGER.debug('stream was closed while reading')
                    break
                except DeserializationError:
                    LOGGER.error('deserialization error accurs:')
                    LOGGER.error(traceback.format_exc())
                    self._stream.close()
                    break

            finally:
                if self._fd in self._lru_cache:
                    self._lru_cache[self._fd][1] = self._ioloop.time()

            if self._current_concurrency >= self._concurrent_request_per_connection:
                future = Future()
                future.set_exception(MaxConcurrencyReachedError('max concurrency reached'))
                self._current_concurrency = self._current_concurrency + 1
                self._ioloop.add_future(future, partial(self._send_response, request.meta, tid))
                continue
            class_name = request.class_name
            method_name = request.method_name
            args = request.args
            kwargs = request.kwargs
            method = self._exporter.get_method(class_name, method_name)
            if method is None:
                msg = 'the requested method:(%s, %s) is not exported' % (
                 class_name, method_name)
                LOGGER.error(msg)
                future = Future()
                future.set_exception(LookupError(msg))
            elif gen.is_coroutine_function(method):
                future = method(*args, **kwargs)
            else:
                run_in_subprocess = get_run_in_subprocess(method)
                if run_in_subprocess is not None and run_in_subprocess and self._process_pool is not None:
                    try:
                        future = self._process_pool.submit(WRAPPER, self._exporter.get_object(class_name), method_name, *args, **kwargs)
                    except BaseException as ex:
                        LOGGER.error('submit task to process pool failed, because %s: %s' % (
                         ex.__class__.__name__, str(ex)))
                        future = Future()
                        future.set_exception(ex)

                elif self._thread_pool is not None:
                    future = self._thread_pool.submit(method, *args, **kwargs)
                else:
                    future = Future()
                    future.set_exception(ConcurrencyError('no thread pool is specified'))
            self._current_concurrency = self._current_concurrency + 1
            self._ioloop.add_future(future, partial(self._send_response, request.meta, tid))

        return

    @gen.coroutine
    def _send_response(self, meta, tid, future):
        result = Result()
        result.meta = meta
        try:
            result.result = future.result()
        except BaseException:
            result.exc = future.exception()

        try:
            try:
                buff = self._serializer.dumps(result)
                yield self._transport.write(self._stream, tid, buff)
            except SerializationError:
                LOGGER.error(traceback.format_exc())
            except StreamClosedError:
                LOGGER.debug('stream was close while writing')
            except StreamBufferFullError:
                LOGGER.error('stream buffer was full while writing')

        finally:
            self._current_concurrency = max(self._current_concurrency - 1, 0)
            if self._fd in self._lru_cache:
                self._lru_cache[self._fd][1] = self._ioloop.time()