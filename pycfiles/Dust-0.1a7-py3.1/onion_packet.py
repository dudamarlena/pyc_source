# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/extensions/onion/onion_packet.py
# Compiled at: 2010-06-01 14:13:33
from dust.core.data_packet import DataPacket
from dust.core.util import splitFields
SENDER_LENGTH = 32
RECEIVER_LENGTH = 32

class OnionPacket(DataPacket):

    def __init__(self):
        DataPacket.__init__(self)
        self.sender = None
        self.receiver = None
        return

    def createOnionPacket(self, keypair, receiver, data, entropy):
        self.sender = keypair.public.bytes
        self.receiver = receiver
        sk = keypair.createSession(Key(self.receiver, False))
        self.createDataPacket(sk, data, entropy)
        self.packet = self.sender + self.receiver + self.packet

    def decodeOnionPacket(self, keypair, packet):
        self.sender, self.receiver, packet = splitFields(packet, [SENDER_LENGTH, RECEIVER_LENGTH])
        if keypair.public.bytes != send.receiver:
            print('Error! Onion packet meant for a different receiver. Keypair does not match')
            return
        sk = keypair.createSession(Key(self.sender, False))
        self.decodeDataPacket(sk, packet)