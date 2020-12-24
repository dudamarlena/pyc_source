# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/uplink/listener/socket.py
# Compiled at: 2020-05-06 12:56:42
from __future__ import absolute_import, division, print_function
import collections, logging, socket
logger = logging.getLogger(__name__)

class SocketFailed(IOError):
    """Failure during socket operation. It needs to be discarded."""


class BaseSocket(object):
    """
    Base class for sockets provided to listeners.

    This is based on a standard TCP socket.

    To be instantiated only by Listeners.
    """

    def __init__(self, sock, on_read=lambda data: None, on_time=lambda : None, on_fail=lambda : None):
        """

        :param sock: socketobject
        :param on_read: callable(data) to be called when data is read.
            Listener thread context
            Raises ValueError on socket should be closed
        :param on_time: callable() when time provided by socket expires
        :param on_fail: callable() when socket is dead and to be discarded.
            Listener thread context.
            Socket descriptor will be handled by listener.
            This should not
        """
        assert sock is not None
        self.sock = sock
        self.data_to_send = collections.deque()
        self.priority_queue = collections.deque()
        self.my_on_read = on_read
        self._on_fail = on_fail
        self.on_time = on_time
        self.is_failed = False
        return

    def on_fail(self):
        self.is_failed = True
        self._on_fail()

    def send(self, data, priority=True):
        """
        Schedule to send some data.

        :param data: data to send, or None to terminate this socket.
            Note that data will be sent atomically, ie. without interruptions.
        :param priority: preempt other datas. Property of sending data atomically will be maintained.
        """
        if self.is_failed:
            return
        else:
            if data is None:
                self.priority_queue = collections.deque()
                self.data_to_send = collections.deque([None])
                return
            if priority:
                self.priority_queue.append(data)
            else:
                self.data_to_send.append(data)
            return

    def oneshot(self, seconds_after, callable):
        """
        Set to fire a callable N seconds after
        :param seconds_after: seconds after this
        :param callable: callable/0
        """
        raise Exception('Abstract; listener should override that')

    def noshot(self):
        """
        Clear all time-delayed callables.

        This will make no time-delayed callables delivered if ran in listener thread
        """
        raise Exception('Abstract; listener should override that')

    def on_read(self):
        """Socket is readable, called by Listener"""
        if self.is_failed:
            return
        try:
            data = self.sock.recv(2048)
        except (IOError, socket.error) as e:
            raise SocketFailed(repr(e))

        if len(data) == 0:
            raise SocketFailed('connection gracefully closed')
        try:
            self.my_on_read(data)
        except ValueError as e:
            raise SocketFailed(repr(e))

    def wants_to_send_data(self):
        return not (len(self.data_to_send) == 0 and len(self.priority_queue) == 0)

    def on_write(self):
        """
        Socket is writable, called by Listener
        :raises SocketFailed: on socket error
        :return: True if I'm done sending shit for now
        """
        if self.is_failed:
            return False
        else:
            while True:
                if len(self.data_to_send) == 0:
                    if len(self.priority_queue) == 0:
                        return True
                    self.data_to_send.appendleft(self.priority_queue.popleft())
                assert len(self.data_to_send) > 0
                if self.data_to_send[0] is None:
                    raise SocketFailed()
                try:
                    sent = self.sock.send(self.data_to_send[0])
                except (IOError, socket.error):
                    raise SocketFailed()

                if sent < len(self.data_to_send[0]):
                    self.data_to_send[0] = self.data_to_send[0][sent:]
                    return False
                self.data_to_send.popleft()
                if len(self.priority_queue) > 0:
                    self.data_to_send.appendleft(self.priority_queue.popleft())

            return

    def fileno(self):
        """Return descriptor number"""
        return self.sock.fileno()

    def close(self):
        """Close this socket"""
        self.sock.close()