# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/serf_client2/connection.py
# Compiled at: 2016-08-26 10:38:38
import socket, msgpack, resource

class ConnectionError(Exception):
    pass


class ConnectionTimeoutError(ConnectionError):
    pass


class Connection(object):
    host = None
    port = None
    timeout = None
    _socket = None
    page_size = None

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.page_size = resource.getpagesize()
        self.unpacker = msgpack.Unpacker(object_hook=_decode_addr_key)

    @property
    def socket(self):
        if not self._socket:
            try:
                self._socket = socket.create_connection((self.host, self.port), self.timeout)
            except socket.error as e:
                raise ConnectionError(*e.args)

        return self._socket

    def read(self):
        try:
            buf = self.socket.recv(self.page_size)
            if len(buf) == 0:
                raise ConnectionError('Connection closed by peer')
            self.unpacker.feed(buf)
        except socket.timeout as e:
            raise ConnectionTimeoutError(*e.args)

        return list(self.unpacker)

    def write(self, message_or_messages):
        if isinstance(message_or_messages, list):
            to_send = ('').join(msgpack.packb(m) for m in message_or_messages)
        else:
            to_send = msgpack.packb(message_or_messages)
        self.socket.sendall(to_send)

    def close(self):
        """
        Close the connection with the Serf agent.
        """
        if self._socket:
            self._socket.close()
            self._socket = None
        return


def _decode_addr_key(obj_dict):
    """
    Callback function to handle the decoding of the 'Addr' field.

    Serf msgpack 'Addr' as an IPv6 address, and the data needs to be unpack
    using socket.inet_ntop().

    See: https://github.com/KushalP/serfclient-py/issues/20

    :param obj_dict: A dictionary containing the msgpack map.
    :return: A dictionary with the correct 'Addr' format.
    """
    key = 'Addr'
    if key in obj_dict:
        try:
            ip_addr = socket.inet_ntop(socket.AF_INET6, obj_dict[key])
            if ip_addr.startswith('::ffff:'):
                ip_addr = ip_addr.lstrip('::ffff:')
            obj_dict[key] = ip_addr.encode('utf-8')
        except ValueError:
            ip_addr = socket.inet_ntop(socket.AF_INET, obj_dict[key])
            obj_dict[key] = ip_addr.encode('utf-8')

    return obj_dict