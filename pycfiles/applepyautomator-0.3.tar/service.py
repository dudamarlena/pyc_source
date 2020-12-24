# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/applepushnotification/service.py
# Compiled at: 2011-03-28 19:47:03
from gevent import monkey
monkey.patch_all()
import ssl, gevent, time, struct, sys
from gevent.queue import Queue
from gevent.event import Event
from socket import *
try:
    import json
except ImportError, e:
    import simplejson as json

class NotificationMessage(object):
    """
        Inititalizes a push notification message.

        token - device token
        alert - message string or message dictionary
        badge - badge number
        sound - name of sound to play
        identifier - message identifier
        expiry - expiry date of message
        extra - dictionary of extra parameters
        """

    def __init__(self, token, alert=None, badge=None, sound=None, identifier=0, expiry=None, extra=None):
        if len(token) != 32:
            raise ValueError, 'Token must be a 32-byte binary string.'
        if alert is not None and not isinstance(alert, (str, unicode, dict)):
            raise ValueError, 'Alert message must be a string or a dictionary.'
        if expiry is None:
            expiry = long(time.time() + 31536000)
        self.token = token
        self.alert = alert
        self.badge = badge
        self.sound = sound
        self.identifier = identifier
        self.expiry = expiry
        self.extra = extra
        return

    def __str__(self):
        aps = {'alert': self.alert}
        if self.badge is not None:
            aps['badge'] = self.badge
        if self.sound is not None:
            aps['sound'] = self.sound
        data = {'aps': aps}
        if self.extra is not None:
            data.update(self.extra)
        encoded = json.dumps(data)
        length = len(encoded)
        return struct.pack('!bIIH32sH%(length)ds' % {'length': length}, 1, self.identifier, self.expiry, 32, self.token, length, encoded)


class NotificationService(object):

    def __init__(self, sandbox=True, **kwargs):
        if 'certfile' not in kwargs:
            raise ValueError, 'Must specify a PEM bundle.'
        self._sslargs = kwargs
        self._push_connection = None
        self._feedback_connection = None
        self._sandbox = sandbox
        self._send_queue = Queue()
        self._error_queue = Queue()
        self._feedback_queue = Queue()
        self._send_greenlet = None
        self._error_greenlet = None
        self._feedback_greenlet = None
        self._send_queue_cleared = Event()
        return

    def _check_send_connection(self):
        if self._push_connection is None:
            s = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM, 0), ssl_version=ssl.PROTOCOL_SSLv3, **self._sslargs)
            addr = ['gateway.push.apple.com', 2195]
            if self._sandbox:
                addr[0] = 'gateway.sandbox.push.apple.com'
            s.connect_ex(tuple(addr))
            self._push_connection = s
            self._error_greenlet = gevent.spawn(self._error_loop)
        return

    def _check_feedback_connection(self):
        if self._feedback_connection is None:
            s = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM, 0), ssl_version=ssl.PROTOCOL_SSLv3, **self._sslargs)
            addr = ['feedback.push.apple.com', 2196]
            if self._sandbox:
                addr[0] = 'feedback.sandbox.push.apple.com'
            s.connect_ex(tuple(addr))
            self._feedback_connection = s
        return

    def _send_loop(self):
        self._send_greenlet = gevent.getcurrent()
        try:
            try:
                while True:
                    msg = self._send_queue.get()
                    self._check_send_connection()
                    try:
                        try:
                            self._push_connection.send(str(msg))
                        except Exception, e:
                            self._send_queue.put(msg)
                            self._push_connection.close()
                            self._push_connection = None
                            gevent.sleep(5.0)

                    finally:
                        if self._send_queue.qsize() < 1 and not self._send_queue_cleared.is_set():
                            self._send_queue_cleared.set()

            except gevent.GreenletExit, e:
                pass

        finally:
            self._send_greenlet = None

        return

    def _error_loop(self):
        self._error_greenlet = gevent.getcurrent()
        try:
            try:
                while True:
                    msg = self._push_connection.recv(6)
                    if len(msg) < 6:
                        return
                    data = struct.unpack('!bbI', msg)
                    self._error_queue.put((data[1], data[2]))

            except gevent.GreenletExit, e:
                pass

        finally:
            self._push_connection.close()
            self._push_connection = None
            self._error_greenlet = None

        return

    def _feedback_loop(self):
        self._feedback_greenlet = gevent.getcurrent()
        try:
            try:
                self._check_feedback_connection()
                while True:
                    msg = self._feedback_connection.recv(38)
                    if len(msg) < 38:
                        return
                    data = struct.unpack('!IH32s', msg)
                    self._feedback_queue.put((data[0], data[2]))

            except gevent.GreenletExit, e:
                pass

        finally:
            self._feedback_connection.close()
            self._feedback_connection = None
            self._feedback_greenlet = None

        return

    def send(self, obj):
        """Send a push notification"""
        if not isinstance(obj, NotificationMessage):
            raise ValueError, 'You can only send NotificationMessage objects.'
        self._send_queue.put(obj)

    def get_error(self, block=True, timeout=None):
        """
                Gets the next error message.
                
                Each error message is a 2-tuple of (status, identifier)."""
        return self._error_queue.get(block=block, timeout=timeout)

    def get_feedback(self, block=True, timeout=None):
        """
                Gets the next feedback message.

                Each feedback message is a 2-tuple of (timestamp, device_token)."""
        if self._feedback_greenlet is None:
            self._feedback_greenlet = gevent.spawn(self._feedback_loop)
        return self._feedback_queue.get(block=block, timeout=timeout)

    def wait_send(self, timeout=None):
        """Wait until all queued messages are sent."""
        self._send_queue_cleared.clear()
        self._send_queue_cleared.wait(timeout=timeout)

    def start(self):
        """Start the message sending loop."""
        if self._send_greenlet is None:
            self._send_greenlet = gevent.spawn(self._send_loop)
        return

    def stop(self, timeout=10.0):
        """
                Send all pending messages, close connection.
                Returns True if no message left to sent. False if dirty.
                
                - timeout: seconds to wait for sending remaining messages. disconnect
                  immedately if None.
                """
        if self._send_greenlet is not None and self._send_queue.qsize() > 0:
            self.wait_send(timeout=timeout)
        if self._send_greenlet is not None:
            gevent.kill(self._send_greenlet)
            self._send_greenlet = None
        if self._error_greenlet is not None:
            gevent.kill(self._error_greenlet)
            self._error_greenlet = None
        if self._feedback_greenlet is not None:
            gevent.kill(self._feedback_greenlet)
            self._feedback_greenlet = None
        return self._send_queue.qsize() < 1