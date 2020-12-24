# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/invite/invite.py
# Compiled at: 2010-06-01 14:16:34
import sys
from dust.core.util import encode, decode
from dust.invite.invite_packet import InviteMessage, InvitePacket

def createInvitePackage(pubkey, v6, tcp, port, number):
    ip = InvitePackage()
    ip.generate(pubkey, v6, tcp, port, number)
    return ip


def loadInvitePackage(filename, password):
    ip = InvitePackage()
    ip.load(filename, password)
    return ip


class InvitePackage:

    def __init__(self):
        self.invites = []

    def __str__(self):
        s = '['
        for invite in self.invites:
            s = s + str(invite) + ', '

        if len(s) > 1:
            s = s[:-2]
        s = s + ']'
        return s

    def getInviteWithId(self, id):
        for invite in self.invites:
            if invite.id == id:
                return invite

        return

    def getInviteForHost(self, tcp, address):
        for invite in self.invites:
            if invite.tcp == tcp and invite.ip == address[0] and invite.port == address[1]:
                return invite

        return

    def getInvitesForHost(self, tcp, address):
        results = []
        for invite in self.invites:
            if invite.tcp == tcp and invite.ip == address[0] and invite.port == address[1]:
                results.append(invite)
                continue

        return results

    def merge(self, ip):
        for invite in ip.invites:
            self.addInvite(invite)

    def addInvite(self, invite):
        if invite not in self.invites:
            self.invites.append(invite)

    def removeInvite(self, invite):
        self.invites.remove(invite)

    def generate(self, pubkey, v6, tcp, port, number, entropy):
        for x in range(number + 1):
            i = InviteMessage()
            i.generate(pubkey, v6, tcp, port, entropy)
            self.addInvite(i)

    def load(self, filename, password):
        try:
            f = open(filename, 'r')
        except:
            print('No such file', filename)
            return

        for line in f.readlines():
            data = decode(line.strip())
            packet = InvitePacket()
            packet.decodeInvitePacket(password, data)
            if packet.checkMac():
                self.addInvite(packet.invite)
            else:
                print('Mac check failed, possible a wrong password?')

        f.close()

    def save(self, filename, password, entropy):
        f = open(filename, 'w')
        for invite in self.invites:
            packet = InvitePacket()
            packet.createInvitePacket(password, invite, entropy)
            data = encode(packet.packet)
            f.write(data)
            f.write('\n')

        f.close()