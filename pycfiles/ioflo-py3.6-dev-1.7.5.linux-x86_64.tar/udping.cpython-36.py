# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/udp/udping.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 6006 bytes
"""
udp async (nonblocking) io module

"""
from __future__ import absolute_import, division, print_function
import sys, os, socket, errno
from binascii import hexlify
from ...aid.sixing import *
from ...aid.consoling import getConsole
console = getConsole()
UDP_MAX_DATAGRAM_SIZE = 65535
UDP_MAX_SAFE_PAYLOAD = 548
UDP_MAX_PACKET_SIZE = min(1024, UDP_MAX_DATAGRAM_SIZE)

class SocketUdpNb(object):
    __doc__ = '\n    Class to manage non blocking I/O on UDP socket.\n    '

    def __init__(self, ha=None, host='', port=55000, bufsize=1024, wlog=None, bcast=False):
        """
        Initialization method for instance.

        ha = host address duple (host, port)
        host = '' equivalant to any interface on host
        port = socket port
        bs = buffer size
        path = path to log file directory
        wlog = WireLog reference for debug logging or over the wire tx and rx
        bcast = Flag if True enables sending to broadcast addresses on socket
        """
        self.ha = ha or (host, port)
        self.bs = bufsize
        self.wlog = wlog
        self.bcast = bcast
        self.ss = None
        self.opened = False

    def actualBufSizes(self):
        """
        Returns duple of the the actual socket send and receive buffer size
        (send, receive)
        """
        if not self.ss:
            return (0, 0)
        else:
            return (
             self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF),
             self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF))

    def open(self):
        """
        Opens socket in non blocking mode.

        if socket not closed properly, binding socket gets error
           socket.error: (48, 'Address already in use')
        """
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.bcast:
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) < self.bs:
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.bs)
        if self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) < self.bs:
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bs)
        self.ss.setblocking(0)
        try:
            self.ss.bind(self.ha)
        except socket.error as ex:
            console.terse('socket.error = {0}\n'.format(ex))
            return False

        self.ha = self.ss.getsockname()
        self.opened = True
        return True

    def reopen(self):
        """
        Idempotently open socket
        """
        self.close()
        return self.open()

    def close(self):
        """
        Closes  socket and logs if any
        """
        if self.ss:
            self.ss.close()
            self.ss = None
            self.opened = False

    def receive(self):
        """
        Perform non blocking read on  socket.

        returns tuple of form (data, sa)
        if no data then returns (b'',None)
        but always returns a tuple with two elements
        """
        try:
            data, sa = self.ss.recvfrom(self.bs)
        except socket.error as ex:
            if ex.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                return (b'', None)
            emsg = 'socket.error = {0}: receiving at {1}\n'.format(ex, self.ha)
            console.profuse(emsg)
            raise

        if console._verbosity >= console.Wordage.profuse:
            try:
                load = data.decode('UTF-8')
            except UnicodeDecodeError as ex:
                load = '0x{0}'.format(hexlify(data).decode('ASCII'))

            cmsg = 'Server at {0}, received from {1}:\n------------\n{2}\n\n'.format(self.ha, sa, load)
            console.profuse(cmsg)
        if self.wlog:
            self.wlog.writeRx(sa, data)
        return (data, sa)

    def send(self, data, da):
        """
        Perform non blocking send on  socket.

        data is string in python2 and bytes in python3
        da is destination address tuple (destHost, destPort)
        """
        try:
            result = self.ss.sendto(data, da)
        except socket.error as ex:
            emsg = 'socket.error = {0}: sending from {1} to {2}\n'.format(ex, self.ha, da)
            console.profuse(emsg)
            result = 0
            raise

        if console._verbosity >= console.Wordage.profuse:
            try:
                load = data[:result].decode('UTF-8')
            except UnicodeDecodeError as ex:
                load = '0x{0}'.format(hexlify(data[:result]).decode('ASCII'))

            cmsg = 'Server at {0}, sent {1} bytes to {2}:\n------------\n{3}\n\n'.format(self.ha, result, da, load)
            console.profuse(cmsg)
        if self.wlog:
            self.wlog.writeTx(da, data[:result])
        return result


PeerUdp = SocketUdpNb