# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/analysis.py
# Compiled at: 2020-04-20 14:21:19
"""
Analysis - Decoding pcap files

Before analyzing files, install libpcap-dev:

    $ sudo apt install libpcap-dev

then install pypcap:

    https://github.com/pynetwork/pypcap
"""
import sys, time, socket, struct
pcap = None
try:
    import pcap
except:
    pass

from .settings import settings
from .debugging import ModuleLogger, bacpypes_debugging, btox
from .pdu import PDU, Address
from .bvll import BVLPDU, bvl_pdu_types, ForwardedNPDU, DistributeBroadcastToNetwork, OriginalUnicastNPDU, OriginalBroadcastNPDU
from .npdu import NPDU, npdu_types
from .apdu import APDU, apdu_types, confirmed_request_types, unconfirmed_request_types, complex_ack_types, error_types, ConfirmedRequestPDU, UnconfirmedRequestPDU, SimpleAckPDU, ComplexAckPDU, SegmentAckPDU, ErrorPDU, RejectPDU, AbortPDU
_debug = 0
_log = ModuleLogger(globals())
_protocols = {socket.IPPROTO_TCP: 'tcp', socket.IPPROTO_UDP: 'udp', 
   socket.IPPROTO_ICMP: 'icmp'}

def strftimestamp(ts):
    return time.strftime('%d-%b-%Y %H:%M:%S', time.localtime(ts)) + '.%06d' % ((ts - int(ts)) * 1000000,)


@bacpypes_debugging
def decode_ethernet(s):
    if _debug:
        decode_ethernet._debug('decode_ethernet %s...', btox(s[:14]))
    d = {}
    d['destination_address'] = btox(s[0:6], ':')
    d['source_address'] = btox(s[6:12], ':')
    d['type'] = struct.unpack('!H', s[12:14])[0]
    d['data'] = s[14:]
    return d


@bacpypes_debugging
def decode_vlan(s):
    if _debug:
        decode_vlan._debug('decode_vlan %s...', btox(s[:4]))
    d = {}
    x = struct.unpack('!H', s[0:2])[0]
    d['priority'] = x >> 13 & 7
    d['cfi'] = x >> 12 & 1
    d['vlan'] = x & 4095
    d['type'] = struct.unpack('!H', s[2:4])[0]
    d['data'] = s[4:]
    return d


@bacpypes_debugging
def decode_ip(s):
    if _debug:
        decode_ip._debug('decode_ip %r', btox(s[:20]))
    d = {}
    d['version'] = (ord(s[0]) & 240) >> 4
    d['header_len'] = ord(s[0]) & 15
    d['tos'] = ord(s[1])
    d['total_len'] = struct.unpack('!H', s[2:4])[0]
    d['id'] = struct.unpack('!H', s[4:6])[0]
    d['flags'] = (ord(s[6]) & 224) >> 5
    d['fragment_offset'] = struct.unpack('!H', s[6:8])[0] & 31
    d['ttl'] = ord(s[8])
    d['protocol'] = _protocols.get(ord(s[9]), '0x%.2x ?' % ord(s[9]))
    d['checksum'] = struct.unpack('!H', s[10:12])[0]
    d['source_address'] = socket.inet_ntoa(s[12:16])
    d['destination_address'] = socket.inet_ntoa(s[16:20])
    if d['header_len'] > 5:
        d['options'] = s[20:4 * (d['header_len'] - 5)]
    else:
        d['options'] = None
    d['data'] = s[4 * d['header_len']:]
    return d


@bacpypes_debugging
def decode_udp(s):
    if _debug:
        decode_udp._debug('decode_udp %s...', btox(s[:8]))
    d = {}
    d['source_port'] = struct.unpack('!H', s[0:2])[0]
    d['destination_port'] = struct.unpack('!H', s[2:4])[0]
    d['length'] = struct.unpack('!H', s[4:6])[0]
    d['checksum'] = struct.unpack('!H', s[6:8])[0]
    d['data'] = s[8:8 + d['length'] - 8]
    return d


@bacpypes_debugging
def decode_packet(data):
    """decode the data, return some kind of PDU."""
    if _debug:
        decode_packet._debug('decode_packet %r', data)
    if not data:
        return
    else:
        d = decode_ethernet(data)
        pduSource = Address(d['source_address'])
        pduDestination = Address(d['destination_address'])
        data = d['data']
        if d['type'] == 33024:
            if _debug:
                decode_packet._debug('    - vlan found')
            d = decode_vlan(data)
            data = d['data']
        if d['type'] == 2048:
            if _debug:
                decode_packet._debug('    - IP found')
            d = decode_ip(data)
            pduSource, pduDestination = d['source_address'], d['destination_address']
            data = d['data']
            if d['protocol'] == 'udp':
                if _debug:
                    decode_packet._debug('    - UDP found')
                d = decode_udp(data)
                data = d['data']
                pduSource = Address((pduSource, d['source_port']))
                pduDestination = Address((pduDestination, d['destination_port']))
                if _debug:
                    decode_packet._debug('    - pduSource: %r', pduSource)
                    decode_packet._debug('    - pduDestination: %r', pduDestination)
            elif _debug:
                decode_packet._debug('    - not a UDP packet')
        else:
            if _debug:
                decode_packet._debug('    - not an IP packet')
            if not data:
                if _debug:
                    decode_packet._debug('    - empty packet')
                return
            pdu = PDU(data, source=pduSource, destination=pduDestination)
            if pdu.pduData[0] == b'\x81':
                if _debug:
                    decode_packet._debug('    - BVLL header found')
                try:
                    xpdu = BVLPDU()
                    xpdu.decode(pdu)
                    pdu = xpdu
                except Exception as err:
                    if _debug:
                        decode_packet._debug('    - BVLPDU decoding error: %r', err)
                    return pdu

                atype = bvl_pdu_types.get(pdu.bvlciFunction)
                if not atype:
                    if _debug:
                        decode_packet._debug('    - unknown BVLL type: %r', pdu.bvlciFunction)
                    return pdu
                try:
                    xpdu = pdu
                    bpdu = atype()
                    bpdu.decode(pdu)
                    if _debug:
                        decode_packet._debug('    - bpdu: %r', bpdu)
                    pdu = bpdu
                    if atype is ForwardedNPDU:
                        old_pdu_source = pdu.pduSource
                        pdu.pduSource = bpdu.bvlciAddress
                        if settings.route_aware:
                            pdu.pduSource.addrRoute = old_pdu_source
                    elif atype not in (DistributeBroadcastToNetwork, OriginalUnicastNPDU, OriginalBroadcastNPDU):
                        return pdu
                except Exception as err:
                    if _debug:
                        decode_packet._debug('    - decoding Error: %r', err)
                    return xpdu

            if pdu.pduData[0] != '\x01':
                if _debug:
                    decode_packet._debug('    - not a version 1 packet: %s...', btox(pdu.pduData[:30]))
                return
            try:
                npdu = NPDU()
                npdu.decode(pdu)
            except Exception as err:
                if _debug:
                    decode_packet._debug('    - decoding Error: %r', err)
                return

        if npdu.npduNetMessage is None:
            if _debug:
                decode_packet._debug('    - not a network layer message, try as an APDU')
            try:
                xpdu = APDU()
                xpdu.decode(npdu)
                apdu = xpdu
            except Exception as err:
                if _debug:
                    decode_packet._debug('    - decoding Error: %r', err)
                return npdu

            if npdu.npduSADR:
                apdu.pduSource = npdu.npduSADR
                if settings.route_aware:
                    apdu.pduSource.addrRoute = npdu.pduSource
            else:
                apdu.pduSource = npdu.pduSource
            if npdu.npduDADR:
                apdu.pduDestination = npdu.npduDADR
            else:
                apdu.pduDestination = npdu.pduDestination
            atype = apdu_types.get(apdu.apduType)
            if not atype:
                if _debug:
                    decode_packet._debug('    - unknown APDU type: %r', apdu.apduType)
                return apdu
            try:
                xpdu = apdu
                apdu = atype()
                apdu.decode(xpdu)
            except Exception as err:
                if _debug:
                    decode_packet._debug('    - decoding Error: %r', err)
                return xpdu

            if isinstance(apdu, ConfirmedRequestPDU):
                atype = confirmed_request_types.get(apdu.apduService)
                if atype or _debug:
                    decode_packet._debug('    - no confirmed request decoder: %r', apdu.apduService)
                return apdu
        else:
            if isinstance(apdu, UnconfirmedRequestPDU):
                atype = unconfirmed_request_types.get(apdu.apduService)
                if not atype:
                    if _debug:
                        decode_packet._debug('    - no unconfirmed request decoder: %r', apdu.apduService)
                    return apdu
            else:
                if isinstance(apdu, SimpleAckPDU):
                    atype = None
                else:
                    if isinstance(apdu, ComplexAckPDU):
                        atype = complex_ack_types.get(apdu.apduService)
                        if not atype:
                            if _debug:
                                decode_packet._debug('    - no complex ack decoder: %r', apdu.apduService)
                            return apdu
                    else:
                        if isinstance(apdu, SegmentAckPDU):
                            atype = None
                        elif isinstance(apdu, ErrorPDU):
                            atype = error_types.get(apdu.apduService)
                            if not atype:
                                if _debug:
                                    decode_packet._debug('    - no error decoder: %r', apdu.apduService)
                                return apdu
                        elif isinstance(apdu, RejectPDU):
                            atype = None
                        elif isinstance(apdu, AbortPDU):
                            atype = None
                        if _debug:
                            decode_packet._debug('    - atype: %r', atype)
                        try:
                            if atype:
                                xpdu = apdu
                                apdu = atype()
                                apdu.decode(xpdu)
                        except Exception as err:
                            if _debug:
                                decode_packet._debug('    - decoding error: %r', err)
                            return xpdu

                    return apdu
                ntype = npdu_types.get(npdu.npduNetMessage)
                if ntype or _debug:
                    decode_packet._debug('    - no network layer decoder: %r', npdu.npduNetMessage)
                return npdu
            if _debug:
                decode_packet._debug('    - ntype: %r', ntype)
            try:
                xpdu = npdu
                npdu = ntype()
                npdu.decode(xpdu)
            except Exception as err:
                if _debug:
                    decode_packet._debug('    - decoding error: %r', err)
                return xpdu

        return npdu
        return


@bacpypes_debugging
def decode_file(fname):
    """Given the name of a pcap file, open it, decode the contents and yield each packet."""
    if _debug:
        decode_file._debug('decode_file %r', fname)
    if not pcap:
        raise RuntimeError('failed to import pcap')
    p = pcap.pcap(fname)
    for i, (timestamp, data) in enumerate(p):
        try:
            pkt = decode_packet(data)
            if not pkt:
                continue
        except Exception as err:
            if _debug:
                decode_file._debug('    - exception decoding packet %d: %r', i + 1, err)
            continue

        pkt._number = i + 1
        pkt._timestamp = timestamp
        yield pkt


@bacpypes_debugging
class Tracer:

    def __init__(self, initial_state=None):
        if _debug:
            Tracer._debug('__init__ initial_state=%r', initial_state)
        self.next(initial_state or self.start)

    def next(self, fn):
        if _debug:
            Tracer._debug('next %r', fn)
        self.current_state = fn

    def start(self, pkt):
        if _debug:
            Tracer._debug('start %r', pkt)


@bacpypes_debugging
def trace(fname, tracers):
    if _debug:
        trace._debug('trace %r %r', fname, tracers)
    current_tracers = [ traceClass() for traceClass in tracers ]
    for pkt in decode_file(fname):
        for i, tracer in enumerate(current_tracers):
            tracer.current_state(pkt)
            if not tracer.current_state:
                current_tracers[i] = tracers[i]()


if __name__ == '__main__':
    try:
        try:
            from bacpypes.consolelogging import ConsoleLogHandler
            if '--debug' in sys.argv:
                indx = sys.argv.index('--debug')
                for i in range(indx + 1, len(sys.argv)):
                    ConsoleLogHandler(sys.argv[i])

                del sys.argv[indx:]
            _log.debug('initialization')
            for pkt in decode_file(sys.argv[1]):
                print (strftimestamp(pkt._timestamp), pkt.__class__.__name__)
                pkt.debug_contents()
                print ''

        except KeyboardInterrupt:
            pass
        except Exception as err:
            _log.exception('an error has occurred: %s', err)

    finally:
        _log.debug('finally')