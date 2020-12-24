# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/uxd/uxding.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 6011 bytes
"""
uxd async io (nonblocking) module

"""
from __future__ import absolute_import, division, print_function
import sys, os, socket, errno
from binascii import hexlify
from ...aid.sixing import *
from ...aid.consoling import getConsole
console = getConsole()

class SocketUxdNb(object):
    __doc__ = '\n    Class to manage non blocking io on UXD (unix domain) socket.\n    Use instance method .close() to close socket\n    '

    def __init__(self, ha=None, umask=None, bufsize=1024, wlog=None):
        """
        Initialization method for instance.

        ha = uxd file name
        umask = umask for uxd file
        bufsize = buffer size
        """
        self.ha = ha
        self.umask = umask
        self.bs = bufsize
        self.wlog = wlog
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
        self.ss = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) < self.bs:
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.bs)
        if self.ss.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF) < self.bs:
            self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bs)
        self.ss.setblocking(0)
        oldumask = None
        if self.umask is not None:
            oldumask = os.umask(self.umask)
        try:
            self.ss.bind(self.ha)
        except socket.error as ex:
            if not ex.errno == errno.ENOENT:
                console.terse('socket.error = {0}\n'.format(ex))
                return False
            try:
                os.makedirs(os.path.dirname(self.ha))
            except OSError as ex:
                console.terse('OSError = {0}\n'.format(ex))
                return False

            try:
                self.ss.bind(self.ha)
            except socket.error as ex:
                console.terse('socket.error = {0}\n'.format(ex))
                return False

        if oldumask is not None:
            os.umask(oldumask)
        self.ha = self.ss.getsockname()
        self.opened = True
        return True

    def reopen(self):
        """
        Idempotently open socket by closing first if need be
        """
        self.close()
        return self.open()

    def close(self):
        """
        Closes  socket.
        """
        if self.ss:
            self.ss.close()
            self.ss = None
            self.opened = False
        try:
            os.unlink(self.ha)
        except OSError:
            if os.path.exists(self.ha):
                raise

    def receive(self):
        """
        Perform non blocking receive on  socket.
        Returns tuple of form (data, sa)
        If no data then returns ('',None)
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
        """Perform non blocking send on  socket.

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
            self.wlog.writeTx(da, data)
        return result


PeerUxd = SocketUxdNb