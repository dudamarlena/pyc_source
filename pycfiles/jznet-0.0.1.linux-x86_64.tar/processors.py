# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyjznet/processors.py
# Compiled at: 2014-12-11 03:38:41
from __future__ import print_function
import threading, logging
from . import messages

class MessageProcessor(threading.Thread):

    def __init__(self, receive_msg_pool, send_msg_pool):
        threading.Thread.__init__(self)
        self.receive_msg_pool = receive_msg_pool
        self.send_msg_pool = send_msg_pool
        self._handlers = []
        self._handlers_map = {}
        self._init_handlers()

    def run(self):
        while True:
            pair = self.receive_msg_pool.take_message()
            if pair is not None:
                try:
                    self._process_message(pair[0], pair[1])
                except Exception as e:
                    print(e)
                    logging.error(e)

        return

    def _init_handlers(self):
        from . import listeners
        self._handlers.append(listeners.PlainMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.BinaryMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.CloseMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.ExceptionMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.ConnectMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.JsonMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.JsonEventMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        self._handlers.append(listeners.RpcMessageHandler(self.send_msg_pool).listen(self.receive_msg_pool))
        for handler in self._handlers:
            self._handlers_map[handler.interest()] = handler

    def add_rpc_service(self, name, rpc_service):
        handler = self._handlers_map.get(messages.RpcMessage)
        if handler is not None:
            handler.add_rpc_service(name, rpc_service)
        return

    def add_rpc_services(self, pairs):
        handler = self._handlers_map.get(messages.RpcMessage)
        if handler is not None:
            handler.add_rpc_services(pairs)
        return

    def _process_message(self, channel, msg):
        handler = self._handlers_map.get(type(msg))
        if handler is not None:
            handler.process(channel, msg)
        else:
            print("Can't find handler for msg type %s" % str(type(msg)))
        return