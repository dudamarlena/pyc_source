# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/hardware/rfid.py
# Compiled at: 2011-06-09 02:34:44
"""
RFID readers which work over serial.
"""
from zope.interface import implements, Interface, Attribute
from twisted.internet import task, serialport, reactor, defer
from twisted.python import log
from sparked.hardware.serialcommand import SerialCommandProtocol
from sparked.hardware.serialport import IProtocolProbe, SerialPortMonitor, SerialProbe
from sparked.events import EventDispatcher
rfidEvents = EventDispatcher()

class TagType:
    UNKNOWN = 'Unknown'
    MIFARE_1K = 'Mifare_1k'
    MIFARE_4K = 'Mifare_4k'
    MIFARE_ULTRALIGHT = 'Mifare_ultralight'


class IRFIDReaderProtocol(Interface):
    events = Attribute("\n        An L{sparked.events.EventDispatcher} object. Implements the\n        following events:\n\n        'tag-present' with kwargs: type=<tag type>, serial=<serial> -\n        every time a tag is polled.\n        ")

    def start():
        """ Start polling/seeking for tags. """
        pass

    def stop():
        """ Stop polling/seeking for tags. """
        pass


class SL031Protocol(SerialCommandProtocol):
    implements(IProtocolProbe, IRFIDReaderProtocol)
    probeRequest = b'\xba\x02\x01\xb9'
    probeResponse = b'\xbd\x03\x01\x01\xbe'
    sndIntro = b'\xba'
    sndOutro = ''
    rcvIntro = b'\xbd'
    rcvOutro = ''
    lengthIncludesChecksum = True
    commands = [
     ('SELECT', 1)]
    pollInterval = 0.2

    def calculateChecksum(self, payload):
        return reduce(lambda a, b: a ^ b, [ ord(c) for c in payload ])

    def got_SELECT(self, data):
        self.logPackage('SELECT', data)
        self.events.dispatch('tag-present', TagType.UNKNOWN, 'DEADBEEF')

    def start(self):
        self._poller = task.LoopingCall(self.sendCommand, 'SELECT')
        self._poller.start(self.pollInterval)

    def stop(self):
        self._poller.stop()


class SonMicroProtocol(SerialCommandProtocol):
    implements(IProtocolProbe, IRFIDReaderProtocol)
    probeRequest = b'\xff\x00\x01\x83\x84'
    probeResponse = b'\xff\x00\x02\x83N\xd3'
    sndIntro = b'\xff\x00'
    sndOutro = ''
    rcvIntro = b'\xff\x00'
    rcvOutro = ''
    lengthIncludesChecksum = False
    commands = [
     ('SELECT', 131),
     ('FIRMWARE', 129)]
    pollInterval = 0.2
    logTraffic = False
    typemap = {1: TagType.MIFARE_ULTRALIGHT, 2: TagType.MIFARE_1K, 
       3: TagType.MIFARE_4K, 
       255: TagType.UNKNOWN}

    def got_FIRMWARE(self, data):
        log.msg('%s - Firmware: %s' % (repr(self), data))

    def got_SELECT(self, data):
        if data == 'N':
            return
        if data == 'U':
            return
        tagtype = self.typemap[ord(data[0])]
        tag = ('').join('%02X' % ord(c) for c in data[1:])
        self.events.dispatch('tag-present', tagtype, tag)

    def start(self):
        self._poller = task.LoopingCall(self.sendCommand, 'SELECT')
        self._poller.start(self.pollInterval)

    def stop(self):
        self._poller.stop()


class HongChangTagProtocol(SerialCommandProtocol):
    implements(IRFIDReaderProtocol)
    sndIntro = '\x02\x00'
    sndOutro = '\x03'
    rcvIntro = '\x02\x00'
    rcvOutro = '\x03'
    lengthIncludesChecksum = False
    checksumIncludesOutro = False
    commands = [
     ('OK', 0),
     ('LED1', 135),
     ('LED2', 136),
     ('MF_GET_SNR', 37)]
    d = None

    def calculateChecksum(self, payload):
        return reduce(lambda a, b: a ^ b, [ ord(c) for c in payload[len(self.sndIntro):] ])

    def sendCommand(self, logical, data=''):
        if self.d is not None:
            warnings.warn('Sending command before response from previous command arrived')
        self.d = defer.Deferred()
        SerialCommandProtocol.sendCommand(self, logical, data)
        return

    def got_OK(self, data):
        d = self.d
        self.d = None
        d.callback(data)
        return


class RFIDReader(object):
    identifier = None
    protocol = None
    reactor = None
    timeout = 0.5

    def __init__(self, identifier, protocol, reactor=None):
        assert IRFIDReaderProtocol.implementedBy(protocol.__class__)
        self.events = EventDispatcher()
        self.events.setEventParent(rfidEvents)
        self.identifier = identifier
        self.protocol = protocol
        self.protocol.events.addObserver('tag-present', self.gotTag)
        self.protocol.events.setEventParent(self.events)
        self.protocol.start()
        self.tags = {}
        if reactor is None:
            from twisted.internet import reactor
        self.reactor = reactor
        return

    def _tagTimeout(self, tpe, tag):
        self.events.dispatch('tag-removed', {'tag': tag, 'type': tpe, 'reader': self.identifier})
        del self.tags[tag]

    def gotTag(self, tpe, tag):
        if tag in self.tags:
            return self.tags[tag].reset(self.timeout)
        self.tags[tag] = self.reactor.callLater(self.timeout, self._tagTimeout, tpe, tag)
        self.events.dispatch('tag-added', {'tag': tag, 'type': tpe, 'reader': self.identifier})

    def __del__(self):
        print 'del'


class RFIDMonitor(SerialPortMonitor):
    """
    A monitor object which tries to instantiate an L{RFIDReader} for each serial port.
    """

    def __init__(self):
        self.readers = {}
        self.candidates = []

    def addCandidate(self, *arg):
        self.candidates.append(arg)

    def deviceAdded(self, info):
        p = info['unique_path']
        reactor.callLater(2, self.probe, p)

    def deviceRemoved(self, info):
        p = info['unique_path']
        if p in self.readers:
            self.readers[p].protocol.stop()
            del self.readers[p]

    def probe(self, device):
        probe = SerialProbe(device)
        for c in self.candidates:
            probe.addCandidate(*c)

        d = probe.start()
        d.addCallbacks(lambda r: self.found(device, r[0], r[1]), log.err)

    def found(self, device, proto, baudrate):
        print 'MATCH >>', proto, baudrate
        port = serialport.SerialPort(proto(), device, reactor, baudrate=baudrate)
        self.readers[device] = RFIDReader(device, port.protocol)