# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/network_udp.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2384 bytes
import socket, sys, time, os
from .driver_base import DriverBase
from ..util import log, util
from ..drivers.return_codes import RETURN_CODES

class CMDTYPE:
    SETUP_DATA = 1
    PIXEL_DATA = 2
    BRIGHTNESS = 3


class NetworkUDP(DriverBase):
    __doc__ = 'Driver for communicating with another device on the network via UDP\n\n    To be used with either\n    BiblioPixelAnimations.receivers.GenericNetworkReceiver\n    or :py:class:`.network_receiver.NetworkReceiver`\n\n    Provides the same parameters of :py:class:`.driver_base.DriverBase` as\n    well as those below:\n\n    :param str host: Network hostname or IP address of receiver.\n    :param int port: Network port of receiver\n    :param bool broadcast: If True, broadcast to subnet instead of specific host\n    '

    def __init__(self, num=0, width=0, height=0, host='localhost', broadcast=False, port=3142, broadcast_interface='', **kwds):
        (super().__init__)(num, width, height, **kwds)
        self._host = host
        self._port = port
        self._sock = None
        self._broadcast = broadcast
        self._broadcast_interface = broadcast_interface

    def _generateHeader(self, cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 255)
        packet.append(size >> 8)
        return packet

    def _connect(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            if self._broadcast:
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            return self._sock
        except socket.gaierror:
            error = 'Unable to connect to or resolve host: {}'.format(self._host)
            log.error(error)
            raise IOError(error)

    def _compute_packet(self):
        self._render()
        count = self.bufByteCount()
        self._packet = util.generate_header(CMDTYPE.PIXEL_DATA, count)
        self._packet.extend(self._buf)

    def _send_packet(self):
        try:
            s = self._connect()
            s.sendto(self._packet, (self._host, self._port))
            s.close()
        except Exception as e:
            log.exception(e)
            error = 'Problem communicating with network receiver!'
            log.error(error)
            raise IOError(error)