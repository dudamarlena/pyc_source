# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/connectors/zmq_tunnel.py
# Compiled at: 2015-04-04 17:44:17
from __future__ import absolute_import, unicode_literals
from tornado import gen
from tornado.concurrent import is_future
import zmq, zmq.eventloop.ioloop
from zmq.eventloop.zmqstream import ZMQStream
from logdog.core.msg import Msg
from .base import BaseConnector
zmq.eventloop.ioloop.install()

class ZMQTunnel(BaseConnector):
    defaults = BaseConnector.defaults(unique=True, connect=(), bind=(), socket=None)

    def __init__(self, *args, **kwargs):
        if not isinstance(kwargs.get(b'bind', ()), (list, tuple)):
            kwargs[b'bind'] = (
             kwargs[b'bind'],)
        if not isinstance(kwargs.get(b'connect', ()), (list, tuple)):
            kwargs[b'connect'] = (
             kwargs[b'connect'],)
        self.stream = self.socket = None
        self.ctx = zmq.Context()
        super(ZMQTunnel, self).__init__(*args, **kwargs)
        return

    def __str__(self):
        return (b'ZMQ-TUNNEL:{}:{}').format(self.config.socket, (b',').join(self.config.bind) or (b',').join(self.config.connect) or b'None')

    @classmethod
    def __singleton_key__(cls, passed_args, passed_kwargs):
        key = super(ZMQTunnel, cls).__singleton_key__(passed_args, passed_kwargs)
        connect = passed_kwargs.get(b'connect', cls.defaults.connect) or ()
        if not isinstance(connect, (list, tuple)):
            connect = [
             connect]
        bind = passed_kwargs.get(b'bind', cls.defaults.bind) or ()
        if not isinstance(bind, (list, tuple)):
            bind = [
             bind]
        return (b'{key}::socket-type={socket_type}::bind={bind}::connect={connect}').format(key=key, socket_type=passed_kwargs.get(b'socket', cls.defaults.socket), connect=(b',').join(sorted(connect)) or b'None', bind=(b',').join(sorted(bind)) or b'None')

    def _pre_start(self):
        self.socket = self.ctx.socket(getattr(zmq, self.config.socket))
        if b'bind' in self.config:
            for addr in self.config.bind:
                self.socket.bind(addr)

        if b'connect' in self.config:
            for addr in self.config.connect:
                self.socket.connect(addr)

        self.stream = ZMQStream(self.socket, io_loop=self.app.io_loop)
        self.stream.on_recv(self.on_recv)

    @gen.coroutine
    def on_recv(self, data):
        data = Msg.deserialize_jsonb(data[0])
        ret = self._forward(data)
        if is_future(ret):
            yield ret

    def send(self, data):
        if self.started:
            data = data.serialize_jsonb()
            return self.stream.send(msg=data)