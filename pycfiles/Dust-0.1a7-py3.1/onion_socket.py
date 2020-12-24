# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/extensions/onion/onion_socket.py
# Compiled at: 2010-06-01 15:24:25
import sys, time, struct
from socket import *
import yaml
from dust.crypto.curve import *
from dust.extensions.onion.onion_packet import OnionPacket
from dust.core.util import encodeAddress, encode
from dust.intro.intro import Introducer

class onion_socket:

    def __init__(self, keys, socket):
        self.keys = keys
        self.keypair = keys.getKeypair()
        self.sock = socket
        self.sessionKeys = {}
        self.remaining = None
        return

    def recvfrom(self, bufsize):
        if self.remaining:
            data, addr, endpoint = self.remaining
            self.remaining = None
        else:
            data, addr, endpoint = self.sock.recvfrom(bufsize)
        if not data:
            print('Onion: No data')
            return (None, None, None)
        packet = self.decodeOnionPacket(data)
        if not packet:
            print('Onion: No packet')
            return (None, None, None)
        else:
            if packet.remaining:
                self.remaining = (
                 packet.remaining, addr, packet.endpoint)
            if type(packet) == OnionPacket:
                return (packet.data, addr, packet.endpoint)
            else:
                print('Not a data packet')
                return (None, None, None)
            return

    def sendto(self, data, addr, endpoint):
        print('sendto ' + str(endpoint))
        packet = self.encodePacket(endpoint, data)
        print('Sending')
        print(packet)
        self.sock.sendto(packet.packet, 0, addr)

    def decodePacket(self, endpoint, data):
        packet = OnionPacket()
        packet.decodeOnionPacket(data)
        if packet.checkMac() and packet.checkTimestamp():
            return packet
        else:
            print('Integrity failed', packet.checkMac(), packet.checkTimestamp())
            print(packet)
            return
            return

    def encodePacket(self, endpoint, data):
        packet = OnionPacket()
        packet.createOnionPacket(self.keys.getKeypair(), endpoint, data, self.keys.entropy)
        return packet