# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/restzzz/lib/python2.7/site-packages/restzzz/zmqwrap.py
# Compiled at: 2014-09-25 18:18:09
import pyramid.exceptions as exc, zmq

class PubSocket(object):

    def __init__(self, connect, subject=None):
        ctx = zmq.Context.instance()
        self._sock = ctx.socket(zmq.PUB)
        self._sock.connect(connect)
        self.subject = subject

    def send(self, *args):
        msg = []
        if self.subject is not None:
            msg.append(self.subject)
        msg.extend(args)
        self._sock.send_multipart(msg)
        return msg


class SubSocket(object):

    def __init__(self, connect, subject=''):
        ctx = zmq.Context.instance()
        self._sock = ctx.socket(zmq.SUB)
        self._sock.connect(connect)
        self._sock.set(zmq.SUBSCRIBE, subject)
        self.subject = subject

    def subscribe(self, subject):
        self._sock.set(zmq.UNSUBSCRIBE, self.subject)
        self._sock.set(zmq.SUBSCRIBE, self.subject)
        self.subject = subject

    def recv(self):
        if self._sock.poll(10):
            return self._sock.recv_multipart()
        raise exc.NotFound