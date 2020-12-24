# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libsnmp/role.py
# Compiled at: 2008-10-18 18:59:45
import socket, logging, time
from libsnmp import debug
from libsnmp import rfc1155
from libsnmp import rfc1157
log = logging.getLogger('v1.SNMP')

class manager:

    def __init__(self, dest, interface=('0.0.0.0', 0), socksize=65536):
        self.dest = dest
        self.interface = interface
        self.socket = None
        self.socksize = socksize
        self.request_id = 1
        return

    def __del__(self):
        self.close()

    def get_socket(self):
        return self.socket

    def open(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.interface)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.socksize)
        return self.socket

    def send(self, request, dst=(None, 0)):
        if not self.socket:
            self.open()
        self.socket.sendto(request, dst)

    def read(self):
        if not self.socket:
            raise ValueError('Socket not initialized')
        (message, src) = self.socket.recvfrom(self.socksize)
        return (
         message, src)

    def close(self):
        if self.socket:
            self.socket.close()
        self.socket = None
        return