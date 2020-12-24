# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/uplink/heartbeat.py
# Compiled at: 2020-04-03 16:00:47
from __future__ import absolute_import, division, print_function
import typing as tp, monotonic
from coolamqp.framing.frames import AMQPHeartbeatFrame
from coolamqp.uplink.connection.watches import AnyWatch

class Heartbeater(object):
    """
    An object that handles heartbeats
    """

    def __init__(self, connection, heartbeat_interval=0):
        self.connection = connection
        self.heartbeat_interval = heartbeat_interval
        self.last_heartbeat_on = monotonic.monotonic()
        self.connection.watchdog(self.heartbeat_interval, self.on_timer)
        self.connection.watch(AnyWatch(self.on_heartbeat))

    def on_heartbeat(self, frame):
        self.last_heartbeat_on = monotonic.monotonic()

    def on_any_frame(self):
        """
        Hehehe, most AMQP servers are not AMQP-compliant.
        Consider a situation where you just got like a metric shitton of messages,
        and the TCP connection is bustin' filled with those frames.

        Server should still be able to send a heartbeat frame, but it doesn't, because of the queue, and
        BANG, dead.

        I know I'm being picky, but at least I implement this behaviour correctly - see priority argument in send.

        Anyway, we should register an all-watch for this.
        """
        self.last_heartbeat_on = monotonic.monotonic()

    def on_timer(self):
        """Timer says we should send a heartbeat"""
        self.connection.send([AMQPHeartbeatFrame()], priority=True)
        if monotonic.monotonic() - self.last_heartbeat_on > 2 * self.heartbeat_interval:
            self.connection.send(None)
        self.connection.watchdog(self.heartbeat_interval, self.on_timer)
        return