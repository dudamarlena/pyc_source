# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/conntypes.py
# Compiled at: 2017-12-12 17:57:07
# Size of source mod 2**32: 4729 bytes
__all__ = [
 'ConnectionType', 'ClassicConnectionType']
from . import version
from .constants import *

class ConnectionType(object):
    __doc__ = '\n    Class representing a Connection Type implementation.\n    \n    Connection Types are identified by their name, usually a lowercase string.\n    \n    See :py:class:`~peng3dnet.net.Client()` for how to specify the connection type used.\n    \n    To use a custom connection type, it must be registered on both server and client via\n    :py:meth:`Server.addConnType() <peng3dnet.net.Server.addConnType>` or\n    :py:meth:`Client.addConnType() <peng3dnet.net.Client.addConnType>`\\ , respectively.\n    \n    ``peer`` is an instance of either :py:class:`~peng3dnet.net.Client()` or\n    :py:class:`~peng3dnet.net.Server()`\\ .\n    \n    Note that a single instance of this class will be shared between all connections\n    of the type implemented by this class. Distinguishing single connections is\n    possible via the ``cid`` parameter given to most methods. On the client side,\n    this parameter will always be ``None``\\ .\n    '

    def __init__(self, peer):
        self.peer = peer

    def init(self, cid):
        r"""
        Called when the :py:class:`~peng3dnet.packet.internal.SetTypePacket()`
        is received on the server side, or sent on the client side.
        
        Detecting which side of the connection is managed can be done by checking
        the ``cid`` parameter, if it is ``None``\ , the client side is represented,
        else it represents the ID of the connected client.
        """
        pass

    def receive(self, msg, pid, flags, cid):
        r"""
        Called whenever a packet is received via connection of the type represented by this class.
        
        ``msg`` is the already decoded message or payload.
        
        ``pid`` is the ID of the packet type.
        
        ``flags`` is the flags portion of the header, containing a bitfield with various internal flags.
        
        ``cid`` is the ID of the connected peer, if it is ``None``\ , the peer is a server.
        
        If the return value of this method equals to ``True``\ , further processing of the packet will be prevented.
        """
        return False

    def send(self, data, pid, cid):
        r"""
        Called whenever a packet has been sent via a connection of the type represented by this class.
        
        ``data`` is the fully encoded data that has been sent.
        
        ``pid`` is the packet type, as received by either
        :py:meth:`Server.send_message() <peng3dnet.net.Server.send_message>` or
        :py:meth:`Client.send_message() <peng3dnet.net.Client.send_message>`\ .
        
        ``cid`` is the ID of the connected peer, it if is ``None``\ , the peer is a server.
        
        If the return value of this method equals to ``True``\ , no further event handlers will be called.
        """
        return False


class ClassicConnectionType(ConnectionType):
    __doc__ = '\n    Classic Connection Type representing a typical connection.\n    \n    Currently adds no further processing to packets and starts a handshake by sending a :py:class:`~peng3dnet.packet.internal.HandshakePacket()` from the server to the client.\n    \n    The handshake allows the client to copy the registry of the server, preventing bugs with mismatching packet IDs.\n    '

    def init(self, cid):
        if cid is not None:
            self.peer.clients[cid].state = STATE_HANDSHAKE_WAIT1
            self.peer.send_message('peng3dnet:internal.handshake', {'version':version.VERSION,  'protoversion':version.PROTOVERSION,  'registry':dict(self.peer.registry.reg_int_str.inv)}, cid)
        else:
            if cid is None:
                self.peer.remote_state = STATE_HANDSHAKE_WAIT1

    init.__noautodoc__ = True