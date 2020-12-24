# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparked/hardware/serialport.py
# Compiled at: 2011-01-09 06:02:26
"""
Everything serial ports.

Autodetection of plugged in serialport devices and protocol probing.
"""
from zope.interface import Interface, Attribute
import serial
from twisted.python import log
from twisted.internet import protocol, defer, reactor
from twisted.internet.serialport import SerialPort
from sparked.hardware import hal
from sparked import events

class SerialPortMonitor(hal.HardwareMonitor):
    """
    Serial port device monitor.
    """
    subsystem = 'serial'
    uniquePath = '/dev/serial/by-id/'


serialEvents = events.EventDispatcher()

class IProtocolProbe(Interface):
    probeRequest = Attribute('\n        What to send to the serial port on connection.\n        ')
    probeResponse = Attribute('\n        What to receive from the serial port. When this is a string,\n        the serialport is expected to return exactly this.\n\n        If this attribute is callable as a static method, a boolean\n        return value determines whether the probe is successful or\n        not. If None is returned, there is not enough data yet and the\n        function will be called again when data arrives again.\n        ')


class SerialProbeException(Exception):
    pass


class SerialProbe(object):
    """
    Request/response-based serial device fingerprinting. Given a
    serial device, try a series of protocol+baudrate combinations to
    see if they match.
    """

    def __init__(self, device, timeout=0.5):
        self.candidates = []
        self.device = device
        self.timeout = timeout

    def addCandidate(self, proto, baudrate=9600):
        if not IProtocolProbe.implementedBy(proto):
            raise SerialProbeException('%s should implement IProtocolProbe' % proto)
        if baudrate not in serial.baudrate_constants.keys():
            raise SerialProbeException('Invalid baud rate: %d' % baudrate)
        self.candidates.append((proto, baudrate))

    def start(self):
        self.deferred = defer.Deferred()
        if not self.candidates:
            return defer.fail(SerialProbeException('No protocols to probe'))
        self._next()
        return self.deferred

    def _next(self):
        (probe, baudrate) = self.candidates[0]
        del self.candidates[0]
        log.msg('Trying %s @ %d baud' % (probe, baudrate))
        proto = SerialProbeProtocol(probe, timeout=self.timeout)
        SerialPort(proto, self.device, reactor, baudrate=baudrate)
        proto.d.addCallback(self._probeResult, probe, baudrate)

    def _probeResult(self, r, probe, baudrate):
        if r is True:
            self.deferred.callback((probe, baudrate))
            return
        if len(self.candidates):
            self._next()
            return
        self.deferred.errback(SerialProbeException('Probing failed'))


class SerialProbeProtocol(protocol.Protocol):
    """
    Internal protocol which tries if given IProtocolProbe fits the
    current connection.
    """
    timeout = 0.5
    probe = None
    reactor = None

    def __init__(self, probe, timeout=None, reactor=None):
        self.probe = probe
        if timeout is not None:
            self.timeout = timeout
        if not reactor:
            from twisted.internet import reactor
        self.reactor = reactor
        self.d = defer.Deferred()
        return

    def connectionMade(self):
        self.data = ''
        self.transport.write(self.probe.probeRequest)
        self.timer = self.reactor.callLater(self.timeout, self.response, False)

    def dataReceived(self, data):
        self.data += data
        if callable(self.probe.probeResponse):
            retval = self.probe.probeResponse(self.data)
        elif len(self.data) < len(self.probe.probeResponse):
            retval = None
        else:
            retval = self.probe.probeResponse == self.data[:len(self.probe.probeResponse)]
        if retval is None:
            return
        else:
            self.response(retval)
            return

    def response(self, val):
        if self.timer.active():
            self.timer.cancel()
        self.transport.loseConnection()
        self.d.callback(val)