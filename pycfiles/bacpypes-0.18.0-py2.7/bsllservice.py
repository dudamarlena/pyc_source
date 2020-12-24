# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/bsllservice.py
# Compiled at: 2020-01-29 15:49:50
"""
BACnet Streaming Link Layer Service
"""
import random
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .comm import Client, bind, ApplicationServiceElement
from .tcp import TCPClientDirector, TCPServerDirector, StreamToPacket
from .pdu import Address, LocalBroadcast, PDU, unpack_ip_addr
from .npdu import NPDU
from .netservice import NetworkAdapter
from .bsll import AUTHENTICATION_FAILURE, AUTHENTICATION_HASH, AUTHENTICATION_NO_SERVICE, AUTHENTICATION_REQUIRED, AccessChallenge, AccessRequest, AccessResponse, BSLCI, BSLPDU, CLIENT_SERVER_SERVICE_ID, DEVICE_TO_DEVICE_SERVICE_ID, DeviceToDeviceAPDU, LANE_SERVICE_ID, NO_DEVICE_TO_DEVICE_SERVICE, NO_LANE_SERVICE, NO_PROXY_SERVICE, NO_ROUTER_TO_ROUTER_SERVICE, PROXY_SERVICE_ID, ProxyToServerBroadcastNPDU, ProxyToServerUnicastNPDU, ROUTER_TO_ROUTER_SERVICE_ID, Result, RouterToRouterNPDU, SUCCESS, ServerToProxyBroadcastNPDU, ServerToProxyUnicastNPDU, ServiceRequest, UNRECOGNIZED_SERVICE, bsl_pdu_types, hash_functions
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
def _Packetize(data):
    if _debug:
        _Packetize._debug('_Packetize %r', data)
    start_ind = data.find(b'\x83')
    if start_ind == -1:
        return None
    else:
        if start_ind > 0:
            if _debug:
                _Packetize._debug('    - garbage: %r', data[:start_ind])
            data = data[start_ind:]
        if len(data) < 4:
            return None
        total_len = (ord(data[2]) << 8) + ord(data[3])
        if len(data) < total_len:
            return None
        packet_slice = (data[:total_len], data[total_len:])
        if _debug:
            _Packetize._debug('    - packet_slice: %r', packet_slice)
        return packet_slice


@bacpypes_debugging
class _StreamToPacket(StreamToPacket):

    def __init__(self):
        if _debug:
            _StreamToPacket._debug('__init__')
        StreamToPacket.__init__(self, _Packetize)

    def indication(self, pdu):
        if _debug:
            _StreamToPacket._debug('indication %r', pdu)
        self.request(pdu)


@bacpypes_debugging
class UserInformation(DebugContents):
    _debug_contents = ('username', 'password*', 'service', 'proxyNetwork')

    def __init__(self, **kwargs):
        if _debug:
            UserInformation._debug('__init__ %r', kwargs)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.service = {}
        allServices = kwargs.get('allServices', False)
        self.service[DEVICE_TO_DEVICE_SERVICE_ID] = kwargs.get('deviceToDeviceService', allServices)
        self.service[ROUTER_TO_ROUTER_SERVICE_ID] = kwargs.get('routerToRouterService', allServices)
        self.service[PROXY_SERVICE_ID] = kwargs.get('proxyService', allServices)
        self.service[LANE_SERVICE_ID] = kwargs.get('laneService', allServices)
        self.service[CLIENT_SERVER_SERVICE_ID] = kwargs.get('clientServerService', allServices)
        self.proxyNetwork = kwargs.get('proxyNetwork', None)
        return


@bacpypes_debugging
class ConnectionState(DebugContents):
    NOT_AUTHENTICATED = 0
    REQUESTED = 1
    CHALLENGED = 2
    AUTHENTICATED = 3
    _debug_contents = ('address', 'service', 'connected', 'accessState', 'challenge',
                       'userinfo', 'proxyAdapter')

    def __init__(self, addr):
        if _debug:
            ConnectionState._debug('__init__ %r', addr)
        self.address = addr
        self.service = None
        self.connected = False
        self.accessState = ConnectionState.NOT_AUTHENTICATED
        self.challenge = None
        self.userinfo = None
        self.proxyAdapter = None
        return


@bacpypes_debugging
class ServiceAdapter():
    _authentication_required = False

    def __init__(self, mux):
        if _debug:
            ServiceAdapter._debug('__init__ %r', mux)
        self.multiplexer = mux
        self.connections = {}
        if self.serviceID == DEVICE_TO_DEVICE_SERVICE_ID:
            mux.deviceToDeviceService = self
        elif self.serviceID == ROUTER_TO_ROUTER_SERVICE_ID:
            mux.routerToRouterService = self
        elif self.serviceID == PROXY_SERVICE_ID:
            mux.proxyService = self
        elif self.serviceID == LANE_SERVICE_ID:
            mux.laneService = self
        else:
            raise RuntimeError(('invalid service ID: {0}').format(self.serviceID))

    def authentication_required(self, addr):
        """Return True iff authentication is required for connection requests from the address."""
        if _debug:
            ServiceAdapter._debug('authentication_required %r', addr)
        return self._authentication_required

    def get_default_user_info(self, addr):
        """Return a UserInformation object for trusted address->user authentication."""
        if _debug:
            ServiceAdapter._debug('get_default_user_info %r', addr)
        return

    def get_user_info(self, username):
        """Return a UserInformation object or None."""
        if _debug:
            ServiceAdapter._debug('get_user_info %r', username)
        return

    def add_connection(self, conn):
        if _debug:
            ServiceAdapter._debug('add_connection %r', conn)
        self.connections[conn.address] = conn
        conn.service = self
        conn.connected = True

    def remove_connection(self, conn):
        if _debug:
            ServiceAdapter._debug('remove_connection %r', conn)
        try:
            del self.connections[conn.address]
        except KeyError:
            ServiceAdapter._warning('remove_connection: %r not a connection', conn)

        conn.service = None
        conn.connected = False
        return

    def service_request(self, pdu):
        if _debug:
            ServiceAdapter._debug('service_request %r', pdu)
        self.multiplexer.indication(self, pdu)

    def service_confirmation(self, conn, pdu):
        raise NotImplementedError('service_confirmation must be overridden')


@bacpypes_debugging
class NetworkServiceAdapter(ServiceAdapter, NetworkAdapter):

    def __init__(self, mux, sap, net, cid=None):
        if _debug:
            NetworkServiceAdapter._debug('__init__ %r %r %r status=%r cid=%r', mux, sap, net, cid)
        ServiceAdapter.__init__(self, mux)
        NetworkAdapter.__init__(self, sap, net, cid)


@bacpypes_debugging
class TCPServerMultiplexer(Client):

    def __init__(self, addr=None):
        if _debug:
            TCPServerMultiplexer._debug('__init__ %r', addr)
        Client.__init__(self)
        if addr is None:
            self.address = Address()
            self.addrTuple = ('', 47808)
        else:
            if isinstance(addr, Address):
                self.address = addr
            else:
                self.address = Address(addr)
            self.addrTuple = self.address.addrTuple
        if _debug:
            TCPServerMultiplexer._debug('    - address: %r', self.address)
            TCPServerMultiplexer._debug('    - addrTuple: %r', self.addrTuple)
        self.director = TCPServerDirector(self.addrTuple)
        bind(self, _StreamToPacket(), self.director)
        self.ase = TCPMultiplexerASE(self)
        bind(self.ase, self.director)
        self.connections = {}
        self.deviceToDeviceService = None
        self.routerToRouterService = None
        self.proxyService = None
        self.laneService = None
        return

    def request(self, pdu):
        if _debug:
            TCPServerMultiplexer._debug('request %r', pdu)
        xpdu = BSLPDU()
        pdu.encode(xpdu)
        if _debug:
            TCPServerMultiplexer._debug('    - xpdu: %r', xpdu)
        ypdu = PDU()
        xpdu.encode(ypdu)
        ypdu.pduDestination = unpack_ip_addr(pdu.pduDestination.addrAddr)
        if _debug:
            TCPServerMultiplexer._debug('    - ypdu: %r', ypdu)
        Client.request(self, ypdu)

    def indication(self, server, pdu):
        if _debug:
            TCPServerMultiplexer._debug('indication %r %r', server, pdu)
        self.request(pdu)

    def confirmation(self, pdu):
        if _debug:
            TCPServerMultiplexer._debug('confirmation %r', pdu)
        pdu = PDU(pdu, source=Address(pdu.pduSource))
        if _debug:
            TCPServerMultiplexer._debug('    - pdu: %r', pdu)
        bslpdu = BSLPDU()
        bslpdu.decode(pdu)
        if _debug:
            TCPServerMultiplexer._debug('    - bslpdu: %r', bslpdu)
        conn = self.connections.get(pdu.pduSource, None)
        if not conn:
            TCPServerMultiplexer._warning('no connection: %r', pdu.pduSource)
            return
        else:
            fn = bslpdu.bslciFunction
            rpdu = bsl_pdu_types[fn]()
            rpdu.decode(bslpdu)
            if _debug:
                TCPServerMultiplexer._debug('    - rpdu: %r', rpdu)
            if fn == BSLCI.result:
                TCPServerMultiplexer._warning('unexpected Result')
            elif fn == BSLCI.serviceRequest:
                if conn.service and conn.connected:
                    conn.service.remove_connection(conn)
                newSAP = None
                resultCode = SUCCESS
                if rpdu.bslciServiceID == DEVICE_TO_DEVICE_SERVICE_ID:
                    if self.deviceToDeviceService:
                        newSAP = self.deviceToDeviceService
                    else:
                        resultCode = NO_DEVICE_TO_DEVICE_SERVICE
                else:
                    if rpdu.bslciServiceID == ROUTER_TO_ROUTER_SERVICE_ID:
                        if self.routerToRouterService:
                            newSAP = self.routerToRouterService
                        else:
                            resultCode = NO_ROUTER_TO_ROUTER_SERVICE
                    elif rpdu.bslciServiceID == PROXY_SERVICE_ID:
                        if self.proxyService:
                            newSAP = self.proxyService
                        else:
                            resultCode = NO_PROXY_SERVICE
                    elif rpdu.bslciServiceID == LANE_SERVICE_ID:
                        if self.laneService:
                            newSAP = self.laneService
                        else:
                            resultCode = NO_LANE_SERVICE
                    else:
                        resultCode = UNRECOGNIZED_SERVICE
                    if resultCode:
                        response = Result(resultCode)
                        response.pduDestination = rpdu.pduSource
                        self.request(response)
                        return
                if not newSAP.authentication_required(conn.address):
                    newSAP.add_connection(conn)
                else:
                    if not conn.userinfo:
                        conn.userinfo = newSAP.get_default_user_info(conn.address)
                        if conn.userinfo:
                            conn.accessState = ConnectionState.AUTHENTICATED
                            if _debug:
                                TCPServerMultiplexer._debug('    - authenticated to default user info: %r', conn.userinfo)
                        elif _debug:
                            TCPServerMultiplexer._debug('    - no default user info')
                    if not conn.accessState == ConnectionState.AUTHENTICATED:
                        resultCode = AUTHENTICATION_REQUIRED
                        conn.service = newSAP
                    elif not conn.userinfo.service[newSAP.serviceID]:
                        resultCode = AUTHENTICATION_NO_SERVICE
                    else:
                        newSAP.add_connection(conn)
                response = Result(resultCode)
                response.pduDestination = rpdu.pduSource
                self.request(response)
            elif fn == BSLCI.deviceToDeviceAPDU and self.deviceToDeviceService:
                if conn.service is not self.deviceToDeviceService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.deviceToDeviceService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.routerToRouterNPDU and self.routerToRouterService:
                if conn.service is not self.routerToRouterService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.routerToRouterService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.proxyToServerUnicastNPDU and self.proxyService:
                if conn.service is not self.proxyService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.proxyService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.proxyToServerBroadcastNPDU and self.proxyService:
                if conn.service is not self.proxyService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.proxyService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.serverToProxyUnicastNPDU and self.proxyService:
                TCPServerMultiplexer._warning('unexpected Server-To-Proxy-Unicast-NPDU')
            elif fn == BSLCI.serverToProxyBroadcastNPDU and self.proxyService:
                TCPServerMultiplexer._warning('unexpected Server-To-Proxy-Broadcast-NPDU')
            elif fn == BSLCI.clientToLESUnicastNPDU and self.laneService:
                if conn.service is not self.laneService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.laneService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.clientToLESBroadcastNPDU and self.laneService:
                if conn.service is not self.laneService:
                    TCPServerMultiplexer._warning('not connected to appropriate service')
                    return
                self.laneService.service_confirmation(conn, rpdu)
            elif fn == BSLCI.lesToClientUnicastNPDU and self.laneService:
                TCPServerMultiplexer._warning('unexpected LES-to-Client-Unicast-NPDU')
            elif fn == BSLCI.lesToClientBroadcastNPDU and self.laneService:
                TCPServerMultiplexer._warning('unexpected LES-to-Client-Broadcast-NPDU')
            elif fn == BSLCI.accessRequest:
                self.do_AccessRequest(conn, rpdu)
            elif fn == BSLCI.accessChallenge:
                TCPServerMultiplexer._warning('unexpected Access-Challenge')
            elif fn == BSLCI.accessResponse:
                self.do_AccessResponse(conn, rpdu)
            else:
                TCPServerMultiplexer._warning('unsupported message')
            return

    def do_AccessRequest(self, conn, bslpdu):
        if _debug:
            TCPServerMultiplexer._debug('do_AccessRequest %r %r', conn, bslpdu)
        if not conn.service:
            if _debug:
                TCPServerMultiplexer._debug('    - request a service first')
            response = Result(AUTHENTICATION_NO_SERVICE)
            response.pduDestination = bslpdu.pduSource
            self.request(response)
            return
        if conn.accessState != ConnectionState.NOT_AUTHENTICATED:
            if _debug:
                TCPServerMultiplexer._debug('    - connection in the wrong state: %r', conn.accessState)
            response = Result(AUTHENTICATION_FAILURE)
            response.pduDestination = bslpdu.pduSource
            self.request(response)
            return
        try:
            hashFn = hash_functions[bslpdu.bslciHashFn]
        except:
            if _debug:
                TCPServerMultiplexer._debug('    - no hash function: %r', bslpdu.bslciHashFn)
            response = Result(AUTHENTICATION_HASH)
            response.pduDestination = bslpdu.pduSource
            self.request(response)
            return

        conn.userinfo = conn.service.get_user_info(bslpdu.bslciUsername)
        if not conn.userinfo:
            if _debug:
                TCPServerMultiplexer._debug('    - no user info: %r', bslpdu.bslciUsername)
            response = Result(AUTHENTICATION_FAILURE)
            response.pduDestination = bslpdu.pduSource
            self.request(response)
            return
        challenge = hashFn(('').join(chr(random.randrange(256)) for i in range(128)))
        conn.challenge = challenge
        conn.accessState = ConnectionState.CHALLENGED
        response = AccessChallenge(bslpdu.bslciHashFn, challenge)
        response.pduDestination = conn.address
        self.request(response)

    def do_AccessResponse(self, conn, bslpdu):
        if _debug:
            TCPServerMultiplexer._debug('do_AccessResponse %r %r', conn, bslpdu)
        resultCode = SUCCESS
        if not conn.userinfo:
            if _debug:
                TCPServerMultiplexer._debug('    - connection has no user info')
            resultCode = AUTHENTICATION_FAILURE
        elif conn.accessState != ConnectionState.CHALLENGED:
            if _debug:
                TCPServerMultiplexer._debug('    - connection in the wrong state: %r', conn.accessState)
            resultCode = AUTHENTICATION_FAILURE
        else:
            try:
                hashFn = hash_functions[bslpdu.bslciHashFn]
            except:
                if _debug:
                    TCPServerMultiplexer._debug('    - no hash function: %r', bslpdu.bslciHashFn)
                response = Result(AUTHENTICATION_HASH)
                response.pduDestination = bslpdu.pduSource
                self.request(response)
                return

            challengeResponse = hashFn(conn.userinfo.password + conn.challenge)
            if challengeResponse == bslpdu.bslciResponse:
                if _debug:
                    TCPServerMultiplexer._debug('    - success')
                conn.accessState = ConnectionState.AUTHENTICATED
                if not conn.service:
                    if _debug:
                        TCPServerMultiplexer._debug('    - no service')
                elif not conn.userinfo.service[conn.service.serviceID]:
                    resultCode = AUTHENTICATION_NO_SERVICE
                    conn.service = None
                else:
                    conn.service.add_connection(conn)
            else:
                if _debug:
                    TCPServerMultiplexer._debug('    - challenge/response mismatch')
                resultCode = AUTHENTICATION_FAILURE
        response = Result(resultCode)
        response.pduDestination = bslpdu.pduSource
        self.request(response)
        return


@bacpypes_debugging
class TCPClientMultiplexer(Client):

    def __init__(self):
        if _debug:
            TCPClientMultiplexer._debug('__init__')
        Client.__init__(self)
        self.director = TCPClientDirector()
        bind(self, _StreamToPacket(), self.director)
        self.ase = TCPMultiplexerASE(self)
        bind(self.ase, self.director)
        self.connections = {}
        self.deviceToDeviceService = None
        self.routerToRouterService = None
        self.proxyService = None
        self.laneService = None
        return

    def request(self, pdu):
        if _debug:
            TCPClientMultiplexer._debug('request %r', pdu)
        xpdu = BSLPDU()
        pdu.encode(xpdu)
        if _debug:
            TCPClientMultiplexer._debug('    - xpdu: %r', xpdu)
        ypdu = PDU()
        xpdu.encode(ypdu)
        ypdu.pduDestination = unpack_ip_addr(pdu.pduDestination.addrAddr)
        if _debug:
            TCPClientMultiplexer._debug('    - ypdu: %r', ypdu)
        Client.request(self, ypdu)

    def indication(self, server, pdu):
        if _debug:
            TCPClientMultiplexer._debug('indication %r %r', server, pdu)
        self.request(pdu)

    def confirmation(self, pdu):
        if _debug:
            TCPClientMultiplexer._debug('confirmation %r', pdu)
        pdu = PDU(pdu, source=Address(pdu.pduSource))
        bslpdu = BSLPDU()
        bslpdu.decode(pdu)
        if _debug:
            TCPClientMultiplexer._debug('    - bslpdu: %r', bslpdu)
        conn = self.connections.get(pdu.pduSource, None)
        if not conn:
            TCPClientMultiplexer._warning('no connection: %r', pdu.pduSource)
            return
        fn = bslpdu.bslciFunction
        rpdu = bsl_pdu_types[fn]()
        rpdu.decode(bslpdu)
        if _debug:
            TCPClientMultiplexer._debug('    - rpdu: %r', rpdu)
        if fn == BSLCI.result:
            if not conn.service:
                TCPClientMultiplexer._warning('unexpected result')
                return
            if conn.connected:
                TCPClientMultiplexer._warning('unexpected result, already connected')
                return
            if rpdu.bslciResultCode == SUCCESS:
                if conn.accessState == ConnectionState.REQUESTED:
                    if _debug:
                        TCPClientMultiplexer._debug('    - authentication successful')
                    conn.accessState = ConnectionState.AUTHENTICATED
                conn.service.add_connection(conn)
                conn.service.connect_ack(conn, rpdu)
            elif rpdu.bslciResultCode == AUTHENTICATION_REQUIRED:
                if conn.accessState != ConnectionState.NOT_AUTHENTICATED:
                    TCPClientMultiplexer._warning('unexpected authentication required')
                    return
                conn.userinfo = conn.service.get_default_user_info(conn.address)
                if not conn.userinfo:
                    TCPClientMultiplexer._warning('authentication required, no user information')
                    return
                conn.accessState = ConnectionState.REQUESTED
                response = AccessRequest(0, conn.userinfo.username)
                response.pduDestination = rpdu.pduSource
                self.request(response)
            else:
                TCPClientMultiplexer._warning('result code: %r', rpdu.bslciResultCode)
        elif fn == BSLCI.serviceRequest:
            TCPClientMultiplexer._warning('unexpected service request')
        elif fn == BSLCI.deviceToDeviceAPDU and self.deviceToDeviceService:
            if conn.service is not self.deviceToDeviceService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.deviceToDeviceService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.routerToRouterNPDU and self.routerToRouterService:
            if conn.service is not self.routerToRouterService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.routerToRouterService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.proxyToServerUnicastNPDU and self.proxyService:
            TCPClientMultiplexer._warning('unexpected Proxy-To-Server-Unicast-NPDU')
        elif fn == BSLCI.proxyToServerBroadcastNPDU and self.proxyService:
            TCPClientMultiplexer._warning('unexpected Proxy-To-Broadcast-Unicast-NPDU')
        elif fn == BSLCI.serverToProxyUnicastNPDU and self.proxyService:
            if conn.service is not self.proxyService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.proxyService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.serverToProxyBroadcastNPDU and self.proxyService:
            if conn.service is not self.proxyService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.proxyService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.clientToLESUnicastNPDU and self.laneService:
            TCPClientMultiplexer._warning('unexpected Client-to-LES-Unicast-NPDU')
        elif fn == BSLCI.clientToLESBroadcastNPDU and self.laneService:
            TCPClientMultiplexer._warning('unexpected Client-to-LES-Broadcast-NPDU')
        elif fn == BSLCI.lesToClientUnicastNPDU and self.laneService:
            if conn.service is not self.laneService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.laneService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.lesToClientBroadcastNPDU and self.laneService:
            if conn.service is not self.laneService:
                TCPClientMultiplexer._warning('not connected to appropriate service')
                return
            self.laneService.service_confirmation(conn, rpdu)
        elif fn == BSLCI.accessRequest:
            TCPClientMultiplexer._warning('unexpected Access-request')
        elif fn == BSLCI.accessChallenge:
            self.do_AccessChallenge(conn, rpdu)
        elif fn == BSLCI.accessResponse:
            TCPClientMultiplexer._warning('unexpected Access-response')
        else:
            TCPClientMultiplexer._warning('unsupported message: %s', rpdu.__class__.__name__)
        return

    def do_AccessChallenge(self, conn, bslpdu):
        if _debug:
            TCPClientMultiplexer._debug('do_AccessRequest %r %r', conn, bslpdu)
        if conn.accessState != ConnectionState.REQUESTED:
            TCPClientMultiplexer._warning('unexpected access challenge')
            return
        try:
            hashFn = hash_functions[bslpdu.bslciHashFn]
        except:
            TCPClientMultiplexer._warning('no hash function: %r', bslpdu.bslciHashFn)
            return

        challengeResponse = hashFn(conn.userinfo.password + bslpdu.bslciChallenge)
        response = AccessResponse(bslpdu.bslciHashFn, challengeResponse)
        response.pduDestination = conn.address
        if _debug:
            TCPClientMultiplexer._debug('    - response: %r', response)
        self.request(response)


@bacpypes_debugging
class TCPMultiplexerASE(ApplicationServiceElement):

    def __init__(self, mux):
        if _debug:
            TCPMultiplexerASE._debug('__init__ %r', mux)
        self.multiplexer = mux

    def indication(self, *args, **kwargs):
        if _debug:
            TCPMultiplexerASE._debug('TCPMultiplexerASE %r %r', args, kwargs)
        if 'addPeer' in kwargs:
            addr = Address(kwargs['addPeer'])
            if _debug:
                TCPMultiplexerASE._debug('    - add peer: %r', addr)
            if addr in self.multiplexer.connections:
                if _debug:
                    TCPMultiplexerASE._debug('    - already a connection')
                return
            conn = ConnectionState(addr)
            if _debug:
                TCPMultiplexerASE._debug('    - conn: %r', conn)
            self.multiplexer.connections[addr] = conn
        if 'delPeer' in kwargs:
            addr = Address(kwargs['delPeer'])
            if _debug:
                TCPMultiplexerASE._info('    - delete peer: %r', addr)
            if addr not in self.multiplexer.connections:
                if _debug:
                    TCPMultiplexerASE._debug('    - not a connection')
                return
            conn = self.multiplexer.connections.get(addr)
            if _debug:
                TCPMultiplexerASE._debug('    - conn: %r', conn)
            if conn.service and conn.connected:
                conn.service.remove_connection(conn)
            del self.multiplexer.connections[addr]


@bacpypes_debugging
class DeviceToDeviceServerService(NetworkServiceAdapter):
    serviceID = DEVICE_TO_DEVICE_SERVICE_ID

    def process_npdu(self, npdu):
        """encode NPDUs from the service access point and send them downstream."""
        if _debug:
            DeviceToDeviceServerService._debug('process_npdu %r', npdu)
        if npdu.pduDestination.addrType == Address.localBroadcastAddr:
            destList = self.connections.keys()
        else:
            if npdu.pduDestination not in self.connections:
                if _debug:
                    DeviceToDeviceServerService._debug('    - not a connected client')
                return
            destList = [
             npdu.pduDestination]
        if _debug:
            DeviceToDeviceServerService._debug('    - destList: %r', destList)
        for dest in destList:
            xpdu = DeviceToDeviceAPDU(npdu)
            xpdu.pduDestination = dest
            self.service_request(xpdu)

    def service_confirmation(self, conn, pdu):
        if _debug:
            DeviceToDeviceServerService._debug('service_confirmation %r %r', conn, pdu)
        npdu = NPDU(pdu.pduData)
        npdu.pduSource = pdu.pduSource
        if _debug:
            DeviceToDeviceServerService._debug('    - npdu: %r', npdu)
        self.adapterSAP.process_npdu(self, npdu)


@bacpypes_debugging
class DeviceToDeviceClientService(NetworkServiceAdapter):
    serviceID = DEVICE_TO_DEVICE_SERVICE_ID

    def process_npdu(self, npdu):
        """encode NPDUs from the service access point and send them downstream."""
        if _debug:
            DeviceToDeviceClientService._debug('process_npdu %r', npdu)
        if npdu.pduDestination.addrType == Address.localBroadcastAddr:
            destList = self.connections.keys()
        else:
            conn = self.connections.get(npdu.pduDestination, None)
            if not conn:
                if _debug:
                    DeviceToDeviceClientService._debug('    - not a connected client')
                conn = self.connect(npdu.pduDestination)
            if not conn.connected:
                conn.pendingNPDU.append(npdu)
                return
            destList = [
             npdu.pduDestination]
        if _debug:
            DeviceToDeviceClientService._debug('    - destList: %r', destList)
        for dest in destList:
            xpdu = DeviceToDeviceAPDU(npdu)
            xpdu.pduDestination = dest
            self.service_request(xpdu)

        return

    def connect(self, addr):
        """Initiate a connection request to the device."""
        if _debug:
            DeviceToDeviceClientService._debug('connect %r', addr)
        conn = ConnectionState(addr)
        self.multiplexer.connections[addr] = conn
        conn.service = self
        conn.pendingNPDU = []
        request = ServiceRequest(DEVICE_TO_DEVICE_SERVICE_ID)
        request.pduDestination = addr
        self.service_request(request)
        return conn

    def connect_ack(self, conn, pdu):
        if _debug:
            DeviceToDeviceClientService._debug('connect_ack %r %r', conn, pdu)
        if pdu.bslciResultCode == 0:
            if conn.pendingNPDU:
                for npdu in conn.pendingNPDU:
                    xpdu = DeviceToDeviceAPDU(npdu)
                    xpdu.pduDestination = npdu.pduDestination
                    self.service_request(xpdu)

                conn.pendingNPDU = []

    def service_confirmation(self, conn, pdu):
        if _debug:
            DeviceToDeviceClientService._debug('service_confirmation %r %r', conn, pdu)
        npdu = NPDU(pdu.pduData)
        npdu.pduSource = pdu.pduSource
        if _debug:
            DeviceToDeviceClientService._debug('    - npdu: %r', npdu)
        self.adapterSAP.process_npdu(self, npdu)


@bacpypes_debugging
class RouterToRouterService(NetworkServiceAdapter):
    serviceID = ROUTER_TO_ROUTER_SERVICE_ID

    def process_npdu(self, npdu):
        """encode NPDUs from the service access point and send them downstream."""
        if _debug:
            RouterToRouterService._debug('process_npdu %r', npdu)
        pdu = PDU()
        npdu.encode(pdu)
        if _debug:
            RouterToRouterService._debug('    - pdu: %r', pdu)
        if pdu.pduDestination.addrType == Address.localBroadcastAddr:
            destList = self.connections.keys()
        else:
            conn = self.connections.get(pdu.pduDestination, None)
            if not conn:
                if _debug:
                    RouterToRouterService._debug('    - not a connected client')
                conn = self.connect(pdu.pduDestination)
            if not conn.connected:
                conn.pendingNPDU.append(pdu)
                return
            destList = [
             pdu.pduDestination]
        if _debug:
            RouterToRouterService._debug('    - destList: %r', destList)
        for dest in destList:
            xpdu = RouterToRouterNPDU(pdu)
            xpdu.pduDestination = dest
            self.service_request(xpdu)

        return

    def connect(self, addr):
        """Initiate a connection request to the peer router."""
        if _debug:
            RouterToRouterService._debug('connect %r', addr)
        conn = ConnectionState(addr)
        self.multiplexer.connections[addr] = conn
        conn.service = self
        conn.pendingNPDU = []
        request = ServiceRequest(ROUTER_TO_ROUTER_SERVICE_ID)
        request.pduDestination = addr
        self.service_request(request)
        return conn

    def connect_ack(self, conn, pdu):
        if _debug:
            RouterToRouterService._debug('connect_ack %r %r', conn, pdu)
        if pdu.bslciResultCode == 0:
            if conn.pendingNPDU:
                for npdu in conn.pendingNPDU:
                    xpdu = RouterToRouterNPDU(npdu)
                    xpdu.pduDestination = npdu.pduDestination
                    self.service_request(xpdu)

                conn.pendingNPDU = []

    def add_connection(self, conn):
        if _debug:
            RouterToRouterService._debug('add_connection %r', conn)
        NetworkServiceAdapter.add_connection(self, conn)

    def remove_connection(self, conn):
        if _debug:
            RouterToRouterService._debug('remove_connection %r', conn)
        NetworkServiceAdapter.remove_connection(self, conn)
        self.adapterSAP.remove_router_references(self, conn.address)

    def service_confirmation(self, conn, pdu):
        if _debug:
            RouterToRouterService._debug('service_confirmation %r %r', conn, pdu)
        npdu = NPDU()
        npdu.decode(pdu)
        npdu.pduSource = pdu.pduSource
        if _debug:
            ProxyServiceNetworkAdapter._debug('    - npdu: %r', npdu)
        self.adapterSAP.process_npdu(self, npdu)


@bacpypes_debugging
class ProxyServiceNetworkAdapter(NetworkAdapter):

    def __init__(self, conn, sap, net, cid=None):
        if _debug:
            ProxyServiceNetworkAdapter._debug('__init__ %r %r %r status=0 cid=%r', conn, sap, net, cid)
        NetworkAdapter.__init__(self, sap, net, cid)
        self.conn = conn

    def process_npdu(self, npdu):
        """encode NPDUs from the network service access point and send them to the proxy."""
        if _debug:
            ProxyServiceNetworkAdapter._debug('process_npdu %r', npdu)
        pdu = PDU()
        npdu.encode(pdu)
        if _debug:
            ProxyServiceNetworkAdapter._debug('    - pdu: %r', pdu)
        if pdu.pduDestination.addrType == Address.localBroadcastAddr:
            xpdu = ServerToProxyBroadcastNPDU(pdu)
        else:
            xpdu = ServerToProxyUnicastNPDU(pdu.pduDestination, pdu)
        xpdu.pduDestination = self.conn.address
        self.conn.service.service_request(xpdu)

    def service_confirmation(self, bslpdu):
        """Receive packets forwarded by the proxy and send them upstream to the network service access point."""
        if _debug:
            ProxyServiceNetworkAdapter._debug('service_confirmation %r', bslpdu)
        pdu = NPDU(bslpdu.pduData)
        pdu.pduSource = bslpdu.bslciAddress
        if isinstance(bslpdu, ProxyToServerBroadcastNPDU):
            pdu.pduDestination = LocalBroadcast()
        if _debug:
            ProxyServiceNetworkAdapter._debug('    - pdu: %r', pdu)
        npdu = NPDU()
        npdu.decode(pdu)
        if _debug:
            ProxyServiceNetworkAdapter._debug('    - npdu: %r', npdu)
        self.adapterSAP.process_npdu(self, npdu)


@bacpypes_debugging
class ProxyServerService(ServiceAdapter):
    serviceID = PROXY_SERVICE_ID

    def __init__(self, mux, nsap):
        if _debug:
            ProxyServerService._debug('__init__ %r %r', mux, nsap)
        ServiceAdapter.__init__(self, mux)
        self.nsap = nsap

    def add_connection(self, conn):
        if _debug:
            ProxyServerService._debug('add_connection %r', conn)
        ServiceAdapter.add_connection(self, conn)
        conn.proxyAdapter = ProxyServiceNetworkAdapter(conn, self.nsap, conn.userinfo.proxyNetwork)
        if _debug:
            ProxyServerService._debug('    - proxyAdapter: %r', conn.proxyAdapter)

    def remove_connection(self, conn):
        if _debug:
            ProxyServerService._debug('remove_connection %r', conn)
        ServiceAdapter.remove_connection(self, conn)
        self.nsap.adapters.remove(conn.proxyAdapter)

    def service_confirmation(self, conn, bslpdu):
        """Receive packets forwarded by the proxy and redirect them to the proxy network adapter."""
        if _debug:
            ProxyServerService._debug('service_confirmation %r %r', conn, bslpdu)
        if not getattr(conn, 'proxyAdapter', None):
            raise RuntimeError('service confirmation received but no adapter for it')
        conn.proxyAdapter.service_confirmation(bslpdu)
        return


@bacpypes_debugging
class ProxyClientService(ServiceAdapter, Client):
    serviceID = PROXY_SERVICE_ID

    def __init__(self, mux, addr=None, userinfo=None, cid=None):
        if _debug:
            ProxyClientService._debug('__init__ %r %r userinfo=%r cid=%r', mux, addr, userinfo, cid)
        ServiceAdapter.__init__(self, mux)
        Client.__init__(self, cid)
        self.address = addr
        self.userinfo = userinfo

    def get_default_user_info(self, addr):
        """get the user information to authenticate."""
        if _debug:
            ProxyClientService._debug('get_default_user_info %r', addr)
        return self.userinfo

    def connect(self, addr=None, userinfo=None):
        """Initiate a connection request to the device."""
        if _debug:
            ProxyClientService._debug('connect addr=%r', addr)
        if addr:
            self.address = addr
        else:
            addr = self.address
        if userinfo:
            self.userinfo = userinfo
        conn = ConnectionState(addr)
        self.multiplexer.connections[addr] = conn
        if _debug:
            ProxyClientService._debug('    - conn: %r', conn)
        conn.service = self
        conn.pendingBSLPDU = []
        request = ServiceRequest(PROXY_SERVICE_ID)
        request.pduDestination = addr
        self.service_request(request)
        return conn

    def connect_ack(self, conn, bslpdu):
        if _debug:
            ProxyClientService._debug('connect_ack %r %r', conn, bslpdu)
        if bslpdu.bslciResultCode == 0:
            if conn.pendingBSLPDU:
                for pdu in conn.pendingBSLPDU:
                    self.service_request(pdu)

                conn.pendingBSLPDU = []
        else:
            ProxyClientService._warning('connection nack: %r', bslpdu.bslciResultCode)

    def service_confirmation(self, conn, bslpdu):
        if _debug:
            ProxyClientService._debug('service_confirmation %r %r', conn, bslpdu)
        pdu = PDU(bslpdu)
        if isinstance(bslpdu, ServerToProxyUnicastNPDU):
            pdu.pduDestination = bslpdu.bslciAddress
        elif isinstance(bslpdu, ServerToProxyBroadcastNPDU):
            pdu.pduDestination = LocalBroadcast()
        if _debug:
            ProxyClientService._debug('    - pdu: %r', pdu)
        self.request(pdu)

    def confirmation(self, pdu):
        if _debug:
            ProxyClientService._debug('confirmation %r ', pdu)
        if not self.address:
            raise RuntimeError('no connection address')
        if pdu.pduDestination.addrType == Address.localBroadcastAddr:
            request = ProxyToServerBroadcastNPDU(pdu.pduSource, pdu)
        else:
            request = ProxyToServerUnicastNPDU(pdu.pduSource, pdu)
        request.pduDestination = self.address
        conn = self.connections.get(self.address, None)
        if not conn:
            if _debug:
                ProxyClientService._debug('    - not a connected client')
            conn = self.connect()
        if not conn.connected:
            conn.pendingBSLPDU.append(request)
        else:
            self.service_request(request)
        return