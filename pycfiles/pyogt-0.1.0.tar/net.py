# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/network/net.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import socket
from logging import getLogger
from pyogp.lib.base.message.circuit import Host
logger = getLogger('net.net')

class NetUDPClient(object):
    __module__ = __name__

    def __init__(self):
        self.sender = Host((None, None))
        return

    def get_sender(self):
        return self.sender

    def send_packet(self, sock, send_buffer, host):
        if send_buffer == None:
            raise Exception('No data specified')
        bytes = sock.sendto(send_buffer, (host.ip, host.port))
        return

    def receive_packet(self, sock):
        buf = 10000
        try:
            (data, addr) = sock.recvfrom(buf)
        except:
            return ('', 0)

        self.sender.ip = addr[0]
        self.sender.port = addr[1]
        return (
         data, len(data))

    def start_udp_connection(self):
        """ Starts a udp connection, returning socket and port. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock

    def __repr__(self):
        return self.sender.__repr__