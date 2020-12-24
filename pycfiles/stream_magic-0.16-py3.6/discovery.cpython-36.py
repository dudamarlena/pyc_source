# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/stream_magic/discovery.py
# Compiled at: 2018-06-07 12:16:41
# Size of source mod 2**32: 4130 bytes
"""
DLNA Digital Media Controller implementation for Cambridge Audio
network audio players that are based on their StreamMagic platform.

This module contains the methods to discover a StreamMagic device
on the local network using IP multicast.
"""
__version__ = '0.16'
__author__ = 'Sebastian Kaps (sebk-666)'
import socket

class StreamMagic:
    __doc__ = ' This is the basic StreamMagic class.\n        It provides the means to discover compatible devices on the\n        network (via IP multicast) and retrieve the necessary data\n        needed to instantiate a StreamMagicPDevice object.\n    '
    SSDP_GROUP = ('239.255.255.250', 1900)
    URN_AVTransport = 'urn:schemas-upnp-org:service:AVTransport:1'
    URN_RenderingControl = 'urn:schemas-upnp-org:service:RenderingControl:1'
    SSDP_ALL = 'ssdp:all'
    SOAP_ENCODING = 'http://schemas.xmlsoap.org/soap/encoding/'
    SOAP_ENVELOPE = 'http://schemas.xmlsoap.org/soap/envelope/'
    devices = None

    def __init__(self):
        """ Initialize instance. """
        self.devices = []

    def _send_udp(self, msg):
        """ Send the specified message to the SSDP multicast group. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.settimeout(2)
        sock.sendto(msg, StreamMagic.SSDP_GROUP)
        replies = []
        try:
            while True:
                data, addr = sock.recvfrom(65507)
                replies.append((addr, data))

        except socket.timeout:
            pass

        return replies

    def discover(self, host=None):
        """ Send out an UDP discover message to the SSDP multicast group
            and return a list of StreamMagic devices that replied to it.

            Optional parameters:
            host='IP_addr': if specified, only include the host with the
                            specified ip address in the returned list.

            Returns a list object: [ (addr, data ), ... ] with:

            addr: (str, int) tupel with the ip address and
                    port number of the host, e.g. ('192.168.10.250', 1900)

            data: {'HEADER': 'value'} dict containing the headers
                    of the reply and their values
        """
        msg = b'M-SEARCH * HTTP/1.1\r\nHOST:239.255.255.250:1900\r\nST:upnp:rootdevice\r\nMX:2\r\nMAN:"ssdp:discover"\r\n\r\n'
        discovered_devices = []
        for addr, data in self._send_udp(msg):
            headers = [elem.split(': ') for elem in data.decode('utf-8').splitlines()[1:]]
            data = dict()
            for header in headers:
                if len(header) > 1:
                    key, val = str(header[0]).lower(), header[1]
                else:
                    key, val = str(header[0]).lower(), ''
                data.update({key: val})

            if host:
                if addr[0] == host:
                    if data['server'].startswith('StreamMagic'):
                        self.devices.append((addr, data))
            else:
                if addr not in [dev[0] for dev in discovered_devices] and data['server'].startswith('StreamMagic'):
                    self.devices.append((addr, data))

        if self.devices:
            return self.devices