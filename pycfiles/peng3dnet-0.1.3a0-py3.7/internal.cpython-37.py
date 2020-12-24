# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/packet/internal.py
# Compiled at: 2020-04-07 16:44:48
# Size of source mod 2**32: 7683 bytes
r"""
This module contains various internal packets not intended for direct use.

These packets will be registered by the default implementations of client and
server classes with names starting with ``peng3dnet:``\ . Any other packets whose
name starts with ``peng3dnet:`` may be processed incorrectly.

Additionally, packets within this module usually use reserved and static packet IDs below 16.

Handshake
=========

Note that if a custom connection type is used, any steps after step 3. may be left out.

1. Server sends a :py:class:`HelloPacket` with version information
2. Client responds with :py:class:`SetTypePacket` containing connection type
3. Server stores connection type and sends :py:class:`HandshakePacket` containing version and registry
4. Client updates own registry based on packet and sends :py:class:`HandshakeAcceptPacket`
5. Server receives packet and calls event handler to signal a successful handshake

Connection shutdown
===================

Note that this only applies to clean shutdowns caused by :py:meth:`~peng3dnet.net.Server.close_connection()` or its client-side equivalent.

1. ``close_connection()`` is called
2. :py:class:`CloseConnectionPacket` is sent to peer and internal flag is set
3. After packet has been fully sent, event handlers are called
4. Peer receives packet and calls event handlers
5. Server cleans up internal data structures
"""
__all__ = [
 'HelloPacket', 'SetTypePacket',
 'HandshakePacket', 'HandshakeAcceptPacket',
 'CloseConnectionPacket']
from . import Packet, SmartPacket
from ..constants import *
from .. import version

class HelloPacket(SmartPacket):
    __doc__ = '\n    Internal packet sent by the server to initialize a handshake.\n    \n    This is usually the first packet transmitted by every connection.\n    It contains version information for the client to check.\n    \n    If the client does not support the given protocol version, the connection must be aborted with the reason ``protoversionmismatch``\\ .\n    '
    state = STATE_HELLOWAIT
    side = SIDE_CLIENT
    conntype = CONNTYPE_NOTSET

    def receive(self, msg, cid=None):
        if msg['version'] != version.VERSION:
            pass
        if msg['protoversion'] != version.PROTOVERSION:
            self.peer.close_connection(cid, 'protoversionmismatch')
            return
        if self.peer.cfg['net.debug.print.connect']:
            print('HELLO')
        self.peer.send_message('peng3dnet:internal.settype', {'conntype': self.peer.target_conntype})
        self.peer.remote_state = STATE_WAITTYPE
        self.peer.conntypes[self.peer.target_conntype].init(cid)

    receive.__noautodoc__ = True

    def send(self, msg, cid=None):
        self.peer.clients[cid].state = STATE_WAITTYPE
        if self.peer.cfg['net.debug.print.connect']:
            print('HELLO %s' % cid)

    send.__noautodoc__ = True


class SetTypePacket(SmartPacket):
    __doc__ = '\n    Internal packet sent by the client to indicate the connection type.\n    \n    If the server does not recognize the connection type, the connection must be aborted with the reason ``unknownconntype``\\ .\n    \n    If no connection type is supplied, ``classic`` is substituted.\n    '
    state = STATE_WAITTYPE
    side = SIDE_SERVER

    def receive(self, msg, cid=None):
        t = msg.get('conntype', 'classic')
        if t not in self.peer.conntypes:
            self.peer.close_connection('unknownconntype', cid)
            return
        self.peer.clients[cid].conntype = t
        self.peer.conntypes[t].init(cid)

    receive.__noautodoc__ = True


class HandshakePacket(SmartPacket):
    __doc__ = '\n    Internal packet sent by the server to synchronize the registry.\n    \n    Additionally, the version information is sent and checked.\n    \n    If the :confval:`net.registry.autosync` config value is true, the registry sent by the server will be adapted to the client.\n    \n    Note that only IDs are synced to names, objects will not be affected.\n    '
    state = STATE_HANDSHAKE_WAIT1
    side = SIDE_CLIENT
    invalid_action = 'close'

    def receive(self, msg, cid=None):
        if msg['version'] != version.VERSION:
            pass
        if msg['protoversion'] != version.PROTOVERSION:
            self.peer.close_connection(cid, 'protoversionmismatch')
            return
        if self.peer.cfg['net.registry.autosync']:
            if msg['registry'].keys() != self.peer.registry.reg_int_str.inv.keys():
                if self.peer.cfg['net.registry.missingpacketaction'] == 'closeconnection':
                    self.peer.close_connection(cid, 'packetregmismatch')
                    return
                if self.peer.cfg['net.registry.missingpacketaction'] == 'ignore':
                    pass
            for name, pid in msg['registry'].items():
                if name in self.peer.registry.reg_int_str.inv:
                    obj = self.peer.registry.getObj(name)
                    opid = self.peer.registry.getInt(name)
                    del self.peer.registry.reg_int_str[opid]
                    del self.peer.registry.reg_int_obj[opid]
                    self.peer.registry.reg_int_str[pid] = name
                    self.peer.registry.reg_int_obj[pid] = obj

        self.peer.send_message('peng3dnet:internal.handshake.accept', {'success': True})
        self.peer.on_handshake_complete()
        with self.peer._connected_condition:
            self.peer._connected_condition.notify_all()

    receive.__noautodoc__ = True


class HandshakeAcceptPacket(SmartPacket):
    __doc__ = '\n    Internal packet sent by the client to indicate a successful handshake.\n    \n    Once this packet has been sent or received, the connection is established and can be used.\n    '
    state = STATE_HANDSHAKE_WAIT1
    side = SIDE_SERVER
    invalid_action = 'close'

    def receive(self, msg, cid=None):
        if msg['success']:
            self.peer.clients[cid].on_handshake_complete()

    receive.__noautodoc__ = True


class CloseConnectionPacket(Packet):
    __doc__ = '\n    Internal packet to be sent to indicate that a connection is about to be closed.\n    \n    Usually includes a reason in the ``reason`` field.\n    \n    This packet can be sent at any time, regardless of connection state or type.\n    '

    def receive(self, msg, cid=None):
        if isinstance(msg, dict):
            reason = msg.get('reason', None)
        else:
            reason = None
        if cid is None:
            self.peer.close(reason=reason)
        else:
            client = self.peer.clients[cid]
            client.close(reason)

    receive.__noautodoc__ = True