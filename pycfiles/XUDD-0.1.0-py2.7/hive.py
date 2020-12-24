# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xudd/hive.py
# Compiled at: 2013-08-06 23:06:50
from __future__ import print_function
import uuid
from collections import deque
from threading import Thread
from itertools import count
from xudd import PY2
from xudd.message import Message

class Hive(Thread):
    """
    Hive handles all actors and the passing of messages between them.

    Inter-hive communication may exist in the future, it doesn't yet ;)
    """

    def __init__(self, actor_messages_per_cycle=15):
        super(Hive, self).__init__()
        self._actor_registry = {}
        self._actor_queue = deque()
        self._actors_in_queue = set()
        self.hive_action_queue = deque()
        self.should_stop = False
        if PY2:
            self.message_uuid = unicode(uuid.uuid4())
        else:
            self.message_uuid = str(uuid.uuid4())
        self.message_counter = count()
        self.actor_messages_per_cycle = actor_messages_per_cycle

    def register_actor(self, actor):
        self._actor_registry[actor.id] = actor

    def remove_actor(self, actor_id):
        self._actor_registry.pop(actor_id)

    def send_message(self, to, directive, from_id=None, body=None, in_reply_to=None, id=None, wants_reply=None):
        """
        API for sending a message to an actor.

        Note, not the same as queueing a message which is a more low-level
        action.  This also constructs a proper Message object.
        """
        message_id = id or self.gen_message_id()
        message = Message(to=to, directive=directive, from_id=from_id, body=body, in_reply_to=in_reply_to, id=message_id, wants_reply=wants_reply)
        self.hive_action_queue.append((
         'queue_message', message))
        return message_id

    def request_possibly_requeue_actor(self, actor):
        self.hive_action_queue.append((
         'check_queue_actor', actor))

    def queue_message(self, message):
        """
        Queue a message to its appropriate actor.
        """
        try:
            actor = self._actor_registry[message.to]
        except KeyError:
            print("Wouldn't it be nice if we handled sending messages to an actor that didn't exist more gracefully?")
            return False

        message.hive_proxy = actor.hive
        actor.message_queue.append(message)
        self.request_possibly_requeue_actor(actor)

    def run(self):
        self.workloop()

    def gen_message_queue(self):
        """Generate a message queue for an actor.

        Note: in this case we're just returning a simple deque(), but hives
        should actually be able to put more complicated queues (possibly
        wrapper queues, see xudd/experimental/threaded_hive.py) on an actor.
        It's up to the hive to decide what kind of queue is
        appropriate... excepting in certain circumstances (such as
        DedicatedActors, which don't exist at the time of writing this), actors
        shouldn't be processing their own queues!
        """
        return deque()

    def gen_proxy(self):
        return HiveProxy(self)

    def workloop(self):
        while not self.should_stop:
            self._process_hive_actions()
            self._process_actor_messages()

    def _process_hive_actions(self):
        for i in range(len(self.hive_action_queue)):
            try:
                action = self.hive_action_queue.popleft()
            except IndexError:
                break

            action_type = action[0]
            if action_type == 'check_queue_actor':
                actor = action[1]
                if not len(actor.message_queue) == 0 and actor not in self._actors_in_queue:
                    self._actor_queue.append(actor)
                    self._actors_in_queue.add(actor)
            elif action_type == 'queue_message':
                message = action[1]
                self.queue_message(message)
            else:
                raise UnknownHiveAction('Unknown action: %s' % action_type)

    def _process_actor_messages(self):
        for i in range(len(self._actor_queue)):
            actor = self._actor_queue.popleft()
            self._actors_in_queue.remove(actor)
            messages_processed = 0
            while self.actor_messages_per_cycle is None or messages_processed < self.actor_messages_per_cycle:
                try:
                    message = actor.message_queue.popleft()
                except IndexError:
                    break

                actor.handle_message(message)
                messages_processed += 1

            self.request_possibly_requeue_actor(actor)

        return

    def gen_actor_id(self):
        """
        Generate an actor id.
        """
        if PY2:
            return unicode(uuid.uuid4())
        else:
            return str(uuid.uuid4())

    def gen_message_id(self):
        """
        Generate a unique message id.

        Since uuid4s take a bit of time to compose, instead we keep a
        local counter combined with our hive's counter-uuid.
        """
        if PY2:
            return '%s:%s' % (self.message_uuid, self.message_counter.next())
        else:
            return '%s:%s' % (self.message_uuid, self.message_counter.__next__())

    def create_actor(self, actor_class, *args, **kwargs):
        hive_proxy = self.gen_proxy()
        actor_id = kwargs.pop('id', None) or self.gen_actor_id()
        actor = actor_class(hive_proxy, actor_id, *args, **kwargs)
        hive_proxy.associate_with_actor(actor)
        self.register_actor(actor)
        return actor_id

    def send_shutdown(self):
        self.should_stop = True


class UnknownHiveAction(Exception):
    pass


class HiveProxy(object):
    """
    Proxy to the Hive.

    Doesn't expose the entire hive because that could result in
    actors playing with things they shouldn't. :)
    """

    def __init__(self, hive):
        self._hive = hive
        self._actor = None
        return

    def associate_with_actor(self, actor):
        """
        Associate an actor with ourselves
        """
        self._actor = actor

    def send_message(self, to, directive, from_id=None, body=None, in_reply_to=None, id=None, wants_reply=None):
        from_id = from_id or self._actor.id
        return self._hive.send_message(to=to, directive=directive, from_id=from_id, body=body, in_reply_to=in_reply_to, id=id, wants_reply=wants_reply)

    def gen_message_queue(self, *args, **kwargs):
        return self._hive.gen_message_queue(*args, **kwargs)

    def remove_actor(self, *args, **kwargs):
        return self._hive.remove_actor(*args, **kwargs)

    def create_actor(self, actor_class, *args, **kwargs):
        return self._hive.create_actor(actor_class, *args, **kwargs)

    def send_shutdown(self, *args, **kwargs):
        return self._hive.send_shutdown(*args, **kwargs)