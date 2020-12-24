# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pure_pcapy.py
# Compiled at: 2018-06-21 05:02:39
# Size of source mod 2**32: 10719 bytes
"""
pcapy clone in pure python
This module aims to support exactly the same interface as pcapy,
so that it can be used as a drop-in replacement. This means the module
does not and probably will never support live captures. Offline file
support should match the original though.
"""
import struct, logging
DLT_NULL = 0
DLT_EN10MB = 1
DLT_IEEE802 = 6
DLT_ARCNET = 7
DLT_SLIP = 8
DLT_PPP = 9
DLT_FDDI = 10
DLT_ATM_RFC1483 = 11
DLT_RAW = 12
DLT_PPP_SERIAL = 50
DLT_PPP_ETHER = 51
DLT_RAW = 101
DLT_C_HDLC = 104
DLT_IEEE802_11 = 105
DLT_LOOP = 108
DLT_LINUX_SLL = 113
DLT_LTALK = 114
DLT_IEEE802_15_4 = 195
DLT_IEEE802_15_4_NONASK_PHY = 215
DLT_IEEE802_15_4_NOFCS = 230
logger = logging.getLogger()
logger.warning('Soon to be deprecated! Use package instead!')

class PcapError(Exception):
    __doc__ = ' General Pcap module exception class '


def fixup_identical_short(short):
    """ noop for "fixing" big/little endian """
    return short


def fixup_identical_long(long_int):
    """ noop for "fixing" big/little endian """
    return long_int


def fixup_swapped_short(short):
    """ swap bytes in a 16b short """
    return (short & 255) << 8 | (short & 65280) >> 8


def fixup_swapped_long(long_int):
    """ swap swapped shorts in a 32b int """
    bottom = fixup_swapped_short(long_int & 65535)
    top = fixup_swapped_short(long_int >> 16 & 65535)
    return bottom << 16 & 4294901760 | top


fixup_sets = {b'\xd4\xc3\xb2\xa1':(
  fixup_identical_short, fixup_identical_long), 
 b'\xa1\xb2\xc3\xd4':(
  fixup_swapped_short, fixup_swapped_long)}

def open_offline(filename):
    """ opens the pcap file indicated by `filename` and returns a Reader object """
    if filename == '-':
        import sys
        source = sys.stdin
    else:
        try:
            source = open(filename, 'rb')
        except IOError as error:
            if error.args[0] == 21:
                raise PcapError('error reading dump file: %s' % error.args[1])
            else:
                raise PcapError('%s: %s' % (filename, error.args[1]))

    return Reader(source)


def open_live(_device, _snaplen, _promisc, _to_ms):
    raise NotImplementedError('This function is only available in pcapy')


def lookupdev():
    raise NotImplementedError('This function is only available in pcapy')


def findalldevs():
    raise NotImplementedError('This function is only available in pcapy')


def compile(_linktype, _snaplen, _filter, _optimize, _netmask):
    raise NotImplementedError('not implemented yet')


class Reader(object):
    __doc__ = '\n    An interface for reading an open pcap file.\n    This object can either read a single packet via `next()` or a series\n    via `loop()` or `dispatch()`.\n    '
    _Reader__GLOBAL_HEADER_LEN = 24
    _Reader__PACKET_HEADER_LEN = 16

    def __init__(self, source):
        """ creates a Reader instance from an open file object """
        self._Reader__source = source
        header = self._Reader__source.read(self._Reader__GLOBAL_HEADER_LEN)
        if len(header) < self._Reader__GLOBAL_HEADER_LEN:
            raise PcapError('truncated dump file; tried to read %i file header bytes, only got %i' % (
             self._Reader__GLOBAL_HEADER_LEN, len(header)))
        else:
            hdr_values = struct.unpack('IHHIIII', header)
            if header[:4] in fixup_sets:
                self.fixup_short, self.fixup_long = fixup_sets[header[:4]]
                logger.debug(header[:4])
                logger.debug(hdr_values)
            else:
                raise PcapError('bad dump file format')
        self.version_major, self.version_minor = [self.fixup_short(x) for x in hdr_values[1:3]]
        self.thiszone, self.sigfigs, self.snaplen, self.network = [self.fixup_long(x) for x in hdr_values[3:]]
        self.last_good_position = self._Reader__GLOBAL_HEADER_LEN
        logger.debug('pcap header: network: %s sigfigs: %s snaplen: %s network %s' % (
         self.thiszone, self.sigfigs, self.snaplen, self.network))

    def __loop_and_count(self, maxcant, callback):
        """
        reads up to `maxcant` packets and runs callback for each of them
        returns the number of packets processed
        """
        i = 0
        while True:
            if i >= maxcant > -1:
                break
            else:
                hdr, data = self.next()
                if hdr is None:
                    break
                else:
                    callback(hdr, data)
            i += 1

        return i

    def dispatch(self, maxcant, callback):
        """
        reads up to `maxcant` packets and runs callback for each of them
        returns the number of packets processed or 0 if no limit was specified
        """
        i = self._Reader__loop_and_count(maxcant, callback)
        if maxcant > -1:
            return i
        else:
            return 0

    def loop(self, maxcant, callback):
        """
        reads up to `maxcant` packets and runs callback for each of them
        does not return a value
        """
        self._Reader__loop_and_count(maxcant, callback)

    def next(self):
        """ reads the next packet from file and returns a (Pkthdr, data) tuple """
        header = self._Reader__source.read(self._Reader__PACKET_HEADER_LEN)
        if len(header) == 0:
            return (None, '')
        else:
            if len(header) < self._Reader__PACKET_HEADER_LEN:
                raise PcapError('truncated dump file; tried to read %i header bytes, only got %i' % (
                 self._Reader__PACKET_HEADER_LEN, len(header)))
            hdr_values = struct.unpack('IIII', header)
            ts_sec, ts_usec, incl_len, orig_len = [self.fixup_long(x) for x in hdr_values]
            data = self._Reader__source.read(incl_len)
            if len(data) < incl_len:
                raise PcapError('truncated dump file; tried to read %i captured bytes, only got %i' % (
                 incl_len, len(data)))
            pkthdr = Pkthdr(ts_sec, ts_usec, incl_len, orig_len)
            return (pkthdr, data)

    def getnet(self):
        raise NotImplementedError('This function is only available in pcapy')

    def getmask(self):
        raise NotImplementedError('This function is only available in pcapy')

    def datalink(self):
        """ returns the datalink type used in the current file """
        return self.network

    def getnonblock(self):
        """
        shows whether the operations are nonblocking, which is always 0 for files
        """
        return 0

    def setnonblock(self, state):
        """ this has no effect on savefiles, so is not implemented in pure-pcapy """
        pass

    def dump_open(self, filename):
        """
        create a new dumper object which inherits the network and snaplen information
        from the original reader
        """
        return Dumper(filename, self.snaplen, self.network)


class Dumper(object):
    __doc__ = "\n    Interface for pcap files, which can be used for creating new files.\n    Although this is accessible only through `Reader.dump_open()` in the\n    original pcapy, there's no good reason for that limitation and this object\n    can be used directly. It implements some sanity checking before the packet\n    is written to the file.\n    Files created this way are always stored using the native byte order.\n    "

    def __init__(self, filename, snaplen, network):
        """ creates a new dumper object which can be used for writing pcap files """
        self.store = open(filename, 'wb')
        self.store.write(struct.pack('IHHIIII', 2712847316, 2, 4, 0, 0, snaplen, network))
        self.store.flush()

    def dump(self, header, data):
        """ writes a new header and packet to the file, then forces a file flush """
        if not isinstance(header, Pkthdr):
            raise PcapError('not a proper Pkthdr')
        else:
            if type(data) != bytes:
                raise PcapError('can dump only bytes')
            if header.getcaplen() != len(data):
                raise PcapError('capture length not equal to length of data')
        fields = list(header.getts()) + [header.getcaplen(), header.getlen()]
        self.store.write((struct.pack)(*('IIII', ), *fields))
        self.store.write(data)
        self.store.flush()


class Pkthdr(object):
    __doc__ = '\n    Packet header, as used in the pcap files before each data segment.\n    This class is a simple data wrapper.\n    '

    def __init__(self, ts_sec, ts_usec, incl_len, orig_len):
        self.ts = (
         ts_sec, ts_usec)
        self.incl_len = incl_len
        self.orig_len = orig_len

    def getts(self):
        """ returns a (seconds, microseconds) tuple for the capture time"""
        return self.ts

    def getcaplen(self):
        """ returns the captured length of the packet """
        return self.incl_len

    def getlen(self):
        """ returns the original length of the packet """
        return self.orig_len


class Bpf(object):

    def __init__(self):
        raise NotImplementedError('not implemented yet')

    def filter(self, packet):
        raise NotImplementedError('not implemented yet')