# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\services\heartbeat.py
# Compiled at: 2010-12-23 17:42:43
"""
A heartbeat server.
"""
from seishub.core.config import IntOption, ListOption, BoolOption
from seishub.core.defaults import HEARTBEAT_CHECK_PERIOD, HEARTBEAT_HUBS, HEARTBEAT_CHECK_TIMEOUT, HEARTBEAT_UDP_PORT, HEARTBEAT_AUTOSTART
from twisted.application import internet, service
from twisted.internet import protocol
import socket, time
__all__ = [
 'HeartbeatService']

class HeartbeatProtocol(protocol.DatagramProtocol):
    """
    Receive UDP heartbeat packets and log them in a dictionary.
    """

    def __init__(self, env):
        self.env = env

    def datagramReceived(self, data, ip_port_tuple):
        ip, _port = ip_port_tuple
        if data == 'SeisHub':
            self.env.config.hubs[ip] = [time.time(), data]


class HeartbeatDetector(internet.TimerService):
    """
    Detect clients not sending heartbeats and removes them from list.
    """

    def __init__(self, env):
        self.env = env
        internet.TimerService.__init__(self, HEARTBEAT_CHECK_PERIOD, self.detect)

    def detect(self):
        """
        Detects clients with heartbeat older than HEARTBEAT_CHECK_TIMEOUT.
        """
        limit = time.time() - HEARTBEAT_CHECK_TIMEOUT
        for node in self.env.config.hubs.items():
            if node[1][0] < limit:
                del self.env.config.hubs[node[0]]

        self.env.log.debug('Active SeisHub nodes: %s' % self.env.config.hubs.items())


class HeartbeatTransmitter(internet.TimerService):
    """
    Sends heartbeat to list of active nodes.
    """

    def __init__(self, env):
        self.env = env
        internet.TimerService.__init__(self, HEARTBEAT_CHECK_PERIOD, self.transmit)

    def transmit(self):
        if len(self.env.config.hubs) == 0:
            ips = self.env.config.getlist('heartbeat', 'default_hubs') or HEARTBEAT_HUBS
        else:
            ips = [ node[0] for node in self.env.config.hubs.items() ]
        for ip in ips:
            self.heartbeat(ip)

    def heartbeat(self, ip):
        try:
            hbsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            hbsocket.sendto('SeisHub', (ip, HEARTBEAT_UDP_PORT))
            self.env.log.debug('Sending heartbeat to ' + ip + ':' + str(HEARTBEAT_UDP_PORT))
        except:
            pass


class HeartbeatReceiver(internet.UDPServer):

    def __init__(self, env):
        self.env = env
        internet.UDPServer.__init__(self, HEARTBEAT_UDP_PORT, HeartbeatProtocol(env))


class HeartbeatService(service.MultiService):
    """
    A asynchronous events-based heartbeat server for SeisHub.
    """
    service_id = 'heartbeat'
    BoolOption('heartbeat', 'autostart', HEARTBEAT_AUTOSTART, 'Enable service on start-up.')
    IntOption('heartbeat', 'port', HEARTBEAT_UDP_PORT, 'Heartbeat port number.')
    ListOption('heartbeat', 'default_hubs', (',').join(HEARTBEAT_HUBS), 'Default IPs for very active SeisHub services.')
    BoolOption('heartbeat', 'active_node', True, 'Heartbeat status')

    def __init__(self, env):
        self.env = env
        service.MultiService.__init__(self)
        self.setName('Heartbeat')
        self.setServiceParent(env.app)
        detector_service = HeartbeatDetector(env)
        detector_service.setName('Heartbeat Detector')
        self.addService(detector_service)
        transmitter_service = HeartbeatTransmitter(env)
        transmitter_service.setName('Heartbeat Transmitter')
        self.addService(transmitter_service)
        receiver_service = HeartbeatReceiver(env)
        receiver_service.setName('Heartbeat Receiver')
        self.addService(receiver_service)

    def privilegedStartService(self):
        if self.env.config.getbool('heartbeat', 'autostart'):
            service.MultiService.privilegedStartService(self)

    def startService(self):
        if self.env.config.getbool('heartbeat', 'autostart'):
            service.MultiService.startService(self)

    def stopService(self):
        if self.running:
            service.MultiService.stopService(self)