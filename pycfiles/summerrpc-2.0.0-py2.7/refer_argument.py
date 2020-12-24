# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/refer_argument.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'ReferArgument']
__authors__ = ['Tim Chow']

class ReferArgument(object):

    def __init__(self):
        self._connection_pool_size = 15
        self._client_socket_timeout = 15
        self._protocol = None
        self._write_timeout = 30
        self._read_timeout = 30
        self._max_pending_writes = None
        self._max_pending_reads = None
        self._max_pooling_reads = None
        self._heartbeat_interval = None
        return

    @property
    def connection_pool_size(self):
        return self._connection_pool_size

    def set_connection_pool_size(self, connection_pool_size):
        self._connection_pool_size = connection_pool_size
        return self

    @property
    def client_socket_timeout(self):
        return self._client_socket_timeout

    def set_client_socket_timeout(self, client_socket_timeout):
        self._client_socket_timeout = client_socket_timeout
        return self

    @property
    def protocol(self):
        return self._protocol

    def set_protocol(self, protocol):
        self._protocol = protocol
        return self

    @property
    def write_timeout(self):
        return self._write_timeout

    def set_write_timeout(self, write_timeout):
        self._write_timeout = write_timeout
        return self

    @property
    def read_timeout(self):
        return self._read_timeout

    def set_read_timeout(self, read_timeout):
        self._read_timeout = read_timeout
        return self

    @property
    def max_pending_writes(self):
        return self._max_pending_writes

    def set_max_pending_writes(self, max_pending_writes):
        self._max_pending_writes = max_pending_writes
        return self

    @property
    def max_pending_reads(self):
        return self._max_pending_reads

    def set_max_pending_reads(self, max_pending_reads):
        self._max_pending_reads = max_pending_reads
        return self

    @property
    def max_pooling_reads(self):
        return self._max_pooling_reads

    def set_max_pooling_reads(self, max_pooling_reads):
        self._max_pooling_reads = max_pooling_reads
        return self

    @property
    def heartbeat_interval(self):
        return self._heartbeat_interval

    def set_heartbeat_interval(self, heartbeat_interval):
        self._heartbeat_interval = heartbeat_interval
        return self