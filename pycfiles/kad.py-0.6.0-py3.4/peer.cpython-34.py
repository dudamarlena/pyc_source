# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kad/peer.py
# Compiled at: 2017-12-29 11:36:17
# Size of source mod 2**32: 3161 bytes
import hashlib, json
from .hashing import hash_function

class Peer(object):
    __doc__ = ' DHT Peer Information'

    def __init__(self, host, port, id, info):
        self.host, self.port, self.id, self.info = (host, port, id, info)

    def astriple(self):
        return (
         self.host, self.port, self.id, self.info)

    def asquad(self):
        return (
         self.host, self.port, self.id, self.info)

    def address(self):
        return (
         self.host, self.port)

    def __repr__(self):
        return repr(self.astriple())

    def _sendmessage(self, message, sock=None, peer_id=None, peer_info=None, lock=None):
        message['peer_id'] = peer_id
        message['peer_info'] = peer_info
        encoded = json.dumps(message)
        if sock:
            if lock:
                with lock:
                    sock.sendto(encoded.encode('ascii'), (self.host, self.port))
            else:
                sock.sendto(encoded.encode('ascii'), (self.host, self.port))

    def ping(self, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'ping'}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def pong(self, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'pong'}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def store(self, key, value, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'store', 
         'id': key, 
         'value': value}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def find_node(self, id, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'find_node', 
         'id': id, 
         'rpc_id': rpc_id}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def found_nodes(self, id, nearest_nodes, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'found_nodes', 
         'id': id, 
         'nearest_nodes': nearest_nodes, 
         'rpc_id': rpc_id}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def find_value(self, id, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'find_value', 
         'id': id, 
         'rpc_id': rpc_id}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)

    def found_value(self, id, value, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {'message_type': 'found_value', 
         'id': id, 
         'value': value, 
         'rpc_id': rpc_id}
        self._sendmessage(message, socket, peer_id=peer_id, peer_info=peer_info, lock=lock)