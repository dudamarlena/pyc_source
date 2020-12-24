# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/clustering/events.py
# Compiled at: 2020-04-03 16:00:47
__doc__ = '\nCluster will emit Events.\n\nThey mean that something, like, happened.\n'
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