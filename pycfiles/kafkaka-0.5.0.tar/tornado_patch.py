# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duwei/PycharmProjects/kafkaka/kafkaka/tornado_patch.py
# Compiled at: 2014-12-25 09:06:57
from itertools import chain
import logging, struct, socket
from time import sleep
from functools import partial
from kafkaka.client import KafkaClient
from kafkaka.conn import Connection
from kafkaka.define import DEFAULT_POOL_SIZE, KafkaError, ConnectionError
from tornado.iostream import IOStream
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger('kafka')

class Gen:

    def __init__(self):
        pass

    @staticmethod
    def task(func, *args, **kwargs):
        return partial(func, *args, **kwargs)

    @staticmethod
    def callback(g, response=None):
        try:
            f = g.send(response)
            if hasattr(f, '__call__'):
                f(partial(Gen.callback, g))
        except StopIteration:
            pass

    @staticmethod
    def async(func):

        def wrapper(*args, **kwargs):
            g = func(*args, **kwargs)
            try:
                f = g.send(None)
            except StopIteration:
                pass

            if hasattr(f, '__call__'):
                f(partial(Gen.callback, g))
            return

        return wrapper


gen = Gen()

class Connection(Connection):

    def __init__(self, pool=None, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self._pool = pool
        self._stream = None
        self._callbacks = []
        self._ready = False
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pool.release(self)

    def _add_callback(self, func):
        self._callbacks.append(func)

    def _do_callbacks(self):
        self._ready = True
        while 1:
            try:
                func = self._callbacks.pop()
                func()
            except IndexError:
                break
            except:
                continue

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self._sock = IOStream(s)
        self._sock.connect((self._host, self._port), self._do_callbacks)

    def send(self, payload, correlation_id=-1, callback=None):
        """
        :param payload: an encoded kafka packet
        :param correlation_id: for now, just for debug logging
        :return:
        """
        if not self._ready:

            def _callback(*args, **kwargs):
                self.send(payload, correlation_id, callback)

            self._add_callback(_callback)
            return
        else:
            log.debug('About to send %d bytes to Kafka, request %d' % (len(payload), correlation_id))
            if payload:
                _bytes = struct.pack('>i%ds' % len(payload), len(payload), payload)
            else:
                _bytes = struct.pack('>i', -1)
            try:
                self._sock.write(_bytes, callback)
            except:
                self.close()
                callback(None)
                self._log_and_raise('Unable to send payload to Kafka')

            return

    def _recv(self, size, callback):
        try:
            self._sock.read_bytes(min(size, 4096), callback)
        except:
            self.close()
            callback(None)
            self._log_and_raise('Unable to receive data from Kafka')

        return

    def recv(self, correlation_id=-1, callback=None):
        """

        :param correlation_id: for now, just for debug logging
        :return: kafka response packet
        """
        log.debug('Reading response %d from Kafka' % correlation_id)
        if not self._ready:

            def _callback():
                self.recv(correlation_id, callback)

            self._add_callback(_callback)
            return

        def get_size(resp):
            if resp == None:
                callback(None)
            size, = struct.unpack('>i', resp)
            self._recv(size, callback)
            return

        self._recv(4, get_size)

    def close(self):
        self._callbacks = []
        log.debug('Closing socket connection' + self._log_tail)
        if self._sock:
            self._sock.close()
            self._sock = None
        else:
            log.debug('Socket connection not exists' + self._log_tail)
        return

    def closed(self):
        return self._sock.closed()


class ConnectionPool(object):

    def __init__(self, connection_class=Connection, **connection_kwargs):
        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.reset()

    def __repr__(self):
        return '%s<%s%s>' % (
         type(self).__name__,
         self.connection_class.__name__,
         str(self.connection_kwargs))

    def __len__(self):
        return len(self._available_connections) + len(self._in_use_connections)

    def reset(self):
        self._created_connections = 0
        self._available_connections = []
        self._in_use_connections = set()

    def get_connection(self):
        """
        Get a connection from the pool
        :return: Connection object
        """
        try:
            c = self._available_connections.pop()
        except IndexError:
            c = self.connection_class(pool=self, **self.connection_kwargs)

        if c.closed():
            self.reset()
            return self.get_connection()
        self._in_use_connections.add(c)
        return c

    def release(self, connection):
        """
        Releases the connection back to the pool
        :param connection:
        :return:
        """
        if connection in self._in_use_connections:
            self._in_use_connections.remove(connection)
            self._available_connections.append(connection)

    def disconnect(self):
        """
        Disconnects all connections in the pool
        :return:
        """
        all_conns = chain(self._available_connections, self._in_use_connections)
        for connection in all_conns:
            connection.disconnect()


class KafkaClient(KafkaClient):

    def __init__(self, *args, **kwargs):
        self._pools = {}
        super(KafkaClient, self).__init__(*args, **kwargs)

    def _get_conn(self, host, port):
        """
        Get or create a connection using Pool
        :param host: host name
        :param port: port number
        :return: Connection
        """
        key = (
         host, port)
        if key not in self._pools:
            self._pools[key] = ConnectionPool(host=host, port=port)
        return self._pools[key].get_connection()

    @gen.async
    def boot_metadata(self, expected_topics, callback=None):
        """
        boot metadata from kafka server
        :param expected_topics: The topics to produce metadata for. If empty the request will yield metadata for all topics.
        :return:
        """
        correlation_id, _topics, request_bytes = self._pack_boot_metadata(expected_topics)
        for host, port in self.hosts * 3:
            try:
                with self._get_conn(host, port) as (conn):
                    yield gen.task(conn.send, request_bytes, correlation_id)
                    resp_bytes = yield gen.task(conn.recv, correlation_id)
                self._unpack_boot_metadata(resp_bytes, expected_topics, callback)
                return
            except KafkaError as e:
                log.warning('Kafka metadata via request [%r] from server %s:%i is not available, trying next server: %s' % (
                 correlation_id, host, port, e))
                sleep(1)
                continue
            except Exception as e:
                log.warning('Could not send request [%r] to server %s:%i, trying next server: %s' % (
                 correlation_id, host, port, e))
                continue

        raise KafkaError('All servers failed to process request')

    @gen.async
    def send_message(self, topic_name, *msg):
        if not self._ready:

            def _callback():
                self.send_message(topic_name, *msg)

            self._add_callback(_callback)
            return
        host, port, request_bytes, correlation_id = self._pack_send_message(topic_name, *msg)
        for i in xrange(self._retry_times):
            with self._get_conn(host, port) as (conn):
                try:
                    yield gen.task(conn.send, request_bytes, correlation_id)
                except ConnectionError as e:
                    log.warning('Could not send request [%r] to server %s:%i, try again, %s' % (correlation_id, host, port, e))
                    if i == self._retry_times - 1:
                        log.error('Could not send request [%r] to server %s:%i, %s' % (correlation_id, host, port, e))
                    continue

                try:
                    resp_bytes = yield gen.task(conn.recv, correlation_id)
                    self._unpack_send_message(resp_bytes)
                except ConnectionError as e:
                    log.error('Could not get response [%r] from server %s:%i, %s' % (correlation_id, host, port, e))
                except Exception as e:
                    log.error('Bad response [%r] from server %s:%i, %s' % (correlation_id, host, port, e))

            break


if __name__ == '__main__':
    pass