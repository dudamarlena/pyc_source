# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duwei/PycharmProjects/kafkaka/kafkaka/conn.py
# Compiled at: 2014-12-25 02:04:44
import logging, socket, struct
from kafkaka.define import ConnectionError
from kafkaka.define import DEFAULT_KAFKA_PORT, DEFAULT_SOCKET_TIMEOUT_SECONDS
log = logging.getLogger('kafka')

class Connection(object):

    def __init__(self, host, port=DEFAULT_KAFKA_PORT, timeout=DEFAULT_SOCKET_TIMEOUT_SECONDS):
        self._sock = None
        self._closed = False
        self._host = host
        self._port = port
        self._timeout = timeout
        self._log_tail = ' @ %s:%d' % (self._host, self._port)
        try:
            self.connect()
        except socket.error as socket.timeout:
            self.close()
            self._log_and_raise('Unable to connect to kafka broker')

        return

    def connect(self):
        self._sock = socket.create_connection((self._host, self._port), self._timeout)

    def __repr__(self):
        return type(self).__name__ + ('<host={0},port={1}>').format(self._host, self._port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send(self, payload, correlation_id=-1):
        """
        :param payload: an encoded kafka packet
        :param correlation_id: for now, just for debug logging
        :return:
        """
        log.debug('About to send %d bytes to Kafka, request %d' % (len(payload), correlation_id))
        if payload:
            _bytes = struct.pack('>i%ds' % len(payload), len(payload), payload)
        else:
            _bytes = struct.pack('>i', -1)
        try:
            self._sock.sendall(_bytes)
        except socket.error as socket.timeout:
            self.close()
            self._log_and_raise('Unable to send payload to Kafka')

    def _recv(self, size):
        bytes_left = size
        responses = []
        log.debug('About to read %d bytes from Kafka broker', size)
        while bytes_left:
            try:
                data = self._sock.recv(min(bytes_left, 4096))
                assert data != ''
            except AssertionError:
                self.close()
                self._log_and_raise('Want to receive more, but server close the socket')
            except socket.error as socket.timeout:
                self.close()
                self._log_and_raise('Unable to receive data from Kafka')

            bytes_left -= len(data)
            log.debug('Read %d/%d bytes from Kafka', size - bytes_left, size)
            responses.append(data)

        return ('').join(responses)

    def recv(self, correlation_id=-1):
        """

        :param correlation_id: for now, just for debug logging
        :return: kafka response packet
        """
        log.debug('Reading response %d from Kafka' % correlation_id)
        resp = self._recv(4)
        size, = struct.unpack('>i', resp)
        resp = self._recv(size)
        return resp

    def close(self):
        log.debug('Closing socket connection' + self._log_tail)
        if self._sock:
            try:
                self._sock.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass

            self._closed = True
            self._sock.close()
            self._sock = None
        else:
            log.debug('Socket connection not exists' + self._log_tail)
        return

    def closed(self):
        return self._closed is True

    def disconnect(self):
        self.close()

    def _log_and_raise(self, err_msg):
        err_msg += self._log_tail
        log.exception(err_msg)
        raise ConnectionError(err_msg)