# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/plist_service.py
# Compiled at: 2019-03-03 17:07:18
import plistlib, ssl, struct, logging, codecs
from re import sub
from six import PY3
from pymobiledevice.usbmux import usbmux
if PY3:
    plistlib.readPlistFromString = plistlib.loads
    plistlib.writePlistToString = plistlib.dumps

class PlistService(object):

    def __init__(self, port, udid=None, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.port = port
        self.connect(udid)

    def connect(self, udid=None):
        mux = usbmux.USBMux()
        mux.process(1.0)
        dev = None
        while not dev and mux.devices:
            mux.process(1.0)
            if udid:
                for d in mux.devices:
                    if d.serial == udid:
                        dev = d

            else:
                dev = mux.devices[0]
                self.logger.info('Connecting to device: ' + dev.serial)

        try:
            self.s = mux.connect(dev, self.port)
        except:
            raise Exception('Connexion to device port %d failed' % self.port)

        return dev.serial

    def close(self):
        self.s.close()

    def recv(self, length=4096):
        return self.s.recv(length)

    def send(self, data):
        try:
            self.s.send(data)
        except:
            self.logger.error('Sending data to device failled')
            return -1

        return 0

    def sendRequest(self, data):
        res = None
        if self.sendPlist(data) >= 0:
            res = self.recvPlist()
        return res

    def recv_exact(self, l):
        data = ''
        if PY3:
            data = ''
        while l > 0:
            d = self.recv(l)
            if not d or len(d) == 0:
                break
            data += d
            l -= len(d)

        return data

    def recv_raw(self):
        l = self.recv_exact(4)
        if not l or len(l) != 4:
            return
        l = struct.unpack('>L', l)[0]
        return self.recv_exact(l)

    def send_raw(self, data):
        if PY3 and isinstance(data, str):
            data = codecs.encode(data)
        hdr = struct.pack('>L', len(data))
        msg = ('').join([hdr, data])
        return self.send(msg)

    def recvPlist(self):
        payload = self.recv_raw()
        if not payload:
            return
        bplist_header = 'bplist00'
        xml_header = '<?xml'
        if PY3:
            bplist_header = 'bplist00'
            xml_header = '<?xml'
        if payload.startswith(bplist_header):
            if PY3:
                return plistlib.readPlistFromString(payload)
            else:
                from pymobiledevice.util.bplist import BPlistReader
                return BPlistReader(payload).parse()

        else:
            if payload.startswith(xml_header):
                payload = sub('[^\\w<>\\/ \\-_0-9"\'\\=\\.\\?\\!\\+]+', '', payload.decode('utf-8')).encode('utf-8')
                return plistlib.readPlistFromString(payload)
            raise Exception('recvPlist invalid data : %s' % payload[:100].encode('hex'))

    def sendPlist(self, d):
        payload = plistlib.writePlistToString(d)
        l = struct.pack('>L', len(payload))
        return self.send(l + payload)

    def ssl_start(self, keyfile, certfile):
        self.s = ssl.wrap_socket(self.s, keyfile, certfile, ssl_version=ssl.PROTOCOL_TLSv1)