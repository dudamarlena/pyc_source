# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/uplink/handshake.py
# Compiled at: 2020-04-03 16:00:47
from __future__ import absolute_import, division, print_function
import six, typing as tp, copy, logging
from coolamqp.framing.definitions import ConnectionStart, ConnectionStartOk, ConnectionTune, ConnectionTuneOk, ConnectionOpen, ConnectionOpenOk
from coolamqp.framing.frames import AMQPMethodFrame
from coolamqp.uplink.connection.states import ST_ONLINE
from coolamqp.uplink.heartbeat import Heartbeater
from coolamqp import __version__
PUBLISHER_CONFIRMS = 'publisher_confirms'
CONSUMER_CANCEL_NOTIFY = 'consumer_cancel_notify'
SUPPORTED_EXTENSIONS = [
 PUBLISHER_CONFIRMS,
 CONSUMER_CANCEL_NOTIFY]
CLIENT_DATA = [
 (
  'product', ('CoolAMQP', 'S')),
 (
  'version', (__version__.encode('utf8'), 'S')),
 (
  'copyright', ('Copyright (C) 2016-2020 SMOK sp. z o.o.', 'S')),
 (
  'information',
  ('Licensed under the MIT License.\nSee https://github.com/smok-serwis/coolamqp for details',
 'S')),
 (
  'capabilities', ([ (capa, (True, 't')) for capa in SUPPORTED_EXTENSIONS ], 'F'))]
WATCHDOG_TIMEOUT = 10
logger = logging.getLogger(__name__)

class Handshaker(object):
    """
    Object that given a connection rolls the handshake.
    """

    def __init__(self, connection, node_definition, on_success, extra_properties=None):
        """
        :param connection: Connection instance to use
        :type node_definition: NodeDefinition
        :param on_success: callable/0, on success
        """
        self.connection = connection
        self.login = node_definition.user.encode('utf8')
        self.password = node_definition.password.encode('utf8')
        self.virtual_host = node_definition.virtual_host.encode('utf8')
        self.heartbeat = node_definition.heartbeat or 0
        self.connection.watch_for_method(0, ConnectionStart, self.on_connection_start)
        self.on_success = on_success
        self.EXTRA_PROPERTIES = extra_properties or []

    def on_watchdog(self):
        """
        Called WATCHDOG_TIMEOUT seconds after setup begins

        If we are not ST_ONLINE after that much, something is wrong and pwn this connection.
        """
        if self.connection.state != ST_ONLINE:
            self.connection.send(None)
        return

    def on_connection_start(self, payload):
        global CLIENT_DATA
        sasl_mechanisms = payload.mechanisms.tobytes().split(' ')
        locale_supported = payload.locales.tobytes().split(' ')
        if 'PLAIN' not in sasl_mechanisms:
            raise ValueError('Server does not support PLAIN')
        server_props = dict(payload.server_properties)
        if 'capabilities' in server_props:
            for label, fv in server_props['capabilities'][0]:
                if label in SUPPORTED_EXTENSIONS:
                    if fv[0]:
                        self.connection.extensions.append(label)

        self.connection.watchdog(WATCHDOG_TIMEOUT, self.on_watchdog)
        self.connection.watch_for_method(0, ConnectionTune, self.on_connection_tune)
        CLIENT_DATA = copy.copy(CLIENT_DATA)
        CLIENT_DATA.extend(self.EXTRA_PROPERTIES)
        self.connection.send([
         AMQPMethodFrame(0, ConnectionStartOk(CLIENT_DATA, 'PLAIN', '\x00' + self.login + '\x00' + self.password, locale_supported[0]))])

    def on_connection_tune(self, payload):
        self.connection.frame_max = payload.frame_max
        self.connection.heartbeat = min(payload.heartbeat, self.heartbeat)
        self.connection.free_channels.extend(six.moves.xrange(1, (65535 if payload.channel_max == 0 else payload.channel_max) + 1))
        self.connection.watch_for_method(0, ConnectionOpenOk, self.on_connection_open_ok)
        self.connection.send([
         AMQPMethodFrame(0, ConnectionTuneOk(payload.channel_max, payload.frame_max, self.connection.heartbeat)),
         AMQPMethodFrame(0, ConnectionOpen(self.virtual_host))])
        if self.connection.heartbeat > 0:
            Heartbeater(self.connection, self.connection.heartbeat)

    def on_connection_open_ok(self, payload):
        self.on_success()