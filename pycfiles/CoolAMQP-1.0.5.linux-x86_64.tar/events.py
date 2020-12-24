# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/clustering/events.py
# Compiled at: 2020-05-06 12:56:42
"""
Cluster will emit Events.

They mean that something, like, happened.
"""
from __future__ import print_function, absolute_import, division
import logging
from coolamqp.objects import ReceivedMessage
logger = logging.getLogger(__name__)

class Event(object):
    """
    An event emitted by Cluster
    """
    __slots__ = ()


class NothingMuch(Event):
    """Nothing happened :D"""
    __slots__ = ()


class ConnectionLost(Event):
    """
    We have lost the connection.

    NOTE that we don't have a ConnectionUp, since re-establishing a connection
    is a complicated process. Broker might not have recognized the failure,
    and some queues will be blocked, some might be ok, and the state
    might be just a bit noisy.

    Please examine your Consumer's .state's to check whether link was regained
    """
    __slots__ = ()


class MessageReceived(ReceivedMessage, Event):
    """
    Something that works as an ersatz ReceivedMessage, but is an event
    """
    __slots__ = ()

    def __init__(self, msg):
        """:type msg: ReceivedMessage"""
        ReceivedMessage.__init__(self, msg.body, msg.exchange_name, msg.routing_key, properties=msg.properties, delivery_tag=msg.delivery_tag, ack=msg.ack, nack=msg.nack)