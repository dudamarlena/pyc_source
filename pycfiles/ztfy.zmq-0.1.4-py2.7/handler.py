# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmq/handler.py
# Compiled at: 2014-05-12 03:31:21
from zmq.utils import jsonapi as json
from ztfy.zmq.interfaces import IZMQMessageHandler
from zope.interface import implements

class ZMQMessageHandler(object):
    """
    Base class for message handlers for a :class:`ztfy.zmq.process.Process`.

    Inheriting classes only need to implement a handler function for each
    message type.
    """
    implements(IZMQMessageHandler)
    handler = None

    def __init__(self, process, stream, stop, handler=None, json_load=-1):
        self.process = process
        self._json_load = json_load
        self.rep_stream = stream
        self._stop = stop
        self.rep_handler = handler or self.handler()
        self.rep_handler.process = process

    def __call__(self, msg):
        """
        Gets called when a messages is received by the stream this handlers is
        registered at. *msg* is a list as returned by
        :meth:`zmq.core.socket.Socket.recv_multipart`.
        """
        i = self._json_load
        msg_type, data = json.loads(msg[i])
        msg[i] = data
        if msg_type.startswith('_'):
            raise AttributeError('%s starts with an "_"' % msg_type)
        rep = getattr(self.rep_handler, msg_type)(*msg)
        self.rep_stream.send_json(rep)