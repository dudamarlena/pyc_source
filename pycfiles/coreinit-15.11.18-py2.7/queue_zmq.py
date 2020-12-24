# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/msg/queue_zmq.py
# Compiled at: 2015-11-12 02:42:40
from coreinit.msg.queue_base import QueueBase
from coreinit.utils.installer import *

class Queue(QueueBase):
    endpoint = None
    mode = None
    zmq_ctx = None
    zmq_sock = None
    NOBLOCK = None

    def configure(self, mode, endpoint):
        super(Queue, self).configure(mode, endpoint)
        try:
            import zmq
        except:
            install_system(['python-zmq'])

        self.NOBLOCK = zmq.NOBLOCK
        self.mode = mode
        self.endpoint = endpoint

    def conect(self):
        import zmq
        self.zmq_ctx = zmq.Context()
        if mode == 'PUSH':
            self.zmq_sock = self.zmq_ctx.socket(zmq.PUSH)
            self.zmq_sock.bind(self.endpoint)
        elif mode == 'PULL':
            self.zmq_sock = self.zmq_ctx.socket(zmq.PULL)
            self.zmq_sock.connect(self.endpoint)
        if mode == 'PUB':
            self.zmq_sock = self.zmq_ctx.socket(zmq.PUB)
            self.zmq_sock.bind(self.endpoint)
        elif mode == 'SUB':
            self.zmq_sock = self.zmq_ctx.socket(zmq.SUB)
            self.zmq_sock.connect(self.endpoint)

    def send(self, data):
        super(Queue, self).senf(data)
        self.zmq_sock.send(data)

    def recv(self, blocking=True):
        super(Queue, self).recv(blocking)
        if blocking:
            return self.zmq_sock.recv()
        else:
            return self.zmq_sock.recv(self.NOBLOCK)