# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/attaches/agroup.py
# Compiled at: 2020-05-06 12:56:42
"""
This is an attache that attaches multiple attaches.

It evicts cancelled attaches.
"""
from __future__ import print_function, absolute_import, division
import logging
logger = logging.getLogger(__name__)
from coolamqp.attaches.channeler import Attache, ST_OFFLINE, ST_ONLINE
from coolamqp.attaches.consumer import Consumer
from coolamqp.attaches.publisher import Publisher

class AttacheGroup(Attache):
    """
    A bunch of attaches
    """

    def __init__(self):
        super(AttacheGroup, self).__init__()
        self.attaches = []
        self.tx_publisher = None
        self.non_tx_publisher = None
        return

    def add(self, attache):
        """
        Add an attache to this group.

        If this is attached, and connection is ST_ONLINE, .attach() will be called
        on this attache at once.

        :param attache: Attache instance
        """
        assert attache not in self.attaches
        self.attaches.append(attache)
        if self.connection is not None and self.connection.state != ST_OFFLINE:
            attache.attach(self.connection)
        if isinstance(attache, Consumer):
            attache.attache_group = self
        if isinstance(attache, Publisher):
            if attache.mode == Publisher.MODE_CNPUB:
                self.tx_publisher = attache
            else:
                self.non_tx_publisher = attache
        return

    def on_cancel_customer(self, customer):
        """
        Called by a customer, when it's cancelled.

        Consumer must have .attache_group set to this. This is done by .add()

        :param customer: a Customer instance
        """
        self.attaches.remove(customer)

    def attach(self, connection):
        """
        Attach to a connection

        :param connection: Connection instance of any state
        """
        self.connection = connection
        for attache in self.attaches:
            if not attache.cancelled:
                attache.attach(connection)

    def is_online(self):
        return self.tx_publisher.state == ST_ONLINE and self.non_tx_publisher.state == ST_ONLINE