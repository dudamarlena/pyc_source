# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/stub.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Stub', 'Refer']
__authors__ = ['Tim Chow']
import inspect, socket, traceback, logging, threading
from .transport import *
from .serializer import *
from .cluster import *
from .protocol import Protocol
from .helper import *
from .decorator import *
from .connection import *
from .request import Request
from .result import Result
from .exception import *
from .heartbeat import *
from .refer_argument import ReferArgument
LOGGER = logging.getLogger(__name__)

class Stub(object):

    def __init__(self):
        self._transport = BlockingRecordTransport()
        self._serializer = PickleSerializer()
        self._cluster = None
        self._protocol = None
        return

    def set_transport(self, transport):
        if not isinstance(transport, Transport):
            raise TypeError('expect Transport, not %s' % type(transport).__name__)
        self._transport = transport
        return self

    def set_serializer(self, serializer):
        if not isinstance(serializer, Serializer):
            raise TypeError('expect Serializer, not %s' % type(serializer).__name__)
        self._serializer = serializer
        return self

    def set_cluster(self, cluster):
        if not isinstance(cluster, Cluster):
            raise TypeError('expect Cluster, not %s' % type(cluster).__name__)
        self._cluster = cluster
        return self

    def set_protocol(self, protocol):
        if not isinstance(protocol, Protocol):
            raise TypeError('expect Protocol, not %s' % type(Protocol).__name__)
        self._protocol = protocol
        return self

    def refer(self, class_object, refer_argument=None):
        if self._cluster is None:
            raise RuntimeError('cluster must be provided')
        if not inspect.isclass(class_object):
            raise TypeError('expect class, not %s' % type(class_object).__name__)
        if refer_argument is None:
            refer_argument = ReferArgument()
        if refer_argument.protocol is None and self._protocol is None:
            raise RuntimeError('protocol must be provided')
        return Refer(class_object, self._transport, self._serializer, self._cluster, self.heartbeat_func, refer_argument.protocol or self._protocol, refer_argument)

    def close(self):
        if self._cluster is not None:
            self._cluster.close()
            self._cluster = None
        return

    def heartbeat_func(self):
        class_name = HeartBeatRequest.__name__
        export = get_export(HeartBeatRequest)
        if export is not None:
            class_name = export['name']
        method_name = 'send'
        provide = get_provide(HeartBeatRequest.send)
        if provide is not None:
            if provide['filtered']:
                raise RuntimeError('HeartBeatRequest.send is filtered')
            method_name = provide['name']
        request = Request()
        request.class_name = class_name
        request.method_name = method_name
        request.args = tuple()
        request.kwargs = dict()
        request.meta = tuple()
        return self._serializer.dumps(request)


class Refer(object):

    def __init__(self, class_object, transport, serializer, cluster, heartbeat_func, protocol, refer_argument):
        self._class_object = class_object
        self._transport = transport
        self._serializer = serializer
        self._cluster = cluster
        self._heartbeat_func = heartbeat_func
        self._protocol = protocol
        self._refer_argument = refer_argument
        self._connection_pool_lock = threading.RLock()
        self._connection_pool = LRUCache(refer_argument.connection_pool_size)

    def make_connection(self, remote):
        with self._connection_pool_lock:
            if remote in self._connection_pool:
                connection = self._connection_pool[remote]
                if not connection.closed and not connection.stopping:
                    return connection
                del self._connection_pool[remote]
            sock = ClientSocketBuilder().with_host(remote[0]).with_port(remote[1]).with_tcp_nodelay().with_blocking().with_timeout(self._refer_argument.client_socket_timeout).build()
            connection = BlockingConnection(sock, self._transport, self._refer_argument.max_pending_writes, self._refer_argument.max_pending_reads, self._refer_argument.max_pooling_reads, self._refer_argument.write_timeout, self._refer_argument.heartbeat_interval, self._heartbeat_func)
            entry = self._connection_pool.will_be_kicked_out()
            if entry is not None:
                entry.value.close()
                LOGGER.info('closing kicked-out connection: ("%s": %d)' % entry.key)
            self._connection_pool[remote] = connection
            return connection
        return

    def __getattr__(self, attr_name):
        attr = getattr(self._class_object, attr_name, None)
        if attr is None:
            raise AttributeError('instance of %s has no attribute: %s' % (
             self._class_object.__name__, attr_name))
        if not inspect.ismethod(attr):
            return attr
        else:
            return self._dynamic_proxy(attr, attr_name)

    def _dynamic_proxy(self, method, method_name):
        class_name = self._class_object.__name__
        export = get_export(self._class_object)
        if export is not None:
            class_name = export['name']
        provide = get_provide(method)
        if provide is not None:
            if provide['filtered']:
                raise RuntimeError('method %s.%s is not exported' % (
                 class_name, attr_name))
            method_name = provide['name']

        def get_connection():
            remote = self._cluster.get_remote(class_name, method_name, self._transport.get_name(), self._serializer.get_name())
            if remote is None:
                raise NoRemoteServerError('there is no remote server')
            return self.make_connection(remote)

        def _inner(*args, **kwargs):
            request = Request()
            request.class_name = class_name
            request.method_name = method_name
            request.args = args
            request.kwargs = kwargs
            connection = get_connection()
            return self._protocol.invoke(request, connection, self._serializer, self._refer_argument.write_timeout, self._refer_argument.read_timeout)

        return _inner

    def __iter_connections(self):
        head = self._connection_pool.head
        entry = head.prev
        while entry is not head:
            yield (
             entry.key, entry.value)
            entry = entry.prev

    def refer_close(self):
        for remote, connection in self.__iter_connections():
            connection.close()
            LOGGER.info('closed connection to ("%s", %d)' % remote)