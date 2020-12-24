# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xudd/actor.py
# Compiled at: 2013-08-06 23:06:50
from functools import wraps
from types import GeneratorType
import logging
_log = logging.getLogger(__name__)

def autoreply(func):
    """
    Automatically reply to a message if not handled in a handle_message
    method.  Replies in the most minimal way possible.
    """

    @wraps(func)
    def wrapper(self, message):
        result = func(self, message)
        if message.needs_reply():
            message.reply()
        return result

    return wrapper


class Actor(object):
    """
    Basic XUDD actor.
    """

    def __init__(self, hive, id):
        self.hive = hive
        self.id = id
        self.message_queue = hive.gen_message_queue()
        self.message_routing = {}
        self._waiting_coroutines = {}

    @autoreply
    def handle_message(self, message):
        """
        Handle a message being sent to this actor.
        """
        if message.in_reply_to is not None and message.in_reply_to in self._waiting_coroutines:
            coroutine = self._waiting_coroutines.pop(message.in_reply_to)
            try:
                if _log.level <= logging.DEBUG:
                    _log.debug(('Sending reply {0}').format(message))
                message_id = coroutine.send(message)
            except StopIteration:
                return

            self._waiting_coroutines[message_id] = coroutine
            return
        else:
            message_handler = self.message_routing[message.directive]
            result = message_handler(message)
            if isinstance(result, GeneratorType):
                coroutine = result
                message_id = result.send(None)
                self._waiting_coroutines[message_id] = coroutine
                return
            return

    def send_message(self, *args, **kwargs):
        return self.hive.send_message(*args, **kwargs)

    def wait_on_message(self, to, directive, from_id=None, id=None, body=None, in_reply_to=None):
        """
        Send a message that we'll wait for a reply to.
        """
        return self.hive.send_message(to, directive, from_id=from_id, body=body, in_reply_to=in_reply_to, id=id, wants_reply=True)


class ActorProxy(object):

    def __init__(self, actor_id):
        self.id = actor_id