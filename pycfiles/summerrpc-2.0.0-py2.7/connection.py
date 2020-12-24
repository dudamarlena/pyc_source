# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/connection.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'Connection', 'BlockingConnection']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod, abstractproperty
import threading, socket
from functools import partial
import time, logging, traceback
from concurrent.futures import Future
from summerrpc.helper import *
from summerrpc.exception import *
LOGGER = logging.getLogger(__name__)

class Connection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def write(self, buff):
        u"""写数据"""
        pass

    @abstractmethod
    def read(self, transaction_id):
        u"""读响应"""
        pass

    @abstractmethod
    def close(self):
        u"""关闭连接以及底层的socket"""
        pass

    @abstractproperty
    def closed(self):
        u"""该属性标识表示：Connection以及底层socket是否已经关闭成功"""
        pass

    @abstractproperty
    def stopping(self):
        pass


class BlockingConnection(Connection):

    def __init__(self, underlying_socket, transport, max_pending_writes=None, max_pending_reads=None, max_pooling_reads=None, write_timeout=60, heartbeat_interval=None, heartbeat_func=None):
        self._socket = underlying_socket
        self._peername = underlying_socket.getpeername()
        self._transport = transport
        self._write_timeout = write_timeout
        self._write_condition = threading.Condition()
        self._pending_writes = StaticList(max_pending_writes or 65535)
        self._async_write_thread = threading.Thread(target=self._async_write)
        self._async_write_thread.setDaemon(False)
        self._read_condition = threading.Condition()
        self._pending_reads = LRUCache(max_pending_reads or 65535)
        self._pooling_reads = LRUCache(max_pooling_reads or 65535)
        self._async_read_thread = threading.Thread(target=self._async_read)
        self._async_read_thread.setDaemon(False)
        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_func = heartbeat_func
        self._heartbeats = LRUCache(4)
        self._heartbeat_lock = threading.Lock()
        self._id_generator = partial(AtomicInteger(0).increment, 1, True)
        self._close_lock = threading.RLock()
        self._stopping = False
        self._closed = False
        self._async_read_thread.start()
        self._async_write_thread.start()

    def _update_pending_writes(self, buff, timeout):
        f = Future()
        transaction_id = self._id_generator()
        self._pending_writes.insert_left((
         buff, f, transaction_id,
         time.time(), timeout))
        return (f, transaction_id)

    def write(self, buff, timeout=None):
        timeout = timeout or self._write_timeout
        self._write_condition.acquire()
        try:
            if self._stopping or self._closed:
                raise ConnectionAlreadyClosedError('connection already closed')
            if self._pending_writes.is_full():
                raise MaxPendingWritesReachedError('max pending writes reached')
            f, transaction_id = self._update_pending_writes(buff, timeout)
            self._write_condition.notify_all()
            return (transaction_id, f)
        finally:
            self._write_condition.release()

    def read(self, transaction_id):
        self._read_condition.acquire()
        try:
            if self._stopping or self._closed:
                raise ConnectionAlreadyClosedError('connection already closed')
            if transaction_id in self._pooling_reads:
                f = self._pooling_reads[transaction_id]
                del self._pooling_reads[transaction_id]
                return f
            if transaction_id in self._pending_reads:
                return self._pending_reads[transaction_id]
            entry = self._pending_reads.will_be_kicked_out()
            if entry is not None:
                entry.value.set_exception(MaxPendingReadsReachedError('max pending reads reached'))
            f = Future()
            self._pending_reads[transaction_id] = f
            self._read_condition.notify_all()
            return f
        finally:
            self._read_condition.release()

        return

    def _async_write(self):
        LOGGER.debug('async write thread starting, thread ident: %s' % threading.currentThread().ident)
        missing_too_many_heartbeat = False
        need_to_wakeup_read_thread = False
        while True:
            if missing_too_many_heartbeat:
                self.close()
                missing_too_many_heartbeat = False
                break
            if need_to_wakeup_read_thread:
                with self._read_condition:
                    LOGGER.debug('wake up read thread, because there is new heartbeat')
                    self._read_condition.notify_all()
                need_to_wakeup_read_thread = False
            self._write_condition.acquire()
            if self._stopping or self._closed:
                self._write_condition.release()
                break
            if self._pending_writes.size <= 0:
                time_to_wait = None if self._heartbeat_interval is None else self._heartbeat_interval / 2.0
                self._write_condition.wait(time_to_wait)
                LOGGER.debug('async write thread has been waken up')
                if not self._stopping and not self._closed and self._pending_writes.size <= 0 and self._heartbeat_func is not None and self._heartbeat_interval is not None:
                    with self._heartbeat_lock:
                        if self._heartbeats.current_size < self._heartbeats.max_size:
                            f, transaction_id = self._update_pending_writes(self._heartbeat_func(), self._heartbeat_interval)
                            self._heartbeats[transaction_id] = f
                            need_to_wakeup_read_thread = True
                        else:
                            LOGGER.error('missing too many heartbeat, closing connection')
                            missing_too_many_heartbeat = True
                self._write_condition.release()
                continue
            buff, future, transaction_id, timestamp, timeout = self._pending_writes.pop_left()
            self._write_condition.release()
            if timeout is not None and timestamp + timeout <= time.time():
                future.set_exception(ConnectionWriteTimeout('transaction_id: %s' % transaction_id))
                continue
            try:
                self._transport.write(self._socket, transaction_id, buff)
                future.set_result(transaction_id)
            except socket.error as ex:
                if ex.errno in ERRNO_CONNRESET:
                    self.close()
                    break
                traceback.print_exc()
                raise
            except BaseException:
                traceback.print_exc()
                raise

            time.sleep(0.0)

        LOGGER.info('async write thread exited, thread indent: %s' % threading.currentThread().ident)
        return

    def _async_read(self):
        LOGGER.debug('async read thread starting, thread ident: %s' % threading.currentThread().ident)
        while True:
            self._read_condition.acquire()
            if self._stopping or self._closed:
                self._read_condition.release()
                break
            if self._pending_reads.current_size <= 0:
                self._heartbeat_lock.acquire()
                has_hearbeat = self._heartbeats.current_size > 0
                self._heartbeat_lock.release()
                if not has_hearbeat:
                    self._read_condition.wait()
                    LOGGER.debug('async read thread has been waken up')
                    self._read_condition.release()
                    continue
            self._read_condition.release()
            try:
                transaction_id, buff = self._transport.read(self._socket)
            except SocketAlreadyClosedError as ex:
                LOGGER.error('socket that connected to %s already closed' % str(self._peername))
                self.close()
                break

            with self._heartbeat_lock:
                if self._stopping or self._closed:
                    break
                if transaction_id in self._heartbeats:
                    LOGGER.debug('accept heartbeat response, transaction_id is: %s' % transaction_id)
                    f = self._heartbeats[transaction_id]
                    f.set_result(buff)
                    del self._heartbeats[transaction_id]
                    continue
            with self._read_condition:
                if self._stopping or self._closed:
                    break
                if transaction_id in self._pending_reads:
                    f = self._pending_reads[transaction_id]
                    del self._pending_reads[transaction_id]
                    f.set_result(buff)
                    continue
                entry = self._pooling_reads.will_be_kicked_out()
                if entry is not None:
                    LOGGER.error("transaction_id: %s hasn't been consumed" % entry.key)
                f = Future()
                f.set_result(buff)
                self._pooling_reads[transaction_id] = f

        LOGGER.info('async read thread exited, thread ident: %d' % threading.currentThread().ident)
        return

    def close(self):
        if self._closed:
            return
        with self._close_lock:
            if self._closed:
                return
            self._stopping = True
            self._socket.close()
            self._close_write()
            self._close_read()
            self._closed = True
            self._stopping = False

    def _close_write(self):
        self._write_condition.acquire()
        while self._pending_writes.size > 0:
            buff, future, transaction_id, timestamp, timeout = self._pending_writes.pop_left()
            future.set_exception(ConnectionAlreadyClosedError('transaction_id: %d' % transaction_id))

        self._write_condition.notify_all()
        self._write_condition.release()

    def _close_read(self):
        self._read_condition.acquire()
        head = self._pending_reads.head
        entry = head.prev
        while entry is not head:
            entry.value.set_exception(ConnectionAlreadyClosedError('transaction_id: %s' % entry.key))
            LOGGER.info('closing read: transaction_id: %d' % entry.key)
            entry = entry.prev

        self._pooling_reads.clear()
        self._read_condition.notify_all()
        self._read_condition.release()

    @property
    def closed(self):
        return self._closed

    @property
    def stopping(self):
        return self._stopping