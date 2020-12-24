# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/intro/intro_socket.py
# Compiled at: 2010-06-01 14:13:58
import sys, time, struct
from socket import *
import yaml
from dust.crypto.curve import *
from dust.intro.intro_packet import IntroPacket
from dust.core.util import encodeAddress

class intro_socket:

    def __init__(self, keys, socket=None):
        self.keys = keys
        self.pubkey = keys.getKeypair().public
        if socket:
            self.sock = socket
        else:
            self.sock = None
        self.address = None
        return

    def bind(self, address):
        print('binding', address)
        self.address = address

    def iconnect(self, invite):
        self.invite = invite

    def isend(self):
        if not self.invite:
            print('No invite')
            return
        else:
            if not self.sock:
                if self.invite.v6:
                    self.sock = socket(AF_INET6, SOCK_DGRAM)
                else:
                    self.sock = socket(AF_INET, SOCK_DGRAM)
            if self.address:
                try:
                    self.sock.bind(self.address)
                except:
                    if self.invite.v6:
                        self.sock.bind(('::', self.address[1]))
                    else:
                        self.sock.bind(('', self.address[1]))

            packet = IntroPacket()
            packet.createIntroPacket(self.invite.secret, self.invite.id, self.pubkey, self.keys.entropy)
            addr = (self.invite.ip, self.invite.port)
            self.sock.sendto(packet.packet, 0, addr)
            self.invite = None
            return