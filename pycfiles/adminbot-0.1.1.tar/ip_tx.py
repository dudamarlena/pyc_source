# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_utils/net_utils/ip_tx.py
# Compiled at: 2018-01-31 14:44:08
__doc__ = '\nSimple IP packet generator/client test tool.\nProvides very limited support for testing specific IP protocols. Primarily used to test\nspecific network paths in a cloud or data center traversing firewalls/security groups, nat points,\netc..\n'
from os.path import abspath, basename
from random import getrandbits
import array, socket, struct, sys, time
from optparse import OptionParser, OptionValueError
ICMP_ECHO_REQUEST = 8
ICMP_EHCO_REPLY = 0
CHUNK_DATA = 0
CHUNK_INIT = 1
CHUNK_HEARTBEAT = 3
TRACE = 3
DEBUG = 2
INFO = 1
QUIET = 0
VERBOSE_LVL = INFO

def get_script_path():
    """
    Returns the path to this script
    """
    try:
        import inspect
    except ImportError:
        return

    return abspath(inspect.stack()[0][1])


def sftp_file(sshconnection, verbose_level=DEBUG):
    """
    Uploads this script using the sshconnection's sftp interface to the sshconnection host.
    :param sshconnection: SshConnection object
    :param verbose_level: The level at which this method should log it's output.
    """
    script_path = get_script_path()
    script_name = basename(script_path)
    sshconnection.sftp_put(script_path, script_name)
    debug(('Done Copying script:"{0}" to "{1}"').format(script_name, sshconnection.host), verbose_level)
    return script_name


def debug(msg, level=DEBUG):
    """
    Write debug info to stdout filtering on the set verbosity level and prefixing each line
    with a '#' to allow for easy parsing of results from output.
    :param msg: string to print
    :param level: verbosity level of this message
    :return: None
    """
    if not VERBOSE_LVL:
        return
    if VERBOSE_LVL >= level:
        for line in str(msg).splitlines():
            sys.stdout.write(('# {0}\n').format(str(line)))
            sys.stdout.flush()


def get_src(dest):
    """
    Attempts to learn the source IP from the outbound interface used to reach the provided
    destination
    :param dest: destination address/ip
    :return: local ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.connect((dest, 1))
    source_ip = s.getsockname()[0]
    s.close()
    return source_ip


def remote_sender(ssh, dst_addr, port=None, srcport=None, proto=17, count=1, socktimeout=10, timeout=15, data=None, verbose=False, interval=0.1, cb=None, cbargs=None):
    """
    Uses the ssh SshConnection obj's sftp interface to transfer this script to the remote
    machine and execute it with the parameters provided. Will return the combined stdout & stderr
    of the remote session.

    :param ssh: SshConnection object to run this script
    :param dst_addr: Where to send packets to
    :param port: The destination port of the packets (depending on protocol support)
    :param srcport: The source port to use in the sent packets
    :param proto: The IP protocol number (ie: 1=icmp, 6=tcp, 17=udp, 132=sctp)
    :param count: The number of packets to send
    :param timeout: The max amount of time allowed for the remote command to execute
    :param socktimeout: Time out used for socket operations
    :param data: Optional data to append to the built packet(s)
    :param verbose: Boolean to enable/disable printing of debug info
    :param cb: A method/function to be used as a call back to handle the ssh command's output
               as it is received. Must return type sshconnection.SshCbReturn
    :param cbargs: list of args to be provided to callback cb.
    :return: :raise RuntimeError: If remote command return status != 0
    """
    if verbose:
        verbose_level = VERBOSE_LVL
    else:
        verbose_level = DEBUG
    script = sftp_file(ssh, verbose_level=verbose_level)
    cmd = ('python {0} -o {1} -c {2} -d {3} -i {4} -t {5} ').format(script, proto, count, dst_addr, interval, socktimeout)
    if port:
        cmd += (' -p {0} ').format(port)
    if srcport is not None:
        cmd += (' -s {0} ').format(srcport)
    if data is not None:
        cmd += (' -l "{0}"').format(data.strip('"'))
    out = ''
    debug(('CMD: {0}').format(cmd), verbose_level)
    cmddict = ssh.cmd(cmd, listformat=False, timeout=timeout, cb=cb, cbargs=cbargs, verbose=verbose)
    out += cmddict.get('output')
    if cmddict.get('status') != 0:
        raise RuntimeError(('{0}\n"{1}" cmd failed with status:{2}, on host:{3}').format(out, cmd, cmddict.get('status'), ssh.host))
    debug(out, verbose_level)
    return out


def send_ip_packet(destip, proto=4, count=1, interval=0.1, payload=None, timeout=10):
    """
    Send a raw ip packet, payload can be used to append to the IP header...
    :param destip: Destination ip
    :param proto: protocol to use, default is 4
    :param payload: optional string buffer to append to IP packet
    """
    s = None
    if payload is None:
        payload = 'IP TEST PACKET'
    payload = payload or ''
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
            s.settimeout(timeout)
            for x in xrange(0, count):
                s.sendto(payload, (destip, 0))
                time.sleep(interval)

        except socket.error as SE:
            if SE.errno == 1 and 'not permitted' in SE.strerror:
                sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
            raise

    finally:
        if s:
            s.close()

    return


def send_sctp_packet(destip, dstport=101, srcport=100, proto=132, ptype=None, payload=None, sctpobj=None, count=1, interval=0.1, timeout=10):
    """
    Send Basic SCTP packets

    :param destip: Destination IP to send SCTP packet to
    :param dstport: Destination port to use in the SCTP packet
    :param srcport: Source port to use in the SCTP packet
    :param proto: Protocol number to use, default is 132 for SCTP
    :param ptype: SCTP type, default is 'init' type
    :param payload: optional payload to use in packets (ie data chunk payload)
    :param sctpobj: A pre-built sctpobj to be sent
    """
    s = None
    if payload is None:
        payload = 'SCTP TEST PACKET'
    payload = payload or ''
    if ptype is None:
        ptype = CHUNK_INIT
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
            s.setsockopt(socket.SOL_IP, socket.IP_TOS, 2)
            s.settimeout(timeout)
            if not sctpobj:
                sctpobj = SCTP(srcport=srcport, dstport=dstport, ptype=ptype, payload=payload)
            for x in xrange(0, count):
                s.sendto(sctpobj.pack(), (destip, dstport))
                time.sleep(interval)

        except socket.error as SE:
            if SE.errno == 1 and 'not permitted' in SE.strerror:
                sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
            raise

    finally:
        if s:
            s.close()

    return


def send_udp_packet(destip, srcport=None, dstport=101, proto=17, payload=None, count=1, interval=0.1, timeout=10):
    """
    Send basic UDP packet

    :param destip: Destination IP to send UDP packet
    :param srcport: source port to use in the UDP packet, if provided will attempt to bind
                    to this port
    :param dstport: destination port to use in the UDP packet
    :param proto: protocol number, default is 17 for UDP
    :param payload: optional payload for this packet
    """
    s = None
    if payload is None:
        payload = 'UDP TEST PACKET'
    payload = payload or ''
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto)
            s.settimeout(timeout)
            if srcport is not None:
                s.bind(('', srcport))
            for x in xrange(0, count):
                s.sendto(payload, (destip, dstport))
                time.sleep(interval)

        except socket.error as SE:
            if SE.errno == 1 and 'not permitted' in SE.strerror:
                sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
            raise

    finally:
        if s:
            s.close()

    return


def send_tcp_packet(destip, dstport=101, srcport=None, proto=6, payload=None, bufsize=None, count=1, interval=0.1, timeout=10):
    """
    Send basic TCP packet

    :param destip: Destination IP to send TCP packet
    :param dstport: destination port to use in this TCP packet
    :param srcport: source port to use in this TCP packet. If provided will attempt to bind
                    to this port
    :param proto: protocol number, default is 6 for TCP
    :param payload: optional payload for this packet
    :param bufsize: Buffer size for recv() on socket after sending packet
    :return: Any data read on socket after sending the packet
    """
    data = ''
    s = None
    if payload is None:
        payload = 'TCP TEST PACKET'
    payload = payload or ''
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
            s.settimeout(timeout)
            if srcport is not None:
                s.bind(('', srcport))
            s.connect((destip, dstport))
            for x in xrange(0, count):
                s.send(payload)
                if bufsize:
                    data += s.recv(bufsize)
                time.sleep(interval)

        except socket.error as SE:
            if SE.errno == 1 and 'not permitted' in SE.strerror:
                sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
            raise

    finally:
        if s:
            s.close()

    return data


def send_icmp_packet(destip, id=1234, seqnum=1, code=0, proto=1, ptype=None, count=1, interval=0.1, payload='ICMP TEST PACKET', timeout=10):
    """
    Send basic ICMP packet (note: does not wait for, or validate a response)

    :param destip: Destination IP to send ICMP packet to
    :param id: ID, defaults to '1234'
    :param seqnum: Sequence number, defaults to '1'
    :param code: ICMP subtype, default to 0
    :param proto: protocol number, defaults to 1 for ICMP
    :param ptype: ICMP type, defaults to icmp echo request
    :param payload: optional payload
    """
    if payload is None:
        payload = 'ICMP TEST PACKET'
    payload = payload or ''
    s = None
    if ptype is None:
        ptype = ICMP_ECHO_REQUEST
    try:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
            s.settimeout(timeout)
            icmp = ICMP(destaddr=destip, id=id, seqnum=seqnum, code=code, ptype=ptype, payload=payload)
            for x in xrange(0, count):
                s.sendto(icmp.pack(), (destip, 0))
                time.sleep(interval)

        except socket.error as SE:
            if SE.errno == 1 and 'not permitted' in SE.strerror:
                sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
            raise

    finally:
        if s:
            s.close()

    return


def send_packet(destip, proto, srcport=None, dstport=345, ptype=None, payload=None, count=1, interval=0.1, timeout=10, verbose=DEBUG):
    """
    Wrapper to sends packets of varying types
    :param destip: Destination IP to send packet to
    :param proto: IP protocol number (ie:1=icmp, 6=tcp, 17=udp, 132=sctp)
    :param srcport: Source port to use in packet (Depends on protocol)
    :param dstport: Destination port to use in packet (Depends on protocol)
    :param ptype: Packet type (if protocol supports subtypes)
    :param payload: Optional payload to send with packet
    :param count: Number of packets to send
    :param verbose: Sets the level info will be logged at
    """
    debug(('send_packet: destip:{0}, dstport:{1}, proto:{2}, ptype:{3}, count:{4}, interval:{5}').format(destip, dstport, proto, ptype, count, interval), level=verbose)
    if proto in (1, 'icmp'):
        send_icmp_packet(destip=destip, ptype=ptype, payload=payload, count=count, interval=interval, timeout=timeout)
    elif proto in (6, 'tcp'):
        send_tcp_packet(destip=destip, srcport=srcport, dstport=dstport, payload=payload, count=count, interval=interval, timeout=timeout)
    elif proto in (17, 'udp'):
        send_udp_packet(destip=destip, srcport=srcport, dstport=dstport, payload=payload, count=count, interval=interval, timeout=timeout)
    elif proto in (132, 'sctp'):
        send_sctp_packet(destip=destip, srcport=srcport, ptype=ptype, dstport=dstport, payload=payload, count=count, interval=interval, timeout=timeout)
    else:
        send_ip_packet(destip=destip, proto=proto, payload=payload, count=count, interval=interval, timeout=timeout)


class ICMP(object):

    def __init__(self, destaddr, id=1234, seqnum=1, code=0, ptype=None, payload=None):
        self.destaddr = destaddr
        if payload is None:
            payload = 'ICMP TEST PACKET'
        self.payload = payload or ''
        self.icmptype = ptype or ICMP_ECHO_REQUEST
        self.id = id
        self.code = code
        self.seqnum = seqnum
        return

    def pack(self):
        tmp_checksum = 0
        header = struct.pack('bbHHh', self.icmptype, self.code, tmp_checksum, self.id, self.seqnum)
        fin_checksum = checksum(header + self.payload)
        header = struct.pack('bbHHh', self.icmptype, self.code, socket.htons(fin_checksum), self.id, self.seqnum)
        packet = header + self.payload
        return packet


class InitChunk(object):

    def __init__(self, tag=None, a_rwnd=62464, outstreams=10, instreams=65535, tsn=None, param_data=None):
        self.tag = tag or getrandbits(32) or 3
        self.a_rwnd = a_rwnd
        self.outstreams = outstreams or 1
        self.instreams = instreams or 1
        self.tsn = tsn or getrandbits(32) or 4
        if param_data is None:
            param_data = ''
            suppaddrtypes = SctpSupportedAddrTypesParam()
            param_data += suppaddrtypes.pack()
            ecn = SctpEcnParam()
            param_data += ecn.pack()
            fwdtsn = SctpFwdTsnSupportParam()
            param_data += fwdtsn.pack()
        self.param_data = param_data
        return

    def pack(self):
        packet = struct.pack('!IIHHI', self.tag, self.a_rwnd, self.outstreams, self.instreams, self.tsn)
        if self.param_data:
            packet += self.param_data
        return packet


class SctpIPv4Param(object):

    def __init__(self, type=5, length=8, ipv4addr=None):
        self.type = type
        self.length = length
        self.addr = ipv4addr

    def pack(self):
        packet = struct.pack('!HHI', self.type, self.length, self.addr)
        return packet


class SctpSupportedAddrTypesParam(object):

    def __init__(self, ptype=12, addr_types=None):
        ipv4 = 5
        if addr_types is None:
            addr_types = [
             ipv4]
        if not isinstance(addr_types, list):
            addr_types = [
             addr_types]
        self.addr_types = addr_types
        self.ptype = 12
        self.length = 4 + 2 * len(self.addr_types)
        return

    def pack(self):
        fmt = '!HH'
        contents = [self.ptype, self.length]
        for atype in self.addr_types:
            fmt += 'H'
            contents.append(atype)

        contents = tuple(contents)
        packet = struct.pack(fmt, *contents)
        if len(self.addr_types) % 2:
            packet += struct.pack('H', 0)
        return packet


class SctpEcnParam(object):

    def __init__(self, ptype=32768):
        self.ptype = ptype
        self.length = 4

    def pack(self):
        return struct.pack('!HH', self.ptype, self.length)


class SctpFwdTsnSupportParam(object):

    def __init__(self, ptype=49152):
        self.ptype = ptype
        self.length = 4

    def pack(self):
        return struct.pack('!HH', self.ptype, self.length)


class DataChunk(object):

    def __init__(self, tsn=1, stream_id=12345, stream_seq=54321, payload_proto=0, payload=None):
        if payload is None:
            payload = 'TEST SCTP DATA CHUNK'
        self.payload = payload
        self.tsn = tsn
        self.stream_id = stream_id
        self.stream_seq = stream_seq
        self.payload_proto = payload_proto
        return

    @property
    def length(self):
        return 12 + len(self.payload)

    def pack(self):
        packet = struct.pack('!iHHi', self.tsn, self.stream_id, self.stream_seq, self.payload_proto)
        packet += self.payload
        return packet


class HeartBeatChunk(object):

    def __init__(self, parameter=1, payload=None):
        self.parameter = parameter
        if payload is None:
            payload = str(getrandbits(64))
        self.hb_info = payload
        self.hb_info_length = 4 + len(payload)
        return

    def pack(self):
        chunk = struct.pack('!HH', self.parameter, self.hb_info_length)
        chunk += self.hb_info
        return chunk


class ChunkHdr(object):

    def __init__(self, chunktype=None, flags=0, payload=None, chunk=None):
        if chunktype is None:
            chunktype = 1
        self.chunktype = chunktype
        self.chunkflags = flags
        if chunk:
            self.chunkobj = chunk
        elif chunktype == 0:
            self.chunkobj = DataChunk(payload=payload)
        elif chunktype == 1:
            self.chunkobj = InitChunk()
        elif chunktype == 4:
            self.chunkobj = HeartBeatChunk(payload=payload)
        self.chunk_data = self.chunkobj.pack()
        self.chunklength = 4
        self.chunklength = 4 + len(self.chunk_data)
        return

    def pack(self):
        chunk = struct.pack('!bbH', self.chunktype, self.chunkflags, self.chunklength)
        packet = chunk + self.chunk_data
        return packet


class SCTP(object):
    """
    Chunk Types
    0   DATA    Payload data
    1   INIT    Initiation
    2   INIT ACK        initiation acknowledgement
    3   SACK    Selective acknowledgement
    4   HEARTBEAT       Heartbeat request
    5   HEARTBEAT ACK   Heartbeat acknowledgement
    6   ABORT   Abort
    7   SHUTDOWN        Shutdown
    8   SHUTDOWN ACK    Shutdown acknowledgement
    9   ERROR   Operation error
    10  COOKIE ECHO     State cookie
    11  COOKIE ACK      Cookie acknowledgement
    12  ECNE    Explicit congestion notification echo (reserved)
    13  CWR     Congestion window reduced (reserved)
    14  SHUTDOWN COMPLETE

    Chunk Flags
    # I - SACK chunk should be sent back without delay.
    # U - If set, this indicates this data is an unordered chunk and the stream sequence number
          is invalid. If an unordered chunk is fragmented then each fragment has this flag set.
    # B - If set, this marks the beginning fragment. An unfragmented chunk has this flag set.
    # E - If set, this marks the end fragment. An unfragmented chunk has this flag set
    """

    def __init__(self, srcport, dstport, tag=None, ptype=None, payload=None, chunk=None):
        self.src = srcport
        self.dst = dstport
        self.checksum = 0
        if ptype is None:
            ptype = CHUNK_INIT
            tag = 0
        if tag is None:
            if ptype == CHUNK_INIT:
                tag = 0
            else:
                tag = getrandbits(16)
        self.tag = tag
        chunk = chunk or ChunkHdr(chunktype=ptype, payload=payload)
        self.chunk = chunk.pack()
        return

    def pack(self, src=None, dst=None, tag=None, do_checksum=True):
        src = src or self.src
        dst = dst or self.dst
        verification_tag = tag or self.tag
        packet = struct.pack('!HHII', src, dst, verification_tag, 0)
        chunk = self.chunk
        if not do_checksum:
            packet += chunk
            return packet
        pktchecksum = cksum(packet + chunk)
        packet = struct.pack('!HHII', src, dst, verification_tag, pktchecksum)
        packet += chunk
        return packet


def checksum(source_string):
    """
    From: https://github.com/samuel/python-ping
    Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.
    """
    sum = 0
    count_to = len(source_string) / 2 * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[(count + 1)]) * 256 + ord(source_string[count])
        sum = sum + this_val
        sum = sum & 4294967295
        count = count + 2

    if count_to < len(source_string):
        sum = sum + ord(source_string[(len(source_string) - 1)])
        sum = sum & 4294967295
    sum = (sum >> 16) + (sum & 65535)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 65535
    answer = answer >> 8 | answer << 8 & 65280
    return answer


crc32c_table = (0, 4067132163, 3778769143, 324072436, 3348797215, 904991772, 648144872,
                3570033899, 2329499855, 2024987596, 1809983544, 2575936315, 1296289744,
                3207089363, 2893594407, 1578318884, 274646895, 3795141740, 4049975192,
                51262619, 3619967088, 632279923, 922689671, 3298075524, 2592579488,
                1760304291, 2075979607, 2312596564, 1562183871, 2943781820, 3156637768,
                1313733451, 549293790, 3537243613, 3246849577, 871202090, 3878099393,
                357341890, 102525238, 4101499445, 2858735121, 1477399826, 1264559846,
                3107202533, 1845379342, 2677391885, 2361733625, 2125378298, 820201905,
                3263744690, 3520608582, 598981189, 4151959214, 85089709, 373468761,
                3827903834, 3124367742, 1213305469, 1526817161, 2842354314, 2107672161,
                2412447074, 2627466902, 1861252501, 1098587580, 3004210879, 2688576843,
                1378610760, 2262928035, 1955203488, 1742404180, 2511436119, 3416409459,
                969524848, 714683780, 3639785095, 205050476, 4266873199, 3976438427,
                526918040, 1361435347, 2739821008, 2954799652, 1114974503, 2529119692,
                1691668175, 2005155131, 2247081528, 3690758684, 697762079, 986182379,
                3366744552, 476452099, 3993867776, 4250756596, 255256311, 1640403810,
                2477592673, 2164122517, 1922457750, 2791048317, 1412925310, 1197962378,
                3037525897, 3944729517, 427051182, 170179418, 4165941337, 746937522,
                3740196785, 3451792453, 1070968646, 1905808397, 2213795598, 2426610938,
                1657317369, 3053634322, 1147748369, 1463399397, 2773627110, 4215344322,
                153784257, 444234805, 3893493558, 1021025245, 3467647198, 3722505002,
                797665321, 2197175160, 1889384571, 1674398607, 2443626636, 1164749927,
                3070701412, 2757221520, 1446797203, 137323447, 4198817972, 3910406976,
                461344835, 3484808360, 1037989803, 781091935, 3705997148, 2460548119,
                1623424788, 1939049696, 2180517859, 1429367560, 2807687179, 3020495871,
                1180866812, 410100952, 3927582683, 4182430767, 186734380, 3756733383,
                763408580, 1053836080, 3434856499, 2722870694, 1344288421, 1131464017,
                2971354706, 1708204729, 2545590714, 2229949006, 1988219213, 680717673,
                3673779818, 3383336350, 1002577565, 4010310262, 493091189, 238226049,
                4233660802, 2987750089, 1082061258, 1395524158, 2705686845, 1972364758,
                2279892693, 2494862625, 1725896226, 952904198, 3399985413, 3656866545,
                731699698, 4283874585, 222117402, 510512622, 3959836397, 3280807620,
                837199303, 582374963, 3504198960, 68661723, 4135334616, 3844915500,
                390545967, 1230274059, 3141532936, 2825850620, 1510247935, 2395924756,
                2091215383, 1878366691, 2644384480, 3553878443, 565732008, 854102364,
                3229815391, 340358836, 3861050807, 4117890627, 119113024, 1493875044,
                2875275879, 3090270611, 1247431312, 2660249211, 1828433272, 2141937292,
                2378227087, 3811616794, 291187481, 34330861, 4032846830, 615137029,
                3603020806, 3314634738, 939183345, 1776939221, 2609017814, 2295496738,
                2058945313, 2926798794, 1545135305, 1330124605, 3173225534, 4084100981,
                17165430, 307568514, 3762199681, 888469610, 3332340585, 3587147933,
                665062302, 2042050490, 2346497209, 2559330125, 1793573966, 3190661285,
                1279665062, 1595330642, 2910671697)

def add(crc, buf):
    buf = array.array('B', buf)
    for b in buf:
        crc = crc >> 8 ^ crc32c_table[((crc ^ b) & 255)]

    return crc


def done(crc):
    tmp = ~crc & 4294967295
    b0 = tmp & 255
    b1 = tmp >> 8 & 255
    b2 = tmp >> 16 & 255
    b3 = tmp >> 24 & 255
    crc = b0 << 24 | b1 << 16 | b2 << 8 | b3
    return crc


def cksum(buf):
    """Return computed CRC-32c checksum."""
    return done(add(4294967295, buf))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--dstport', dest='dstport', type='int', default=101, help='Destination Port', metavar='PORT')
    parser.add_option('-s', '--srcport', dest='srcport', type='int', default=100, help='Source Port', metavar='PORT')
    parser.add_option('-c', '--count', dest='count', type='int', default=1, help='Number of packets to send', metavar='COUNT')
    parser.add_option('-i', '--interval', dest='interval', type='float', default=0.1, help="Time interval between sending packets, default='.1'", metavar='INTERVAL')
    parser.add_option('-d', '--dst', dest='destip', default=None, help='Destination ip', metavar='IP')
    parser.add_option('-o', '--proto', dest='proto', type='int', default=17, help='Protocol number(Examples: 1:icmp, 6:tcp, 17:udp, 132:sctp), default:17', metavar='PROTOCOL')
    parser.add_option('-l', '--payload', dest='payload', default=None, help='Chunk, data, payload, etc', metavar='DATA')
    parser.add_option('-v', '--verbose', dest='verbose', type='int', default=DEBUG, help='Verbose level, 0=quiet, 1=info, 2=debug, 3=trace. Default=1')
    parser.add_option('-t', '--socktimeout', dest='socktimeout', type='float', default=10, help='Socket timeout in seconds', metavar='TIMEOUT')
    options, args = parser.parse_args()
    if not options.destip:
        raise OptionValueError("'-d / --dst' for destination IP/Addr must be provided")
    VERBOSE_LVL = options.verbose
    destip = options.destip
    proto = options.proto
    srcport = options.srcport
    interval = options.interval
    socktimeout = options.socktimeout
    if srcport is not None:
        srcport = int(srcport)
    dstport = int(options.dstport)
    payload = options.payload
    count = options.count
    send_packet(destip=destip, proto=proto, srcport=srcport, dstport=dstport, payload=payload, count=count, interval=interval, timeout=socktimeout)