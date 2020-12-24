# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pcapd.py
# Compiled at: 2019-03-03 17:07:55
from __future__ import print_function
from six import PY3
import struct, time, sys, logging
from pymobiledevice.lockdown import LockdownClient
from tempfile import mkstemp
from optparse import OptionParser
LINKTYPE_ETHERNET = 1
LINKTYPE_RAW = 101

class PcapOut(object):

    def __init__(self, pipename='test.pcap'):
        self.pipe = open(pipename, 'wb')
        self.pipe.write(struct.pack('<LHHLLLL', 2712847316, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET))

    def __del__(self):
        self.pipe.close()

    def writePacket(self, packet):
        t = time.time()
        pkthdr = struct.pack('<LLLL', int(t), int(t * 1000000 % 1000000), len(packet), len(packet))
        data = pkthdr + packet
        l = self.pipe.write(data)
        self.pipe.flush()
        return True


class Win32Pipe(object):

    def __init__(self, pipename='\\\\.\\pipe\\wireshark'):
        self.pipe = win32pipe.CreateNamedPipe(pipename, win32pipe.PIPE_ACCESS_OUTBOUND, win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT, 1, 65536, 65536, 300, None)
        print('Connect wireshark to %s' % pipename)
        win32pipe.ConnectNamedPipe(self.pipe, None)
        win32file.WriteFile(self.pipe, struct.pack('<LHHLLLL', 2712847316, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET))
        return

    def writePacket(self, packet):
        t = time.time()
        pkthdr = struct.pack('<LLLL', int(t), int(t * 1000000 % 1000000), len(packet), len(packet))
        errCode, nBytesWritten = win32file.WriteFile(self.pipe, pkthdr + packet)
        return errCode == 0


if __name__ == '__main__':
    if sys.platform == 'darwin':
        print('Why not use rvictl ?')
    parser = OptionParser(usage='%prog')
    parser.add_option('-u', '--udid', default=False, action='store', dest='device_udid', metavar='DEVICE_UDID', help='Device udid')
    parser.add_option('-o', '--output', dest='output', default=False, help='Output location', type='string')
    options, args = parser.parse_args()
    if sys.platform == 'win32':
        import win32pipe, win32file
        output = Win32Pipe()
    else:
        if options.output:
            path = options.output
        else:
            _, path = mkstemp(prefix='device_dump_', suffix='.pcap', dir='.')
        print('Recording data to: %s' % path)
        output = PcapOut(path)
    logging.basicConfig(level=logging.INFO)
    lockdown = LockdownClient(options.device_udid)
    pcap = lockdown.startService('com.apple.pcapd')
    while True:
        d = pcap.recvPlist()
        if not d:
            break
        if not PY3:
            d = d.data
        hdrsize, xxx, packet_size = struct.unpack('>LBL', d[:9])
        flags1, flags2, offset_to_ip_data, zero = struct.unpack('>LLLL', d[9:25])
        assert hdrsize >= 25
        if PY3:
            interfacetype = d[25:hdrsize].strip('\x00')
        else:
            interfacetype = d[25:hdrsize].strip('\x00')
            interfacetype = "b'" + ('\\x').join(('{:02x}').format(ord(c)) for c in interfacetype) + "'"
        t = time.time()
        print(interfacetype, packet_size, t)
        packet = d[hdrsize:]
        assert packet_size == len(packet)
        if offset_to_ip_data == 0:
            if PY3:
                packet = b'\xbe\xef\xbe\xef\xbe\xef\xbe\xef\xbe\xef\xbe\xef\x08\x00' + packet
            else:
                packet = b'\xbe\xef\xbe\xef\xbe\xef\xbe\xef\xbe\xef\xbe\xef\x08\x00' + packet
        if not output.writePacket(packet):
            break