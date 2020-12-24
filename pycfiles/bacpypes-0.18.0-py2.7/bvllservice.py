# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/bvllservice.py
# Compiled at: 2020-01-29 15:49:50
"""
BACnet Virtual Link Layer Service
"""
import sys, struct
from .settings import settings
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .udp import UDPDirector
from .task import OneShotTask, RecurringTask
from .comm import Client, Server, bind, ServiceAccessPoint, ApplicationServiceElement
from .pdu import Address, LocalBroadcast, PDU, unpack_ip_addr
from .bvll import BVLPDU, DeleteForeignDeviceTableEntry, DistributeBroadcastToNetwork, FDTEntry, ForwardedNPDU, OriginalBroadcastNPDU, OriginalUnicastNPDU, ReadBroadcastDistributionTable, ReadBroadcastDistributionTableAck, ReadForeignDeviceTable, ReadForeignDeviceTableAck, RegisterForeignDevice, Result, WriteBroadcastDistributionTable, bvl_pdu_types
_debug = 0
_log = ModuleLogger(globals())

class _MultiplexClient(Client):

    def __init__(self, mux):
        Client.__init__(self)
        self.multiplexer = mux

    def confirmation(self, pdu):
        self.multiplexer.confirmation(self, pdu)


class _MultiplexServer(Server):

    def __init__(self, mux):
        Server.__init__(self)
        self.multiplexer = mux

    def indication(self, pdu):
        self.multiplexer.indication(self, pdu)


@bacpypes_debugging
class UDPMultiplexer():

    def __init__(self, addr=None, noBroadcast=False):
        if _debug:
            UDPMultiplexer._debug('__init__ %r noBroadcast=%r', addr, noBroadcast)
        specialBroadcast = False
        if addr is None:
            self.address = Address()
            self.addrTuple = ('', 47808)
            self.addrBroadcastTuple = ('255.255.255.255', 47808)
        else:
            if isinstance(addr, Address):
                self.address = addr
            else:
                self.address = Address(addr)
            self.addrTuple = self.address.addrTuple
            self.addrBroadcastTuple = self.address.addrBroadcastTuple
            if not self.addrBroadcastTuple:
                noBroadcast = True
            elif self.addrTuple == self.addrBroadcastTuple:
                self.addrBroadcastTuple = ('255.255.255.255', self.addrTuple[1])
            else:
                specialBroadcast = True
        if _debug:
            UDPMultiplexer._debug('    - address: %r', self.address)
            UDPMultiplexer._debug('    - addrTuple: %r', self.addrTuple)
            UDPMultiplexer._debug('    - addrBroadcastTuple: %r', self.addrBroadcastTuple)
            UDPMultiplexer._debug('    - route_aware: %r', settings.route_aware)
        self.direct = _MultiplexClient(self)
        self.directPort = UDPDirector(self.addrTuple)
        bind(self.direct, self.directPort)
        if specialBroadcast and not noBroadcast and sys.platform in ('linux2', 'darwin'):
            self.broadcast = _MultiplexClient(self)
            self.broadcastPort = UDPDirector(self.addrBroadcastTuple, reuse=True)
            bind(self.broadcast, self.broadcastPort)
        else:
            self.broadcast = None
            self.broadcastPort = None
        self.annexH = _MultiplexServer(self)
        self.annexJ = _MultiplexServer(self)
        return

    def close_socket(self):
        if _debug:
            UDPMultiplexer._debug('close_socket')
        self.directPort.close_socket()
        if self.broadcastPort:
            self.broadcastPort.close_socket()

    def indication(self, server, pdu):
        if _debug:
            UDPMultiplexer._debug('indication %r %r', server, pdu)
        if pdu.pduDestination.addrType == Address.localBroadcastAddr:
            dest = self.addrBroadcastTuple
            if _debug:
                UDPMultiplexer._debug('    - requesting local broadcast: %r', dest)
            if not dest:
                return
        elif pdu.pduDestination.addrType == Address.localStationAddr:
            dest = unpack_ip_addr(pdu.pduDestination.addrAddr)
            if _debug:
                UDPMultiplexer._debug('    - requesting local station: %r', dest)
        else:
            raise RuntimeError('invalid destination address type')
        self.directPort.indication(PDU(pdu, destination=dest))

    def confirmation(self, client, pdu):
        if _debug:
            UDPMultiplexer._debug('confirmation %r %r', client, pdu)
        if pdu.pduSource == self.addrTuple:
            if _debug:
                UDPMultiplexer._debug('    - from us!')
            return
        src = Address(pdu.pduSource)
        if client is self.direct:
            dest = self.address
        else:
            if client is self.broadcast:
                dest = LocalBroadcast()
            else:
                raise RuntimeError('confirmation mismatch')
            if pdu.pduData or _debug:
                UDPMultiplexer._debug('    - no data')
            return
        msg_type = struct.unpack('B', pdu.pduData[:1])[0]
        if _debug:
            UDPMultiplexer._debug('    - msg_type: %r', msg_type)
        if msg_type == 1:
            if self.annexH.serverPeer:
                self.annexH.response(PDU(pdu, source=src, destination=dest))
        elif msg_type == 129:
            if self.annexJ.serverPeer:
                self.annexJ.response(PDU(pdu, source=src, destination=dest))
        else:
            UDPMultiplexer._warning('unsupported message')


@bacpypes_debugging
class BTR(Client, Server, DebugContents):
    _debug_contents = ('peers+', )

    def __init__(self, cid=None, sid=None):
        """An Annex-H BACnet Tunneling Router node."""
        if _debug:
            BTR._debug('__init__ cid=%r sid=%r', cid, sid)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        self.peers = {}

    def indication(self, pdu):
        if _debug:
            BTR._debug('indication %r', pdu)
        if pdu.pduDestination.addrType == Address.localStationAddr:
            if pdu.pduDestination not in self.peers:
                return
            self.request(pdu)
        elif pdu.pduDestination.addrType == Address.localBroadcastAddr:
            for peerAddr in self.peers.keys():
                xpdu = PDU(pdu.pduData, destination=peerAddr)
                self.request(xpdu)

        else:
            raise RuntimeError('invalid destination address type (2)')

    def confirmation(self, pdu):
        if _debug:
            BTR._debug('confirmation %r', pdu)
        if pdu.pduSource not in self.peers:
            BTR._warning('not a peer: %r', pdu.pduSource)
            return
        self.response(pdu)

    def add_peer(self, peerAddr, networks=None):
        """Add a peer and optionally provide a list of the reachable networks."""
        if _debug:
            BTR._debug('add_peer %r networks=%r', peerAddr, networks)
        if peerAddr in self.peers:
            if not networks:
                networks = []
            else:
                self.peers[peerAddr].extend(networks)
        else:
            if not networks:
                networks = []
            self.peers[peerAddr] = networks

    def delete_peer(self, peerAddr):
        """Delete a peer."""
        if _debug:
            BTR._debug('delete_peer %r', peerAddr)
        del self.peers[peerAddr]


@bacpypes_debugging
class AnnexJCodec(Client, Server):

    def __init__(self, cid=None, sid=None):
        if _debug:
            AnnexJCodec._debug('__init__ cid=%r sid=%r', cid, sid)
        Client.__init__(self, cid)
        Server.__init__(self, sid)

    def indication(self, rpdu):
        if _debug:
            AnnexJCodec._debug('indication %r', rpdu)
        bvlpdu = BVLPDU()
        rpdu.encode(bvlpdu)
        pdu = PDU()
        bvlpdu.encode(pdu)
        self.request(pdu)

    def confirmation(self, pdu):
        if _debug:
            AnnexJCodec._debug('confirmation %r', pdu)
        bvlpdu = BVLPDU()
        bvlpdu.decode(pdu)
        rpdu = bvl_pdu_types[bvlpdu.bvlciFunction]()
        rpdu.decode(bvlpdu)
        self.response(rpdu)


@bacpypes_debugging
class BIPSAP(ServiceAccessPoint):

    def __init__(self, sap=None):
        """A BIP service access point."""
        if _debug:
            BIPSAP._debug('__init__ sap=%r', sap)
        ServiceAccessPoint.__init__(self, sap)

    def sap_indication(self, pdu):
        if _debug:
            BIPSAP._debug('sap_indication %r', pdu)
        self.request(pdu)

    def sap_confirmation(self, pdu):
        if _debug:
            BIPSAP._debug('sap_confirmation %r', pdu)
        self.request(pdu)


@bacpypes_debugging
class BIPSimple(BIPSAP, Client, Server):

    def __init__(self, sapID=None, cid=None, sid=None):
        """A BIP node."""
        if _debug:
            BIPSimple._debug('__init__ sapID=%r cid=%r sid=%r', sapID, cid, sid)
        BIPSAP.__init__(self, sapID)
        Client.__init__(self, cid)
        Server.__init__(self, sid)

    def indication(self, pdu):
        if _debug:
            BIPSimple._debug('indication %r', pdu)
        if pdu.pduDestination.addrType == Address.localStationAddr:
            xpdu = OriginalUnicastNPDU(pdu, destination=pdu.pduDestination, user_data=pdu.pduUserData)
            if _debug:
                BIPSimple._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif pdu.pduDestination.addrType == Address.localBroadcastAddr:
            xpdu = OriginalBroadcastNPDU(pdu, destination=pdu.pduDestination, user_data=pdu.pduUserData)
            if _debug:
                BIPSimple._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        else:
            BIPSimple._warning('invalid destination address: %r', pdu.pduDestination)

    def confirmation(self, pdu):
        if _debug:
            BIPSimple._debug('confirmation %r', pdu)
        if isinstance(pdu, Result):
            self.sap_response(pdu)
        elif isinstance(pdu, ReadBroadcastDistributionTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, ReadForeignDeviceTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, OriginalUnicastNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=pdu.pduDestination, user_data=pdu.pduUserData)
            if _debug:
                BIPSimple._debug('    - xpdu: %r', xpdu)
            self.response(xpdu)
        elif isinstance(pdu, OriginalBroadcastNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=LocalBroadcast(), user_data=pdu.pduUserData)
            if _debug:
                BIPSimple._debug('    - xpdu: %r', xpdu)
            self.response(xpdu)
        elif isinstance(pdu, ForwardedNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.bvlciAddress, destination=LocalBroadcast(), user_data=pdu.pduUserData)
            if _debug:
                BIPSimple._debug('    - xpdu: %r', xpdu)
            self.response(xpdu)
        elif isinstance(pdu, WriteBroadcastDistributionTable):
            xpdu = Result(code=16, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTable):
            xpdu = Result(code=32, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, RegisterForeignDevice):
            xpdu = Result(code=48, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTable):
            xpdu = Result(code=64, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, DeleteForeignDeviceTableEntry):
            xpdu = Result(code=80, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, DistributeBroadcastToNetwork):
            xpdu = Result(code=96, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        else:
            BIPSimple._warning('invalid pdu type: %s', type(pdu))


@bacpypes_debugging
class BIPForeign(BIPSAP, Client, Server, OneShotTask, DebugContents):
    _debug_contents = ('registrationStatus', 'bbmdAddress', 'bbmdTimeToLive')

    def __init__(self, addr=None, ttl=None, sapID=None, cid=None, sid=None):
        """A BIP node."""
        if _debug:
            BIPForeign._debug('__init__ addr=%r ttl=%r sapID=%r cid=%r sid=%r', addr, ttl, sapID, cid, sid)
        BIPSAP.__init__(self, sapID)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        OneShotTask.__init__(self)
        self.registrationStatus = -1
        self.bbmdAddress = None
        self.bbmdTimeToLive = None
        if addr:
            if ttl is None:
                raise RuntimeError('BBMD address and time-to-live must both be specified')
            self.register(addr, ttl)
        return

    def indication(self, pdu):
        if _debug:
            BIPForeign._debug('indication %r', pdu)
        if pdu.pduDestination.addrType == Address.localStationAddr:
            xpdu = OriginalUnicastNPDU(pdu, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduDestination
            self.request(xpdu)
        elif pdu.pduDestination.addrType == Address.localBroadcastAddr:
            if self.registrationStatus != 0:
                if _debug:
                    BIPForeign._debug('    - packet dropped, unregistered')
                return
            xpdu = DistributeBroadcastToNetwork(pdu, user_data=pdu.pduUserData)
            xpdu.pduDestination = self.bbmdAddress
            self.request(xpdu)
        else:
            BIPForeign._warning('invalid destination address: %r', pdu.pduDestination)

    def confirmation(self, pdu):
        if _debug:
            BIPForeign._debug('confirmation %r', pdu)
        if isinstance(pdu, Result):
            if self.registrationStatus == -2:
                return
            if pdu.pduSource != self.bbmdAddress:
                if _debug:
                    BIPForeign._debug('    - packet dropped, not from the BBMD')
                return
            self.registrationStatus = pdu.bvlciResultCode
            if pdu.bvlciResultCode == 0:
                self.install_task(delta=self.bbmdTimeToLive)
            return
        if isinstance(pdu, OriginalUnicastNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=pdu.pduDestination, user_data=pdu.pduUserData)
            self.response(xpdu)
        elif isinstance(pdu, ForwardedNPDU):
            if self.registrationStatus != 0:
                if _debug:
                    BIPForeign._debug('    - packet dropped, unregistered')
                return
            if pdu.pduSource != self.bbmdAddress:
                if _debug:
                    BIPForeign._debug('    - packet dropped, not from the BBMD')
                return
            xpdu = PDU(pdu.pduData, source=pdu.bvlciAddress, destination=LocalBroadcast(), user_data=pdu.pduUserData)
            self.response(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, ReadForeignDeviceTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, WriteBroadcastDistributionTable):
            xpdu = Result(code=16, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTable):
            xpdu = Result(code=32, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, RegisterForeignDevice):
            xpdu = Result(code=48, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTable):
            xpdu = Result(code=64, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, DeleteForeignDeviceTableEntry):
            xpdu = Result(code=80, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, DistributeBroadcastToNetwork):
            xpdu = Result(code=96, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, OriginalBroadcastNPDU):
            if _debug:
                BIPForeign._debug('    - packet dropped')
        else:
            BIPForeign._warning('invalid pdu type: %s', type(pdu))

    def register(self, addr, ttl):
        """Initiate the process of registering with a BBMD."""
        if ttl <= 0:
            raise ValueError('time-to-live must be greater than zero')
        if isinstance(addr, Address):
            self.bbmdAddress = addr
        else:
            self.bbmdAddress = Address(addr)
        self.bbmdTimeToLive = ttl
        self.install_task(when=0)

    def unregister(self):
        """Drop the registration with a BBMD."""
        pdu = RegisterForeignDevice(0)
        pdu.pduDestination = self.bbmdAddress
        self.request(pdu)
        self.registrationStatus = -2
        self.bbmdAddress = None
        self.bbmdTimeToLive = None
        return

    def process_task(self):
        """Called when the registration request should be sent to the BBMD."""
        pdu = RegisterForeignDevice(self.bbmdTimeToLive)
        pdu.pduDestination = self.bbmdAddress
        self.request(pdu)


@bacpypes_debugging
class BIPBBMD(BIPSAP, Client, Server, RecurringTask, DebugContents):
    _debug_contents = ('bbmdAddress', 'bbmdBDT+', 'bbmdFDT+')

    def __init__(self, addr, sapID=None, cid=None, sid=None):
        """A BBMD node."""
        if _debug:
            BIPBBMD._debug('__init__ %r sapID=%r cid=%r sid=%r', addr, sapID, cid, sid)
        BIPSAP.__init__(self, sapID)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        RecurringTask.__init__(self, 1000.0)
        self.bbmdAddress = addr
        self.bbmdBDT = []
        self.bbmdFDT = []
        self.install_task()

    def indication(self, pdu):
        if _debug:
            BIPBBMD._debug('indication %r', pdu)
        if pdu.pduDestination.addrType == Address.localStationAddr:
            xpdu = OriginalUnicastNPDU(pdu, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduDestination
            if _debug:
                BIPBBMD._debug('    - original unicast xpdu: %r', xpdu)
            self.request(xpdu)
        elif pdu.pduDestination.addrType == Address.localBroadcastAddr:
            xpdu = OriginalBroadcastNPDU(pdu, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduDestination
            if _debug:
                BIPBBMD._debug('    - original broadcast xpdu: %r', xpdu)
            self.request(xpdu)
            xpdu = ForwardedNPDU(self.bbmdAddress, pdu, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - forwarded xpdu: %r', xpdu)
            for bdte in self.bbmdBDT:
                if bdte != self.bbmdAddress:
                    xpdu.pduDestination = Address((bdte.addrIP | ~bdte.addrMask, bdte.addrPort))
                    BIPBBMD._debug('    - sending to peer: %r', xpdu.pduDestination)
                    self.request(xpdu)

            for fdte in self.bbmdFDT:
                xpdu.pduDestination = fdte.fdAddress
                if _debug:
                    BIPBBMD._debug('    - sending to foreign device: %r', xpdu.pduDestination)
                self.request(xpdu)

        else:
            BIPBBMD._warning('invalid destination address: %r', pdu.pduDestination)

    def confirmation(self, pdu):
        if _debug:
            BIPBBMD._debug('confirmation %r', pdu)
        if isinstance(pdu, Result):
            self.sap_response(pdu)
        elif isinstance(pdu, WriteBroadcastDistributionTable):
            xpdu = Result(code=16, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            if _debug:
                BIPBBMD._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTable):
            xpdu = ReadBroadcastDistributionTableAck(self.bbmdBDT, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            if _debug:
                BIPBBMD._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, ForwardedNPDU):
            if self.serverPeer:
                xpdu = PDU(pdu.pduData, source=pdu.bvlciAddress, destination=LocalBroadcast(), user_data=pdu.pduUserData)
                if _debug:
                    BIPBBMD._debug('    - upstream xpdu: %r', xpdu)
                self.response(xpdu)
            xpdu = ForwardedNPDU(pdu.bvlciAddress, pdu, destination=None, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - forwarded xpdu: %r', xpdu)
            if pdu.pduDestination.addrType == Address.localStationAddr:
                if _debug:
                    BIPBBMD._debug('    - unicast message')
                if self.bbmdAddress in self.bbmdBDT:
                    xpdu.pduDestination = LocalBroadcast()
                    if _debug:
                        BIPBBMD._debug('    - local broadcast')
                    self.request(xpdu)
            else:
                if pdu.pduDestination.addrType == Address.localBroadcastAddr:
                    if _debug:
                        BIPBBMD._debug('    - directed broadcast message')
                else:
                    BIPBBMD._warning('invalid destination address: %r', pdu.pduDestination)
                for fdte in self.bbmdFDT:
                    xpdu.pduDestination = fdte.fdAddress
                    if _debug:
                        BIPBBMD._debug('    - sending to foreign device: %r', xpdu.pduDestination)
                    self.request(xpdu)

        elif isinstance(pdu, RegisterForeignDevice):
            stat = self.register_foreign_device(pdu.pduSource, pdu.bvlciTimeToLive)
            xpdu = Result(code=stat, destination=pdu.pduSource, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTable):
            xpdu = ReadForeignDeviceTableAck(self.bbmdFDT, destination=pdu.pduSource, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, DeleteForeignDeviceTableEntry):
            stat = self.delete_foreign_device_table_entry(pdu.bvlciAddress)
            xpdu = Result(code=stat, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            if _debug:
                BIPBBMD._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, DistributeBroadcastToNetwork):
            if self.serverPeer:
                xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=LocalBroadcast(), user_data=pdu.pduUserData)
                if _debug:
                    BIPBBMD._debug('    - upstream xpdu: %r', xpdu)
                self.response(xpdu)
            xpdu = ForwardedNPDU(pdu.pduSource, pdu, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - forwarded xpdu: %r', xpdu)
            for bdte in self.bbmdBDT:
                if bdte == self.bbmdAddress:
                    xpdu.pduDestination = LocalBroadcast()
                    if _debug:
                        BIPBBMD._debug('    - local broadcast')
                    self.request(xpdu)
                else:
                    xpdu.pduDestination = Address((bdte.addrIP | ~bdte.addrMask, bdte.addrPort))
                    if _debug:
                        BIPBBMD._debug('    - sending to peer: %r', xpdu.pduDestination)
                    self.request(xpdu)

            for fdte in self.bbmdFDT:
                if fdte.fdAddress != pdu.pduSource:
                    xpdu.pduDestination = fdte.fdAddress
                    if _debug:
                        BIPBBMD._debug('    - sending to foreign device: %r', xpdu.pduDestination)
                    self.request(xpdu)

        elif isinstance(pdu, OriginalUnicastNPDU):
            if self.serverPeer:
                xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=pdu.pduDestination, user_data=pdu.pduUserData)
                if _debug:
                    BIPBBMD._debug('    - upstream xpdu: %r', xpdu)
                self.response(xpdu)
        elif isinstance(pdu, OriginalBroadcastNPDU):
            if self.serverPeer:
                xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=LocalBroadcast(), user_data=pdu.pduUserData)
                if _debug:
                    BIPBBMD._debug('    - upstream xpdu: %r', xpdu)
                self.response(xpdu)
            xpdu = ForwardedNPDU(pdu.pduSource, pdu, user_data=pdu.pduUserData)
            if _debug:
                BIPBBMD._debug('    - forwarded xpdu: %r', xpdu)
            for bdte in self.bbmdBDT:
                if bdte != self.bbmdAddress:
                    xpdu.pduDestination = Address((bdte.addrIP | ~bdte.addrMask, bdte.addrPort))
                    if _debug:
                        BIPBBMD._debug('    - sending to peer: %r', xpdu.pduDestination)
                    self.request(xpdu)

            for fdte in self.bbmdFDT:
                xpdu.pduDestination = fdte.fdAddress
                if _debug:
                    BIPBBMD._debug('    - sending to foreign device: %r', xpdu.pduDestination)
                self.request(xpdu)

        else:
            BIPBBMD._warning('invalid pdu type: %s', type(pdu))
        return

    def register_foreign_device(self, addr, ttl):
        """Add a foreign device to the FDT."""
        if _debug:
            BIPBBMD._debug('register_foreign_device %r %r', addr, ttl)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            for fdte in self.bbmdFDT:
                if addr == fdte.fdAddress:
                    break
            else:
                fdte = FDTEntry()
                fdte.fdAddress = addr
                self.bbmdFDT.append(fdte)

        fdte.fdTTL = ttl
        fdte.fdRemain = ttl + 5
        return 0

    def delete_foreign_device_table_entry(self, addr):
        if _debug:
            BIPBBMD._debug('delete_foreign_device_table_entry %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            stat = 0
            for i in range(len(self.bbmdFDT) - 1, -1, -1):
                if addr == self.bbmdFDT[i].fdAddress:
                    del self.bbmdFDT[i]
                    break

            stat = 80
        return stat

    def process_task(self):
        for i in range(len(self.bbmdFDT) - 1, -1, -1):
            fdte = self.bbmdFDT[i]
            fdte.fdRemain -= 1
            if fdte.fdRemain <= 0:
                if _debug:
                    BIPBBMD._debug('foreign device expired: %r', fdte.fdAddress)
                del self.bbmdFDT[i]

    def add_peer(self, addr):
        if _debug:
            BIPBBMD._debug('add_peer %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            for bdte in self.bbmdBDT:
                if addr == bdte:
                    break
            else:
                self.bbmdBDT.append(addr)

    def delete_peer(self, addr):
        if _debug:
            BIPBBMD._debug('delete_peer %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            for i in range(len(self.bbmdBDT) - 1, -1, -1):
                if addr == self.bbmdBDT[i]:
                    del self.bbmdBDT[i]
                    break


@bacpypes_debugging
class BIPNAT(BIPSAP, Client, Server, RecurringTask, DebugContents):
    _debug_contents = ('bbmdAddress', 'bbmdBDT+', 'bbmdFDT+')

    def __init__(self, addr, sapID=None, cid=None, sid=None):
        """A BBMD node that is the destination for NATed traffic."""
        if _debug:
            BIPNAT._debug('__init__ %r sapID=%r cid=%r sid=%r', addr, sapID, cid, sid)
        BIPSAP.__init__(self, sapID)
        Client.__init__(self, cid)
        Server.__init__(self, sid)
        RecurringTask.__init__(self, 1000.0)
        self.bbmdAddress = addr
        self.bbmdBDT = []
        self.bbmdFDT = []
        self.install_task()

    def indication(self, pdu):
        if _debug:
            BIPNAT._debug('indication %r', pdu)
        if pdu.pduDestination.addrType == Address.localStationAddr:
            xpdu = OriginalUnicastNPDU(pdu, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduDestination
            if _debug:
                BIPNAT._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif pdu.pduDestination.addrType == Address.localBroadcastAddr:
            xpdu = ForwardedNPDU(self.bbmdAddress, pdu, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - forwarded xpdu: %r', xpdu)
            for bdte in self.bbmdBDT:
                if bdte != self.bbmdAddress:
                    xpdu.pduDestination = Address((bdte.addrIP, bdte.addrPort))
                    BIPNAT._debug('        - sending to peer: %r', xpdu.pduDestination)
                    self.request(xpdu)

            for fdte in self.bbmdFDT:
                xpdu.pduDestination = fdte.fdAddress
                if _debug:
                    BIPNAT._debug('        - sending to foreign device: %r', xpdu.pduDestination)
                self.request(xpdu)

        else:
            BIPNAT._warning('invalid destination address: %r', pdu.pduDestination)

    def confirmation(self, pdu):
        if _debug:
            BIPNAT._debug('confirmation %r', pdu)
        if isinstance(pdu, Result):
            self.sap_response(pdu)
        elif isinstance(pdu, WriteBroadcastDistributionTable):
            xpdu = Result(code=99, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTable):
            xpdu = ReadBroadcastDistributionTableAck(self.bbmdBDT, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            if _debug:
                BIPNAT._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadBroadcastDistributionTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, ForwardedNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.bvlciAddress, destination=LocalBroadcast(), user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - upstream xpdu: %r', xpdu)
            self.response(xpdu)
            xpdu = ForwardedNPDU(pdu.bvlciAddress, pdu, destination=None, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - forwarded xpdu: %r', xpdu)
            for fdte in self.bbmdFDT:
                xpdu.pduDestination = fdte.fdAddress
                if _debug:
                    BIPNAT._debug('        - sending to foreign device: %r', xpdu.pduDestination)
                self.request(xpdu)

        elif isinstance(pdu, RegisterForeignDevice):
            stat = self.register_foreign_device(pdu.pduSource, pdu.bvlciTimeToLive)
            xpdu = Result(code=stat, destination=pdu.pduSource, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTable):
            xpdu = ReadForeignDeviceTableAck(self.bbmdFDT, destination=pdu.pduSource, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, ReadForeignDeviceTableAck):
            self.sap_response(pdu)
        elif isinstance(pdu, DeleteForeignDeviceTableEntry):
            stat = self.delete_foreign_device_table_entry(pdu.bvlciAddress)
            xpdu = Result(code=stat, user_data=pdu.pduUserData)
            xpdu.pduDestination = pdu.pduSource
            if _debug:
                BIPNAT._debug('    - xpdu: %r', xpdu)
            self.request(xpdu)
        elif isinstance(pdu, DistributeBroadcastToNetwork):
            xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=LocalBroadcast(), user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - upstream xpdu: %r', xpdu)
            self.response(xpdu)
            xpdu = ForwardedNPDU(pdu.pduSource, pdu, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - forwarded xpdu: %r', xpdu)
            for bdte in self.bbmdBDT:
                if bdte == self.bbmdAddress:
                    if _debug:
                        BIPNAT._debug('        - no local broadcast')
                else:
                    xpdu.pduDestination = Address((bdte.addrIP, bdte.addrPort))
                    if _debug:
                        BIPNAT._debug('        - sending to peer: %r', xpdu.pduDestination)
                    self.request(xpdu)

            for fdte in self.bbmdFDT:
                if fdte.fdAddress != pdu.pduSource:
                    xpdu.pduDestination = fdte.fdAddress
                    if _debug:
                        BIPNAT._debug('        - sending to foreign device: %r', xpdu.pduDestination)
                    self.request(xpdu)

        elif isinstance(pdu, OriginalUnicastNPDU):
            xpdu = PDU(pdu.pduData, source=pdu.pduSource, destination=pdu.pduDestination, user_data=pdu.pduUserData)
            if _debug:
                BIPNAT._debug('    - upstream xpdu: %r', xpdu)
            self.response(xpdu)
        elif isinstance(pdu, OriginalBroadcastNPDU):
            if _debug:
                BIPNAT._debug('    - original broadcast dropped')
        else:
            BIPNAT._warning('invalid pdu type: %s', type(pdu))
        return

    def register_foreign_device(self, addr, ttl):
        """Add a foreign device to the FDT."""
        if _debug:
            BIPNAT._debug('register_foreign_device %r %r', addr, ttl)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            for fdte in self.bbmdFDT:
                if addr == fdte.fdAddress:
                    break
            else:
                fdte = FDTEntry()
                fdte.fdAddress = addr
                self.bbmdFDT.append(fdte)

        fdte.fdTTL = ttl
        fdte.fdRemain = ttl + 5
        return 0

    def delete_foreign_device_table_entry(self, addr):
        if _debug:
            BIPNAT._debug('delete_foreign_device_table_entry %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            stat = 0
            for i in range(len(self.bbmdFDT) - 1, -1, -1):
                if addr == self.bbmdFDT[i].fdAddress:
                    del self.bbmdFDT[i]
                    break

            stat = 99
        return stat

    def process_task(self):
        for i in range(len(self.bbmdFDT) - 1, -1, -1):
            fdte = self.bbmdFDT[i]
            fdte.fdRemain -= 1
            if fdte.fdRemain <= 0:
                if _debug:
                    BIPNAT._debug('foreign device expired: %r', fdte.fdAddress)
                del self.bbmdFDT[i]

    def add_peer(self, addr):
        if _debug:
            BIPNAT._debug('add_peer %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            if self.bbmdBDT and addr == self.bbmdAddress:
                raise RuntimeError('add self to BDT as first address')
            for bdte in self.bbmdBDT:
                if addr == bdte:
                    break
            else:
                self.bbmdBDT.append(addr)

    def delete_peer(self, addr):
        if _debug:
            BIPNAT._debug('delete_peer %r', addr)
        if isinstance(addr, Address):
            pass
        else:
            if isinstance(addr, str):
                addr = Address(addr)
            else:
                raise TypeError('addr must be a string or an Address')
            for i in range(len(self.bbmdBDT) - 1, -1, -1):
                if addr == self.bbmdBDT[i]:
                    del self.bbmdBDT[i]
                    break


@bacpypes_debugging
class BVLLServiceElement(ApplicationServiceElement):

    def __init__(self, aseID=None):
        if _debug:
            BVLLServiceElement._debug('__init__ aseID=%r', aseID)
        ApplicationServiceElement.__init__(self, aseID)

    def indication(self, npdu):
        if _debug:
            BVLLServiceElement._debug('indication %r %r', npdu)
        fn = npdu.__class__.__name__
        if hasattr(self, fn):
            getattr(self, fn)(npdu)
        else:
            BVLLServiceElement._warning('no handler for %s', fn)

    def confirmation(self, npdu):
        if _debug:
            BVLLServiceElement._debug('confirmation %r %r', npdu)
        fn = npdu.__class__.__name__
        if hasattr(self, fn):
            getattr(self, fn)(npdu)
        else:
            BVLLServiceElement._warning('no handler for %s', fn)