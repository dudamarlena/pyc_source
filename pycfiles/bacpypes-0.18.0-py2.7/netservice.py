# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/netservice.py
# Compiled at: 2020-01-29 15:49:52
"""
Network Service
"""
from copy import deepcopy as _deepcopy
from .settings import settings
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .errors import ConfigurationError
from .core import deferred
from .comm import Client, Server, bind, ServiceAccessPoint, ApplicationServiceElement
from .task import FunctionTask
from .pdu import Address, LocalBroadcast, LocalStation, PDU, RemoteStation, GlobalBroadcast
from .npdu import NPDU, npdu_types, IAmRouterToNetwork, WhoIsRouterToNetwork, WhatIsNetworkNumber, NetworkNumberIs
from .apdu import APDU as _APDU
_debug = 0
_log = ModuleLogger(globals())
ROUTER_AVAILABLE = 0
ROUTER_BUSY = 1
ROUTER_DISCONNECTED = 2
ROUTER_UNREACHABLE = 3

class RouterInfo(DebugContents):
    """These objects are routing information records that map router
    addresses with destination networks."""
    _debug_contents = ('snet', 'address', 'dnets')

    def __init__(self, snet, address):
        self.snet = snet
        self.address = address
        self.dnets = {}

    def set_status(self, dnets, status):
        """Change the status of each of the DNETS."""
        for dnet in dnets:
            self.dnets[dnet] = status


@bacpypes_debugging
class RouterInfoCache():

    def __init__(self):
        if _debug:
            RouterInfoCache._debug('__init__')
        self.routers = {}
        self.path_info = {}

    def get_router_info(self, snet, dnet):
        if _debug:
            RouterInfoCache._debug('get_router_info %r %r', snet, dnet)
        router_info = self.path_info.get((snet, dnet), None)
        if _debug:
            RouterInfoCache._debug('   - router_info: %r', router_info)
        return router_info

    def update_router_info(self, snet, address, dnets, status=ROUTER_AVAILABLE):
        if _debug:
            RouterInfoCache._debug('update_router_info %r %r %r', snet, address, dnets)
        existing_router_info = self.routers.get(snet, {}).get(address, None)
        other_routers = set()
        for dnet in dnets:
            other_router = self.path_info.get((snet, dnet), None)
            if other_router and other_router is not existing_router_info:
                other_routers.add(other_router)

        if other_routers:
            for router_info in other_routers:
                for dnet in dnets:
                    if dnet in router_info.dnets:
                        del router_info.dnets[dnet]
                        del self.path_info[(snet, dnet)]
                        if _debug:
                            RouterInfoCache._debug('    - del path: %r -> %r via %r', snet, dnet, router_info.address)

                if not router_info.dnets:
                    del self.routers[snet][router_info.address]
                    if _debug:
                        RouterInfoCache._debug('    - no dnets: %r via %r', snet, router_info.address)

        if not existing_router_info:
            router_info = RouterInfo(snet, address)
            if snet not in self.routers:
                self.routers[snet] = {address: router_info}
            else:
                self.routers[snet][address] = router_info
            for dnet in dnets:
                self.path_info[(snet, dnet)] = router_info
                if _debug:
                    RouterInfoCache._debug('    - add path: %r -> %r via %r', snet, dnet, router_info.address)
                router_info.dnets[dnet] = status

        else:
            for dnet in dnets:
                if dnet not in existing_router_info.dnets:
                    self.path_info[(snet, dnet)] = existing_router_info
                    if _debug:
                        RouterInfoCache._debug('    - add path: %r -> %r via %r', snet, dnet, router_info.address)
                existing_router_info.dnets[dnet] = status

        return

    def update_router_status(self, snet, address, status):
        if _debug:
            RouterInfoCache._debug('update_router_status %r %r %r', snet, address, status)
        existing_router_info = self.routers.get(snet, {}).get(address, None)
        if not existing_router_info:
            if _debug:
                RouterInfoCache._debug('    - not a router we know about')
            return
        existing_router_info.status = status
        if _debug:
            RouterInfoCache._debug('    - status updated')
        return

    def delete_router_info(self, snet, address=None, dnets=None):
        if _debug:
            RouterInfoCache._debug('delete_router_info %r %r %r', dnets)
        if address is None and dnets is None:
            raise RuntimeError('inconsistent parameters')
        if address is not None:
            router_info = self.routers.get(snet, {}).get(address, None)
            if not router_info:
                if _debug:
                    RouterInfoCache._debug('    - no route info')
            else:
                for dnet in dnets or router_info.dnets:
                    del self.path_info[(snet, dnet)]
                    if _debug:
                        RouterInfoCache._debug('    - del path: %r -> %r via %r', snet, dnet, router_info.address)

                del self.routers[snet][address]
            return
        other_routers = set()
        for dnet in dnets:
            other_router = self.path_info.get((snet, dnet), None)
            if other_router and other_router is not existing_router_info:
                other_routers.add(other_router)

        for router_info in other_routers:
            for dnet in dnets:
                if dnet in router_info.dnets:
                    del router_info.dnets[dnet]
                    del self.path_info[(snet, dnet)]
                    if _debug:
                        RouterInfoCache._debug('    - del path: %r -> %r via %r', snet, dnet, router_info.address)

            if not router_info.dnets:
                del self.routers[snet][router_info.address]
                if _debug:
                    RouterInfoCache._debug('    - no dnets: %r via %r', snet, router_info.address)

        return

    def update_source_network(self, old_snet, new_snet):
        if _debug:
            RouterInfoCache._debug('update_source_network %r %r', old_snet, new_snet)
        if old_snet not in self.routers:
            if _debug:
                RouterInfoCache._debug('    - no router references: %r', list(self.routers.keys()))
            return
        snet_routers = self.routers[new_snet] = self.routers.pop(old_snet)
        for address, router_info in snet_routers.items():
            for dnet in router_info.dnets:
                self.path_info[(new_snet, dnet)] = self.path_info.pop((old_snet, dnet))


@bacpypes_debugging
class NetworkAdapter(Client, DebugContents):
    _debug_contents = ('adapterSAP-', 'adapterNet', 'adapterAddr', 'adapterNetConfigured')

    def __init__(self, sap, net, addr, cid=None):
        if _debug:
            NetworkAdapter._debug('__init__ %s %r %r cid=%r', sap, net, addr, cid)
        Client.__init__(self, cid)
        self.adapterSAP = sap
        self.adapterNet = net
        self.adapterAddr = addr
        if net is None:
            self.adapterNetConfigured = None
        else:
            self.adapterNetConfigured = 1
        return

    def confirmation(self, pdu):
        """Decode upstream PDUs and pass them up to the service access point."""
        if _debug:
            NetworkAdapter._debug('confirmation %r (net=%r)', pdu, self.adapterNet)
        npdu = NPDU(user_data=pdu.pduUserData)
        npdu.decode(pdu)
        self.adapterSAP.process_npdu(self, npdu)

    def process_npdu(self, npdu):
        """Encode NPDUs from the service access point and send them downstream."""
        if _debug:
            NetworkAdapter._debug('process_npdu %r (net=%r)', npdu, self.adapterNet)
        pdu = PDU(user_data=npdu.pduUserData)
        npdu.encode(pdu)
        self.request(pdu)

    def EstablishConnectionToNetwork(self, net):
        pass

    def DisconnectConnectionToNetwork(self, net):
        pass


@bacpypes_debugging
class NetworkServiceAccessPoint(ServiceAccessPoint, Server, DebugContents):
    _debug_contents = ('adapters++', 'pending_nets', 'local_adapter-')

    def __init__(self, router_info_cache=None, sap=None, sid=None):
        if _debug:
            NetworkServiceAccessPoint._debug('__init__ sap=%r sid=%r', sap, sid)
        ServiceAccessPoint.__init__(self, sap)
        Server.__init__(self, sid)
        self.adapters = {}
        self.router_info_cache = router_info_cache or RouterInfoCache()
        self.pending_nets = {}
        self.local_adapter = None
        return

    def bind(self, server, net=None, address=None):
        """Create a network adapter object and bind.

        bind(s, None, None)
            Called for simple applications, local network unknown, no specific
            address, APDUs sent upstream

        bind(s, net, None)
            Called for routers, bind to the network, (optionally?) drop APDUs

        bind(s, None, address)
            Called for applications or routers, bind to the network (to be
            discovered), send up APDUs with a metching address

        bind(s, net, address)
            Called for applications or routers, bind to the network, send up
            APDUs with a metching address.
        """
        if _debug:
            NetworkServiceAccessPoint._debug('bind %r net=%r address=%r', server, net, address)
        if net in self.adapters:
            raise RuntimeError('already bound: %r' % (net,))
        adapter = NetworkAdapter(self, net, address)
        self.adapters[net] = adapter
        if _debug:
            NetworkServiceAccessPoint._debug('    - adapter: %r, %r', net, adapter)
        if address:
            if _debug:
                NetworkServiceAccessPoint._debug('    - setting local adapter')
            self.local_adapter = adapter
        if not self.local_adapter:
            if _debug:
                NetworkServiceAccessPoint._debug('    - default local adapter')
            self.local_adapter = adapter
        if not self.local_adapter.adapterAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - no local address')
        bind(adapter, server)

    def update_router_references(self, snet, address, dnets):
        """Update references to routers."""
        if _debug:
            NetworkServiceAccessPoint._debug('update_router_references %r %r %r', snet, address, dnets)
        if snet not in self.adapters:
            raise RuntimeError('no adapter for network: %d' % (snet,))
        self.router_info_cache.update_router_info(snet, address, dnets)

    def delete_router_references(self, snet, address=None, dnets=None):
        """Delete references to routers/networks."""
        if _debug:
            NetworkServiceAccessPoint._debug('delete_router_references %r %r %r', snet, address, dnets)
        if snet not in self.adapters:
            raise RuntimeError('no adapter for network: %d' % (snet,))
        self.router_info_cache.delete_router_info(snet, address, dnets)

    def indication(self, pdu):
        if _debug:
            NetworkServiceAccessPoint._debug('indication %r', pdu)
        if not self.adapters:
            raise ConfigurationError('no adapters')
        local_adapter = self.local_adapter
        if _debug:
            NetworkServiceAccessPoint._debug('    - local_adapter: %r', local_adapter)
        apdu = _APDU(user_data=pdu.pduUserData)
        pdu.encode(apdu)
        if _debug:
            NetworkServiceAccessPoint._debug('    - apdu: %r', apdu)
        npdu = NPDU(user_data=pdu.pduUserData)
        apdu.encode(npdu)
        if _debug:
            NetworkServiceAccessPoint._debug('    - npdu: %r', npdu)
        npdu.npduHopCount = 255
        if settings.route_aware and npdu.pduDestination.addrRoute:
            assert npdu.pduDestination.addrRoute.addrType == Address.localStationAddr
            if _debug:
                NetworkServiceAccessPoint._debug('    - routed: %r', npdu.pduDestination.addrRoute)
            if npdu.pduDestination.addrType in (Address.remoteStationAddr, Address.remoteBroadcastAddr, Address.globalBroadcastAddr):
                if _debug:
                    NetworkServiceAccessPoint._debug('    - continue DADR: %r', apdu.pduDestination)
                npdu.npduDADR = apdu.pduDestination
            npdu.pduDestination = npdu.pduDestination.addrRoute
            local_adapter.process_npdu(npdu)
            return
        else:
            if npdu.pduDestination.addrType == Address.localStationAddr:
                local_adapter.process_npdu(npdu)
                return
            if npdu.pduDestination.addrType == Address.localBroadcastAddr:
                local_adapter.process_npdu(npdu)
                return
            if npdu.pduDestination.addrType == Address.globalBroadcastAddr:
                npdu.pduDestination = LocalBroadcast()
                npdu.npduDADR = apdu.pduDestination
                for xadapter in self.adapters.values():
                    xadapter.process_npdu(npdu)

                return
            if npdu.pduDestination.addrType != Address.remoteBroadcastAddr and npdu.pduDestination.addrType != Address.remoteStationAddr:
                raise RuntimeError('invalid destination address type: %s' % (npdu.pduDestination.addrType,))
            dnet = npdu.pduDestination.addrNet
            if _debug:
                NetworkServiceAccessPoint._debug('    - dnet: %r', dnet)
            if dnet == local_adapter.adapterNet:
                if npdu.pduDestination.addrType == Address.remoteStationAddr:
                    if _debug:
                        NetworkServiceAccessPoint._debug('    - mapping remote station to local station')
                    npdu.pduDestination = LocalStation(npdu.pduDestination.addrAddr)
                elif npdu.pduDestination.addrType == Address.remoteBroadcastAddr:
                    if _debug:
                        NetworkServiceAccessPoint._debug('    - mapping remote broadcast to local broadcast')
                    npdu.pduDestination = LocalBroadcast()
                else:
                    raise RuntimeError('addressing problem')
                local_adapter.process_npdu(npdu)
                return
            npdu.pduDestination = None
            npdu.npduDADR = apdu.pduDestination
            if dnet in self.pending_nets:
                if _debug:
                    NetworkServiceAccessPoint._debug('    - already waiting for path')
                self.pending_nets[dnet].append(npdu)
                return
            router_info = None
            for snet, snet_adapter in self.adapters.items():
                router_info = self.router_info_cache.get_router_info(snet, dnet)
                if router_info:
                    break

            if router_info:
                if _debug:
                    NetworkServiceAccessPoint._debug('    - router_info found: %r', router_info)
                dnet_status = router_info.dnets[dnet]
                if _debug:
                    NetworkServiceAccessPoint._debug('    - dnet_status: %r', dnet_status)
                npdu.pduDestination = router_info.address
                snet_adapter.process_npdu(npdu)
            else:
                if _debug:
                    NetworkServiceAccessPoint._debug('    - no known path to network')
                net_list = self.pending_nets.get(dnet, None)
                if net_list is None:
                    net_list = self.pending_nets[dnet] = []
                net_list.append(npdu)
                xnpdu = WhoIsRouterToNetwork(dnet)
                xnpdu.pduDestination = LocalBroadcast()
                for adapter in self.adapters.values():
                    self.sap_indication(adapter, xnpdu)

            return

    def process_npdu(self, adapter, npdu):
        if _debug:
            NetworkServiceAccessPoint._debug('process_npdu %r %r', adapter, npdu)
        if not self.adapters:
            raise ConfigurationError('no adapters')
        if npdu.npduSADR and npdu.npduSADR.addrType != Address.nullAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - check source path')
            snet = npdu.npduSADR.addrNet
            if snet in self.adapters:
                NetworkServiceAccessPoint._warning('    - path error (1)')
                return
            self.router_info_cache.update_router_info(adapter.adapterNet, npdu.pduSource, [snet])
        if not npdu.npduDADR or npdu.npduDADR.addrType == Address.nullAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - no DADR')
            processLocally = adapter is self.local_adapter or npdu.npduNetMessage is not None
            forwardMessage = False
        elif npdu.npduDADR.addrType == Address.remoteBroadcastAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - DADR is remote broadcast')
            if npdu.npduDADR.addrNet == adapter.adapterNet:
                NetworkServiceAccessPoint._warning('    - path error (2)')
                return
            processLocally = npdu.npduDADR.addrNet == self.local_adapter.adapterNet
            forwardMessage = True
        elif npdu.npduDADR.addrType == Address.remoteStationAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - DADR is remote station')
            if npdu.npduDADR.addrNet == adapter.adapterNet:
                NetworkServiceAccessPoint._warning('    - path error (3)')
                return
            processLocally = npdu.npduDADR.addrNet == self.local_adapter.adapterNet and npdu.npduDADR.addrAddr == self.local_adapter.adapterAddr.addrAddr
            forwardMessage = not processLocally
        elif npdu.npduDADR.addrType == Address.globalBroadcastAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - DADR is global broadcast')
            processLocally = True
            forwardMessage = True
        else:
            NetworkServiceAccessPoint._warning('invalid destination address type: %s', npdu.npduDADR.addrType)
            return
        if _debug:
            NetworkServiceAccessPoint._debug('    - processLocally: %r', processLocally)
            NetworkServiceAccessPoint._debug('    - forwardMessage: %r', forwardMessage)
        if npdu.npduNetMessage is None:
            if _debug:
                NetworkServiceAccessPoint._debug('    - application layer message')
            if processLocally and self.serverPeer:
                if _debug:
                    NetworkServiceAccessPoint._debug('    - processing APDU locally')
                apdu = _APDU(user_data=npdu.pduUserData)
                apdu.decode(_deepcopy(npdu))
                if _debug:
                    NetworkServiceAccessPoint._debug('    - apdu: %r', apdu)
                if len(self.adapters) > 1 and adapter != self.local_adapter:
                    if not npdu.npduSADR:
                        apdu.pduSource = RemoteStation(adapter.adapterNet, npdu.pduSource.addrAddr)
                    else:
                        apdu.pduSource = npdu.npduSADR
                    if settings.route_aware:
                        apdu.pduSource.addrRoute = npdu.pduSource
                    if not npdu.npduDADR:
                        apdu.pduDestination = self.local_adapter.adapterAddr
                    elif npdu.npduDADR.addrType == Address.globalBroadcastAddr:
                        apdu.pduDestination = GlobalBroadcast()
                    elif npdu.npduDADR.addrType == Address.remoteBroadcastAddr:
                        apdu.pduDestination = LocalBroadcast()
                    else:
                        apdu.pduDestination = self.local_adapter.adapterAddr
                else:
                    if npdu.npduSADR:
                        apdu.pduSource = npdu.npduSADR
                        if settings.route_aware:
                            if _debug:
                                NetworkServiceAccessPoint._debug('    - adding route')
                            apdu.pduSource.addrRoute = npdu.pduSource
                    else:
                        apdu.pduSource = npdu.pduSource
                    if npdu.npduDADR and npdu.npduDADR.addrType == Address.globalBroadcastAddr:
                        apdu.pduDestination = GlobalBroadcast()
                    else:
                        apdu.pduDestination = npdu.pduDestination
                if _debug:
                    NetworkServiceAccessPoint._debug('    - apdu.pduSource: %r', apdu.pduSource)
                    NetworkServiceAccessPoint._debug('    - apdu.pduDestination: %r', apdu.pduDestination)
                self.response(apdu)
        else:
            if _debug:
                NetworkServiceAccessPoint._debug('    - network layer message')
            if processLocally:
                if npdu.npduNetMessage not in npdu_types:
                    if _debug:
                        NetworkServiceAccessPoint._debug('    - unknown npdu type: %r', npdu.npduNetMessage)
                    return
                if _debug:
                    NetworkServiceAccessPoint._debug('    - processing NPDU locally')
                xpdu = npdu_types[npdu.npduNetMessage](user_data=npdu.pduUserData)
                xpdu.decode(_deepcopy(npdu))
                self.sap_request(adapter, xpdu)
            if forwardMessage or _debug:
                NetworkServiceAccessPoint._debug('    - no forwarding')
            return
        if len(self.adapters) == 1:
            if _debug:
                NetworkServiceAccessPoint._debug('    - not a router')
            return
        if npdu.npduHopCount == 0:
            if _debug:
                NetworkServiceAccessPoint._debug('    - no more hops')
            return
        newpdu = _deepcopy(npdu)
        newpdu.pduSource = None
        newpdu.pduDestination = None
        newpdu.npduHopCount -= 1
        if not npdu.npduSADR:
            newpdu.npduSADR = RemoteStation(adapter.adapterNet, npdu.pduSource.addrAddr)
        else:
            newpdu.npduSADR = npdu.npduSADR
        if npdu.npduDADR.addrType == Address.globalBroadcastAddr:
            if _debug:
                NetworkServiceAccessPoint._debug('    - global broadcasting')
            newpdu.pduDestination = LocalBroadcast()
            for xadapter in self.adapters.values():
                if xadapter is not adapter:
                    xadapter.process_npdu(_deepcopy(newpdu))

            return
        if npdu.npduDADR.addrType == Address.remoteBroadcastAddr or npdu.npduDADR.addrType == Address.remoteStationAddr:
            dnet = npdu.npduDADR.addrNet
            if _debug:
                NetworkServiceAccessPoint._debug('    - remote station/broadcast')
            if dnet in self.adapters:
                xadapter = self.adapters[dnet]
                if xadapter is adapter:
                    if _debug:
                        NetworkServiceAccessPoint._debug('    - path error (4)')
                    return
                if _debug:
                    NetworkServiceAccessPoint._debug('    - found path via %r', xadapter)
                if npdu.npduDADR.addrType == Address.remoteBroadcastAddr:
                    newpdu.pduDestination = LocalBroadcast()
                else:
                    newpdu.pduDestination = LocalStation(npdu.npduDADR.addrAddr)
                newpdu.npduDADR = None
                xadapter.process_npdu(_deepcopy(newpdu))
                return
            router_info = None
            for snet, snet_adapter in self.adapters.items():
                router_info = self.router_info_cache.get_router_info(snet, dnet)
                if router_info:
                    break

            if router_info:
                if _debug:
                    NetworkServiceAccessPoint._debug('    - found path via %r', router_info)
                newpdu.pduDestination = router_info.address
                snet_adapter.process_npdu(_deepcopy(newpdu))
                return
            if _debug:
                NetworkServiceAccessPoint._debug('    - no router info found')
            xnpdu = WhoIsRouterToNetwork(dnet)
            xnpdu.pduDestination = LocalBroadcast()
            for xadapter in self.adapters.values():
                if xadapter is adapter:
                    continue
                self.sap_indication(xadapter, xnpdu)

            return
        if _debug:
            NetworkServiceAccessPoint._debug('    - bad DADR: %r', npdu.npduDADR)
        return

    def sap_indication(self, adapter, npdu):
        if _debug:
            NetworkServiceAccessPoint._debug('sap_indication %r %r', adapter, npdu)
        xpdu = NPDU(user_data=npdu.pduUserData)
        npdu.encode(xpdu)
        npdu._xpdu = xpdu
        adapter.process_npdu(xpdu)

    def sap_confirmation(self, adapter, npdu):
        if _debug:
            NetworkServiceAccessPoint._debug('sap_confirmation %r %r', adapter, npdu)
        xpdu = NPDU(user_data=npdu.pduUserData)
        npdu.encode(xpdu)
        npdu._xpdu = xpdu
        adapter.process_npdu(xpdu)


@bacpypes_debugging
class NetworkServiceElement(ApplicationServiceElement):
    _startup_disabled = False

    def __init__(self, eid=None):
        if _debug:
            NetworkServiceElement._debug('__init__ eid=%r', eid)
        ApplicationServiceElement.__init__(self, eid)
        self.network_number_is_task = None
        if not self._startup_disabled:
            deferred(self.startup)
        return

    def startup(self):
        if _debug:
            NetworkServiceElement._debug('startup')
        sap = self.elementService
        if _debug:
            NetworkServiceElement._debug('    - sap: %r', sap)
        for adapter in sap.adapters.values():
            if _debug:
                NetworkServiceElement._debug('    - adapter: %r', adapter)
            if adapter.adapterNet is None:
                if _debug:
                    NetworkServiceElement._debug('    - skipping, unknown net')
                continue
            else:
                if adapter.adapterAddr is None:
                    if _debug:
                        NetworkServiceElement._debug('    - skipping, unknown addr')
                    continue
                netlist = []
                for xadapter in sap.adapters.values():
                    if xadapter is not adapter:
                        if xadapter.adapterNet is None or xadapter.adapterAddr is None:
                            continue
                        netlist.append(xadapter.adapterNet)

            if not netlist:
                if _debug:
                    NetworkServiceElement._debug('    - skipping, no netlist')
                continue
            self.i_am_router_to_network(adapter=adapter, network=netlist)

        return

    def indication(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('indication %r %r', adapter, npdu)
        fn = npdu.__class__.__name__
        if hasattr(self, fn):
            getattr(self, fn)(adapter, npdu)

    def confirmation(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('confirmation %r %r', adapter, npdu)
        fn = npdu.__class__.__name__
        if hasattr(self, fn):
            getattr(self, fn)(adapter, npdu)

    def i_am_router_to_network(self, adapter=None, destination=None, network=None):
        if _debug:
            NetworkServiceElement._debug('i_am_router_to_network %r %r %r', adapter, destination, network)
        sap = self.elementService
        if _debug:
            NetworkServiceElement._debug('    - sap: %r', sap)
        if len(sap.adapters) == 1:
            raise RuntimeError('not a router')
        if adapter is not None:
            if destination is None:
                destination = LocalBroadcast()
            elif destination.addrType in (Address.localStationAddr, Address.localBroadcastAddr):
                pass
            elif destination.addrType == Address.remoteStationAddr:
                if destination.addrNet != adapter.adapterNet:
                    raise ValueError('invalid address, remote station for a different adapter')
                destination = LocalStation(destination.addrAddr)
            elif destination.addrType == Address.remoteBroadcastAddr:
                if destination.addrNet != adapter.adapterNet:
                    raise ValueError('invalid address, remote broadcast for a different adapter')
                destination = LocalBroadcast()
            else:
                raise TypeError('invalid destination address')
        else:
            if destination is None:
                destination = LocalBroadcast()
            elif destination.addrType == Address.localStationAddr:
                raise ValueError('ambiguous destination')
            elif destination.addrType == Address.localBroadcastAddr:
                pass
            elif destination.addrType == Address.remoteStationAddr:
                if destination.addrNet not in sap.adapters:
                    raise ValueError('invalid address, no network for remote station')
                adapter = sap.adapters[destination.addrNet]
                destination = LocalStation(destination.addrAddr)
            elif destination.addrType == Address.remoteBroadcastAddr:
                if destination.addrNet not in sap.adapters:
                    raise ValueError('invalid address, no network for remote broadcast')
                adapter = sap.adapters[destination.addrNet]
                destination = LocalBroadcast()
            else:
                raise TypeError('invalid destination address')
            if _debug:
                NetworkServiceElement._debug('    - adapter, destination, network: %r, %r, %r', adapter, destination, network)
            if adapter is not None:
                adapter_list = [
                 adapter]
            else:
                adapter_list = list(sap.adapters.values())
            for adapter in adapter_list:
                netlist = []
                for xadapter in sap.adapters.values():
                    if xadapter is not adapter:
                        netlist.append(xadapter.adapterNet)

                if network is None:
                    pass
                elif isinstance(network, int):
                    if network not in netlist:
                        continue
                    netlist = [
                     network]
                elif isinstance(network, list):
                    netlist = [ net for net in netlist if net in network ]
                iamrtn = IAmRouterToNetwork(netlist)
                iamrtn.pduDestination = destination
                if _debug:
                    NetworkServiceElement._debug('    - adapter, iamrtn: %r, %r', adapter, iamrtn)
                self.request(adapter, iamrtn)

        return

    def WhoIsRouterToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('WhoIsRouterToNetwork %r %r', adapter, npdu)
        sap = self.elementService
        if _debug:
            NetworkServiceElement._debug('    - sap: %r', sap)
        if len(sap.adapters) == 1:
            if _debug:
                NetworkServiceElement._debug('    - not a router')
            return
        if npdu.wirtnNetwork is None:
            if _debug:
                NetworkServiceElement._debug('    - requesting all networks')
            netlist = []
            for xadapter in sap.adapters.values():
                if xadapter is adapter:
                    continue
                netlist.append(xadapter.adapterNet)

            if netlist:
                if _debug:
                    NetworkServiceElement._debug('    - found these: %r', netlist)
                iamrtn = IAmRouterToNetwork(netlist, user_data=npdu.pduUserData)
                iamrtn.pduDestination = npdu.pduSource
                self.response(adapter, iamrtn)
        else:
            if _debug:
                NetworkServiceElement._debug('    - requesting specific network: %r', npdu.wirtnNetwork)
            dnet = npdu.wirtnNetwork
            if dnet in sap.adapters:
                if _debug:
                    NetworkServiceElement._debug('    - directly connected')
                if sap.adapters[dnet] is adapter:
                    if _debug:
                        NetworkServiceElement._debug('    - same network')
                    return
                iamrtn = IAmRouterToNetwork([dnet], user_data=npdu.pduUserData)
                iamrtn.pduDestination = npdu.pduSource
                self.response(adapter, iamrtn)
                return
            router_info = None
            for snet, snet_adapter in sap.adapters.items():
                router_info = sap.router_info_cache.get_router_info(snet, dnet)
                if router_info:
                    break

            if router_info:
                if _debug:
                    NetworkServiceElement._debug('    - router found: %r', router_info)
                if snet_adapter is adapter:
                    if _debug:
                        NetworkServiceElement._debug('    - same network')
                    return
                iamrtn = IAmRouterToNetwork([dnet], user_data=npdu.pduUserData)
                iamrtn.pduDestination = npdu.pduSource
                self.response(adapter, iamrtn)
            else:
                if _debug:
                    NetworkServiceElement._debug('    - forwarding to other adapters')
                whoisrtn = WhoIsRouterToNetwork(dnet, user_data=npdu.pduUserData)
                whoisrtn.pduDestination = LocalBroadcast()
                if npdu.npduSADR:
                    whoisrtn.npduSADR = npdu.npduSADR
                else:
                    whoisrtn.npduSADR = RemoteStation(adapter.adapterNet, npdu.pduSource.addrAddr)
                if _debug:
                    NetworkServiceElement._debug('    - whoisrtn: %r', whoisrtn)
                for xadapter in sap.adapters.values():
                    if xadapter is not adapter:
                        if _debug:
                            NetworkServiceElement._debug('    - sending on adapter: %r', xadapter)
                        self.request(xadapter, whoisrtn)

        return

    def IAmRouterToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('IAmRouterToNetwork %r %r', adapter, npdu)
        sap = self.elementService
        if _debug:
            NetworkServiceElement._debug('    - sap: %r', sap)
        sap.update_router_references(adapter.adapterNet, npdu.pduSource, npdu.iartnNetworkList)
        if len(sap.adapters) == 1:
            if _debug:
                NetworkServiceElement._debug('    - not a router')
        else:
            if _debug:
                NetworkServiceElement._debug('    - forwarding to other adapters')
            iamrtn = IAmRouterToNetwork(npdu.iartnNetworkList, user_data=npdu.pduUserData)
            iamrtn.pduDestination = LocalBroadcast()
            for xadapter in sap.adapters.values():
                if xadapter is not adapter:
                    if _debug:
                        NetworkServiceElement._debug('    - sending on adapter: %r', xadapter)
                    self.request(xadapter, iamrtn)

            for dnet in npdu.iartnNetworkList:
                pending_npdus = sap.pending_nets.get(dnet, None)
                if pending_npdus is not None:
                    if _debug:
                        NetworkServiceElement._debug('    - %d pending to %r', len(pending_npdus), dnet)
                    del sap.pending_nets[dnet]
                    for pending_npdu in pending_npdus:
                        if _debug:
                            NetworkServiceElement._debug('    - sending %s', repr(pending_npdu))
                        pending_npdu.pduDestination = npdu.pduSource
                        adapter.process_npdu(pending_npdu)

        return

    def ICouldBeRouterToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('ICouldBeRouterToNetwork %r %r', adapter, npdu)

    def RejectMessageToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('RejectMessageToNetwork %r %r', adapter, npdu)

    def RouterBusyToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('RouterBusyToNetwork %r %r', adapter, npdu)

    def RouterAvailableToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('RouterAvailableToNetwork %r %r', adapter, npdu)

    def InitializeRoutingTable(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('InitializeRoutingTable %r %r', adapter, npdu)

    def InitializeRoutingTableAck(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('InitializeRoutingTableAck %r %r', adapter, npdu)

    def EstablishConnectionToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('EstablishConnectionToNetwork %r %r', adapter, npdu)

    def DisconnectConnectionToNetwork(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('DisconnectConnectionToNetwork %r %r', adapter, npdu)

    def what_is_network_number(self, adapter=None, address=None):
        if _debug:
            NetworkServiceElement._debug('what_is_network_number %r', adapter, address)
        sap = self.elementService
        if adapter is None and address is not None:
            raise RuntimeError('inconsistent parameters')
        winn = WhatIsNetworkNumber()
        winn.pduDestination = LocalBroadcast()
        if adapter:
            if address is not None:
                winn.pduDestination = address
            adapter_list = [
             adapter]
        else:
            adapter_list = []
            for xadapter in sap.adapters.values():
                if xadapter.adapterNet is None:
                    adapter_list.append(xadapter)

            if _debug:
                NetworkServiceElement._debug('    - adapter_list: %r', adapter_list)
            for xadapter in adapter_list:
                self.request(xadapter, winn)

        return

    def WhatIsNetworkNumber(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('WhatIsNetworkNumber %r %r', adapter, npdu)
        sap = self.elementService
        if adapter.adapterNet is None:
            if _debug:
                NetworkServiceElement._debug('   - local network not known')
            return
        if npdu.pduDestination.addrType == Address.localBroadcastAddr:
            if _debug:
                NetworkServiceElement._debug('    - local broadcast request')
            if len(sap.adapters) == 1:
                if _debug:
                    NetworkServiceElement._debug('    - not a router')
                if self.network_number_is_task:
                    if _debug:
                        NetworkServiceElement._debug('    - already waiting')
                else:
                    self.network_number_is_task = FunctionTask(self.network_number_is, adapter)
                    self.network_number_is_task.install_task(delta=10000)
                    return
        self.network_number_is(adapter)
        return

    def network_number_is(self, adapter=None):
        if _debug:
            NetworkServiceElement._debug('network_number_is %r', adapter)
        sap = self.elementService
        if adapter is not None:
            adapter_list = [
             adapter]
        else:
            adapter_list = []
            for xadapter in sap.adapters.values():
                if xadapter.adapterNet is not None and xadapter.adapterNetConfigured == 1:
                    adapter_list.append(xadapter)

            if _debug:
                NetworkServiceElement._debug('    - adapter_list: %r', adapter_list)
            for xadapter in adapter_list:
                if xadapter.adapterNet is None:
                    if _debug:
                        NetworkServiceElement._debug('    - unknown network: %r', xadapter)
                    continue
                nni = NetworkNumberIs(net=xadapter.adapterNet, flag=xadapter.adapterNetConfigured)
                nni.pduDestination = LocalBroadcast()
                if _debug:
                    NetworkServiceElement._debug('    - nni: %r', nni)
                self.request(xadapter, nni)

        return

    def NetworkNumberIs(self, adapter, npdu):
        if _debug:
            NetworkServiceElement._debug('NetworkNumberIs %r %r', adapter, npdu)
        sap = self.elementService
        if npdu.pduDestination.addrType != Address.localBroadcastAddr:
            if _debug:
                NetworkServiceElement._debug('    - not broadcast')
            return
        if self.network_number_is_task:
            if _debug:
                NetworkServiceElement._debug('    - cancel waiting task')
            self.network_number_is_task.suspend_task()
            self.network_number_is_task = None
        if adapter.adapterNet is None:
            if _debug:
                NetworkServiceElement._debug('   - local network not known: %r', list(sap.adapters.keys()))
            sap.router_info_cache.update_source_network(None, npdu.nniNet)
            del sap.adapters[None]
            adapter.adapterNet = npdu.nniNet
            adapter.adapterNetConfigured = 0
            sap.adapters[adapter.adapterNet] = adapter
            if _debug:
                NetworkServiceElement._debug('   - local network learned')
            return
        if adapter.adapterNet == npdu.nniNet:
            if _debug:
                NetworkServiceElement._debug('   - matches what we have')
            return
        if adapter.adapterNetConfigured == 1:
            if _debug:
                NetworkServiceElement._debug("   - doesn't match what we know")
            return
        if _debug:
            NetworkServiceElement._debug('   - learning something new')
        sap.router_info_cache.update_source_network(adapter.adapterNet, npdu.nniNet)
        del sap.adapters[adapter.adapterNet]
        adapter.adapterNet = npdu.nniNet
        adapter.adapterNetConfigured = npdu.nniFlag
        sap.adapters[adapter.adapterNet] = adapter
        return