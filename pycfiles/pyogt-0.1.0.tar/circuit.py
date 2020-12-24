# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/message/circuit.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from msgtypes import PackFlags

class Host(object):
    __module__ = __name__

    def __init__(self, context):
        self.ip = context[0]
        self.port = context[1]

    def __repr__(self):
        """return a string representation"""
        return str("Host: '%s:%s'" % (self.ip, self.port))

    def is_ok(self):
        if self.ip == None or self.port == None or self.ip == 0 or self.port == 0:
            return False
        return True

    def set_host_by_name(self, hostname):
        pass


class Circuit(object):
    """ This is used to keep track of a given circuit. It keeps statistics
        as well as circuit information. """
    __module__ = __name__

    def __init__(self, host, pack_in_id):
        self.host = host
        self.circuit_code = 0
        self.session_id = 0
        self.is_alive = True
        self.is_trusted = False
        self.is_blocked = False
        self.allow_timeout = True
        self.last_packet_out_id = 0
        self.last_packet_in_id = pack_in_id
        self.acks = []
        self.unacked_packets = {}
        self.unack_packet_count = 0
        self.unack_packet_bytes = 0
        self.final_retry_packets = {}
        self.final_packet_count = 0

    def next_packet_id(self):
        self.last_packet_out_id += 1
        return self.last_packet_out_id

    def prepare_packet(self, packet, flag=PackFlags.LL_NONE, retries=0):
        packet.send_flags = flag
        packet.retries = retries
        packet.packet_id = self.next_packet_id()
        ack_count = len(self.acks)
        if ack_count > 0 and packet.name != 'PacketAck':
            packet.send_flags |= PackFlags.LL_ACK_FLAG
            for packet_id in self.acks:
                packet.add_ack(packet_id)

        if flag == PackFlags.LL_RELIABLE_FLAG:
            self.add_reliable_packet(packet)

    def handle_packet(self, packet):
        for ack_packet_id in packet.acks:
            self.ack_reliable_packet(ack_packet_id)

        if packet.reliable == True:
            self.collect_ack(packet.packet_id)

    def ack_reliable_packet(self, packet_id):
        if packet_id in self.unacked_packets:
            del self.unacked_packets[packet_id]
            self.unack_packet_count -= 1
        if packet_id in self.final_retry_packets:
            del self.final_retry_packets[packet_id]
            self.final_packet_count -= 1

    def collect_ack(self, packet_id):
        """ set a packet_id that this circuit needs to eventually ack
            (need to send ack out)"""
        self.acks.append(packet_id)

    def add_reliable_packet(self, packet):
        """ add a packet that we want to be acked
            (want an incoming ack) """
        self.unack_packet_count += 1
        self.unacked_packets[packet.packet_id] = packet


class CircuitManager(object):
    """ Manages a collection of circuits and provides some higher-level
        functionality to do so. """
    __module__ = __name__

    def __init__(self):
        self.circuit_map = {}
        self.unacked_circuits = {}

    def get_unacked_circuits(self):
        pass

    def get_circuit(self, host):
        if (
         host.ip, host.port) in self.circuit_map:
            return self.circuit_map[(host.ip, host.port)]
        return

    def add_circuit(self, host, packet_in_id):
        circuit = Circuit(host, packet_in_id)
        self.circuit_map[(host.ip, host.port)] = circuit
        return circuit

    def remove_circuit_data(self, host):
        if (
         host.ip, host.port) in self.circuit_map:
            del self.circuit_map[(host.ip, host.port)]

    def is_circuit_alive(self, host):
        if (host.ip, host.port) not in self.circuit_map:
            return False
        circuit = self.circuit_map[(host.ip, host.port)]
        return circuit.is_alive