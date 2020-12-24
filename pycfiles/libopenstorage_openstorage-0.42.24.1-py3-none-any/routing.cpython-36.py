# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/jeepney/jeepney/routing.py
# Compiled at: 2020-01-10 16:25:36
# Size of source mod 2**32: 2350 bytes
from .low_level import MessageType, HeaderFields
from .wrappers import DBusErrorResponse

class Router:
    __doc__ = 'Routing for messages coming back to a client application.\n    \n    :param handle_factory: Constructor for an object like asyncio.Future,\n        with methods *set_result* and *set_exception*. Outgoing method call\n        messages will get a handle associated with them.\n    :param on_unhandled: Callback for messages not otherwise dispatched.\n    '

    def __init__(self, handle_factory, on_unhandled=None):
        self.handle_factory = handle_factory
        self.on_unhandled = on_unhandled
        self.outgoing_serial = 0
        self.awaiting_reply = {}
        self.signal_callbacks = {}

    def outgoing(self, msg):
        """Set the serial number in the message & make a handle if a method call
        """
        self.outgoing_serial += 1
        msg.header.serial = self.outgoing_serial
        if msg.header.message_type is MessageType.method_call:
            self.awaiting_reply[msg.header.serial] = handle = self.handle_factory()
            return handle

    def subscribe_signal(self, callback, path, interface, member):
        """Add a callback for a signal.
        """
        self.signal_callbacks[(path, interface, member)] = callback

    def incoming(self, msg):
        """Route an incoming message.
        """
        hdr = msg.header
        if hdr.message_type is MessageType.signal:
            key = (
             hdr.fields.get(HeaderFields.path, None),
             hdr.fields.get(HeaderFields.interface, None),
             hdr.fields.get(HeaderFields.member, None))
            cb = self.signal_callbacks.get(key, None)
            if cb is not None:
                cb(msg.body)
                return
        reply_serial = hdr.fields.get(HeaderFields.reply_serial, -1)
        reply_handle = self.awaiting_reply.pop(reply_serial, None)
        if reply_handle is not None:
            if hdr.message_type is MessageType.method_return:
                reply_handle.set_result(msg.body)
                return
            if hdr.message_type is MessageType.error:
                reply_handle.set_exception(DBusErrorResponse(msg))
                return
        if self.on_unhandled:
            self.on_unhandled(msg)