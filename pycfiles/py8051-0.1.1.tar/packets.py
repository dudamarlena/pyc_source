# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/py80211/packets.py
# Compiled at: 2012-12-06 19:26:11
from binascii import a2b_hex
import random

class Generator(object):
    """
    A collection of code for building 802.11 packets
    This code allows building both valid 802.11 packets as
    well as malformed packets
    """

    def __init__(self):
        """
        intialize packet hex values
        """
        self.packetTypes = {'deauth': [
                    0, 12], 
           'disass': [
                    0, 10], 
           'auth': [
                  0, 11], 
           'assos': [
                   0, 0], 
           'data': [
                  2, 0], 
           'reass': [
                   0, 3]}
        self.packetBcast = {'oldbcast': '\x00\x00\x00\x00\x00\x00', 
           'l2': b'\xff\xff\xff\xff\xff\xff', 
           'ipv6m': '33\x00\x00\x00\x16', 
           'stp': b'\x01\x80\xc2\x00\x00\x00', 
           'cdp': b'\x01\x00\x0c\xcc\xcc\xcc', 
           'cstp': b'\x01\x00\x0c\xcc\xcc\xcd', 
           'stpp': b'\x01\x80\xc2\x00\x00\x08', 
           'oam': b'\x01\x80\xc2\x00\x00\x02', 
           'ipv4m': b'\x01\x00^\x00\x00\xcd', 
           'ota': b'\x01\x0b\x85\x00\x00\x00'}
        self.deauthPacketReason = [
         '\n\x00',
         '\x01\x00',
         '\x05\x00',
         '\x04\x00',
         '\x08\x00',
         '\x02\x00']
        self.capabilities = {'xmas': self.bit2hex('1111111111111111'), 
           'apnw': self.bit2hex('1100000000000001'), 
           'apw': self.bit2hex('1000110000000001'), 
           'empty': self.bit2hex('0000000000000000')}

    def reassPacketEngine(self, allow_bcast, destination_addr, source_addr, bss_id_addr, channel, frameType=[
 'reass']):
        """
        Generate a reassoication packet
        """
        return self.authPacketEngine(allow_bcast, destination_addr, source_addr, bss_id_addr, channel, frameType=['reass'])

    def authPacketEngine(self, allow_bcast, destination_addr, source_addr, bss_id_addr, channel, frameType=[
 'auth', 'assos']):
        """
        Build each packet based on options
        Options are packets with broadcast address or no broadcast addresses
        allow_bcast is a boolen var on if bcast addresses are allowed to be used
        destination_addr is expecting a string mac addy in format of "xx:xx:xx:xx:xx:xx"
        source_addr is expecting a string mac addy in format of "xx:xx:xx:xx:xx:xx"
        bss_id_addr is expecing the bssid mac addy in format of "xx:xx:xx:xx:xx:xx"`
        channel is expected as int, no check is done if its a valid 802.11 channel
        """
        packets = []
        channel = int(channel)
        if allow_bcast == True:
            for ptype in frameType:
                for bcast in self.packetBcast:
                    packets.append([
                     self.authBuildPacket(self.packetTypes[ptype], destination_addr, self.packetBcast[bcast], bss_id_addr, ptype),
                     channel, source_addr])

        if allow_bcast == False:
            for ptype in frameType:
                packets.append([
                 self.authBuildPacket(self.packetTypes[ptype], destination_addr, source_addr, bss_id_addr),
                 channel, source_addr])

        return packets

    def authBuildPacket(self, bptype, dstAddr, srcAddr, bssid, ptype):
        """
        Constructs the packets to be sent
        ptype = expected packet type
        """
        packet = self.genPtype(bptype)
        packet.append('\x00\x00')
        packet.append(dstAddr)
        packet.append(srcAddr)
        packet.append(bssid)
        packet.append('\x10\x00')
        if ptype == 'assos':
            packet.append(self.randomDictObj(self.capabilities))
            packet.append('\x01\x00')
            packet.append('\x00\x00')
        else:
            packet.append('\x00\x00\x01\x00\x00\x00')
        return ('').join(packet)

    def deauthPacketEngine(self, allow_bcast, destination_addr, source_addr, bss_id_addr, channel, frameType=[
 'deauth', 'disass']):
        """
        Build each packet based on options
        Options are packets with broadcast address
        or no broadcast addresses
        allow_bcast is a boolen var on if bcast addresses are allowed to be used
        destination_addr is expecting a string mac addy in format of "xx:xx:xx:xx:xx:xx"
        source_addr is expecting a string mac addy in format of "xx:xx:xx:xx:xx:xx"
        bss_id_addr is expecing the bssid mac addy in format of "xx:xx:xx:xx:xx:xx"
        channel is expected as int, no check is done if its a valid 802.11 channel
        a list of frames types to send, these can be overloaded
        """
        packets = []
        destination_addr = destination_addr
        source_addr = source_addr
        bss_id_addr = bss_id_addr
        channel = int(channel)
        if allow_bcast == False:
            for btype in frameType:
                packets.append([
                 self.deauthBuildPacket(self.packetTypes[btype], destination_addr, source_addr, bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                 channel])
                packets.append([
                 self.deauthBuildPacket(self.packetTypes[btype], source_addr, destination_addr, bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                 channel])

        if allow_bcast == True:
            for btype in frameType:
                packets.append([
                 self.deauthBuildPacket(self.packetTypes[btype], destination_addr, source_addr, bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                 channel])
                packets.append([
                 self.deauthBuildPacket(self.packetTypes[btype], self.source_addr, self.destination_addr, self.bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                 channel])
                for bcast in self.packetBcast:
                    packets.append([
                     self.deauthBuildPacket(self.packetTypes[btype], self.packetBcast[bcast], source_addr, bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                     channel])
                    packets.append([
                     self.deauthBuildPacket(self.packetTypes[btype], source_addr, self.packetBcast[bcast], bss_id_addr, self.randomDictObj(self.deauthPacketReason)),
                     channel])

        return packets

    def deauthBuildPacket(self, btype, dstAddr, srcAddr, bssid, reasonCode):
        """
        Constructs the deauth/disassoicate packets to be sent
        """
        packet = self.genPtype(btype)
        packet.append('\x00\x00')
        packet.append(dstAddr)
        packet.append(srcAddr)
        packet.append(bssid)
        packet.append('pj')
        packet.append(reasonCode)
        return ('').join(packet)

    def wdsBuildPacket(self, btype, dstAddr, srcAddr, bssid, reasonCode):
        """
        Contructs the WDS 4 address packet to be sent
        """
        packet = self.genPtype(btype)
        packet.append('\x00\x00')
        packet.append(dstAddr)
        packet.append(srcAddr)
        packet.append(bssid)
        packet.append('pj')
        packet.append(srcAddr)
        return ('').join(packet)

    def randomDictObj(self, dictObject):
        """
        provide a random object value from a given dictionary
        dictObject = Dictionary object to pull random values from
        """
        dictObjectList = dictObject.values()
        return dictObjectList[random.randrange(0, len(dictObjectList, 1))]

    def randomMac(self):
        """
        # really not needed replaced by randomDictOjb
        # left in for the time being since its not being used
        # will most likely delete
        return a random mac address from self.packetBcast
        """
        return self.packetBcast.values()[random.randrange(0, len(self.packetBcast.values(), 1))]

    def convertHex(self, mac):
        """
        # set for removal?
        convert a mac address to hex
        """
        return a2b_hex(mac.replace(':', ''))

    def randDeauthReason(self):
        """
        #set for removal
        Generate a random reason code for the kick
        """
        return self.deauthPacketReason[random.randrange(0, len(self.deauthPacketReason), 1)]

    def bit2hex(self, bits):
        """
        convert a string of bits to hex... the easy way
        string of bits to base 2 returns and int
        then preform an chr on the int
        currently expects 16 bits
        """
        fbit = int(bits[0:8], 2)
        sbit = int(bits[8:16], 2)
        return chr(fbit) + chr(sbit)

    def genPtype(self, ptype, fromds=False):
        """
        generate a framecontrol in little endian
        ptype is list [type,subtype] as int
        if fromds is false then packet is from client to ap
        if fromds is true then packet is from ap to clinet
        returns 2 bytes as string
        """
        pbyte = 0 | int(ptype[0]) << 2
        pbyte = pbyte | int(ptype[1]) << 4
        if fromds is True:
            flags = '\x02'
        else:
            flags = '\x01'
        return pbyte + flags


if __name__ == '__main__':
    for bits in Generator().capabilities:
        pass