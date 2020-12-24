# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/clustering/single.py
# Compiled at: 2020-05-06 12:56:42
from __future__ import print_function, absolute_import, division
import logging
from coolamqp.framing.definitions import ConnectionUnblocked, ConnectionBlocked
from coolamqp.objects import Callable
from coolamqp.uplink import Connection
from coolamqp.uplink.connection import MethodWatch
logger = logging.getLogger(__name__)

class SingleNodeReconnector(object):
    """
    Connection to one node. It will do it's best to remain alive.
    """

    def __init__(self, node_def, attache_group, listener_thread, extra_properties=None, log_frames=None, name=None):
        self.listener_thread = listener_thread
        self.node_def = node_def
        self.attache_group = attache_group
        self.connection = None
        self.extra_properties = extra_properties
        self.log_frames = log_frames
        self.name = name or 'CoolAMQP'
        self.terminating = False
        self.on_fail = Callable()
        self.on_blocked = Callable()
        self.on_fail.add(self._on_fail)
        return

    def is_connected(self):
        return self.connection is not None

    def connect(self, timeout):
        assert self.connection is None
        self.connection = Connection(self.node_def, self.listener_thread, extra_properties=self.extra_properties, log_frames=self.log_frames, name=self.name)
        self.attache_group.attach(self.connection)
        self.connection.start(timeout)
        self.connection.finalize.add(self.on_fail)
        mw = MethodWatch(0, (ConnectionBlocked,), lambda : self.on_blocked(True))
        mw.oneshot = False
        self.connection.watch(mw)
        mw = MethodWatch(0, (ConnectionUnblocked,), lambda : self.on_blocked(False))
        mw.oneshot = False
        self.connection.watch(mw)
        return

    def _on_fail(self):
        if self.terminating:
            return
        else:
            self.connection = None
            self.listener_thread.call_next_io_event(self.connect)
            return

    def shutdown(self):
        """Close this connection"""
        self.terminating = True
        if self.connection is not None:
            self.connection.send(None)
            self.connection = None
        return