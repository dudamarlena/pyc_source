# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/transport.py
# Compiled at: 2018-07-31 10:42:31
"""
传输层：负责生成/解析协议，以及发送/接收数据包
"""
__all__ = [
 'Transport', 'BlockingSocketUtility',
 'RecordTransport', 'BlockingRecordTransport']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod
import struct, socket, errno, logging, tornado.gen as gen
from .helper import *
from .exception import SocketAlreadyClosedError
LOGGER = logging.getLogger(__name__)

class Transport(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, stream):
        pass

    @abstractmethod
    def write(self, stream, transaction_id, buff):
        pass

    @abstractmethod
    def generate_packet(self, transaction_id, body_buff):
        pass

    @abstractmethod
    def get_name(self):
        pass


class BlockingSocketUtility(object):

    @staticmethod
    def read_bytes(sock, num):
        u"""在阻塞socket上读取固定数量的字节"""
        current_num = 0
        buff = bytearray(num)
        while current_num < num:
            try:
                incomming = sock.recv(num - current_num)
            except socket.timeout as ex:
                LOGGER.error('timeout reached in read_bytes()')
                continue
            except socket.error as ex:
                if ex.errno == errno.EINTR:
                    LOGGER.error(str(ex))
                    continue
                if ex.errno == errno.EBADF:
                    LOGGER.error('bad file descriptor')
                    raise SocketAlreadyClosedError
                raise

            if incomming == '':
                raise SocketAlreadyClosedError
            buff[current_num:(current_num + len(incomming))] = incomming
            current_num = current_num + len(incomming)

        return buff

    @staticmethod
    def write_data(sock, data):
        u"""向阻塞socket写数据"""
        data = memoryview(data)
        send_bytes = 0
        while send_bytes < len(data):
            try:
                length = sock.send(data[send_bytes:])
                send_bytes = send_bytes + length
            except socket.timeout:
                LOGGER.error('timeout reached in write_data()')


class _BaseRecordTransport(Transport, Singleton):
    HEAD_FMT = '!I'
    HEAD_LENGTH = struct.calcsize(HEAD_FMT)
    TRANSACTION_ID_FMT = '!I'
    TRANSACTION_ID_LENGTH = struct.calcsize(TRANSACTION_ID_FMT)
    BODY_FMT = '%ds'

    def generate_packet(self, transaction_id, body_buff):
        body_buff_len = len(body_buff)
        head_buff = struct.pack(self.HEAD_FMT, body_buff_len)
        transaction_id_buff = struct.pack(self.TRANSACTION_ID_FMT, transaction_id)
        body_buff = struct.pack(self.BODY_FMT % body_buff_len, body_buff)
        return head_buff + transaction_id_buff + body_buff

    def get_name(self):
        return 'record'


class RecordTransport(_BaseRecordTransport):

    @gen.coroutine
    def read(self, stream):
        head_buff = yield stream.read_bytes(self.HEAD_LENGTH)
        head_info = struct.unpack(self.HEAD_FMT, head_buff)[0]
        transaction_id_buff = yield stream.read_bytes(self.TRANSACTION_ID_LENGTH)
        transaction_id = struct.unpack(self.TRANSACTION_ID_FMT, transaction_id_buff)[0]
        body_length = head_info
        body_buff = yield stream.read_bytes(body_length)
        body = struct.unpack(self.BODY_FMT % body_length, body_buff)[0]
        raise gen.Return((transaction_id, body))

    @gen.coroutine
    def write(self, stream, transaction_id, buff):
        yield stream.write(self.generate_packet(transaction_id, buff))


class BlockingRecordTransport(_BaseRecordTransport):

    def read(self, sock):
        head_buff = BlockingSocketUtility.read_bytes(sock, self.HEAD_LENGTH)
        head_info = struct.unpack(self.HEAD_FMT, head_buff)[0]
        transaction_id_buff = BlockingSocketUtility.read_bytes(sock, self.TRANSACTION_ID_LENGTH)
        transaction_id = struct.unpack(self.TRANSACTION_ID_FMT, transaction_id_buff)[0]
        body_length = head_info
        body_buff = BlockingSocketUtility.read_bytes(sock, body_length)
        body = struct.unpack(self.BODY_FMT % body_length, body_buff)[0]
        return (
         transaction_id, body)

    def write(self, sock, transaction_id, buff):
        data = self.generate_packet(transaction_id, buff)
        BlockingSocketUtility.write_data(sock, data)