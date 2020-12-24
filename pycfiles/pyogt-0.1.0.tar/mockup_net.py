# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/tests/mockup_net.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import socket, random
from pyogp.lib.base.message.circuit import Host

class MockupUDPServer(object):
    __module__ = __name__

    def __init__(self):
        self.rec_buffer = ''
        self.ip = 'MockupUDPServer'
        self.port = 80

    def receive_message(self, client, receive_buffer):
        self.rec_buffer = receive_buffer

    def send_message(self, client, send_message):
        client.rec = send_message
        client.sender = Host((self, self.port))


class MockupUDPClient(object):
    __module__ = __name__

    def __init__(self):
        self.rec = ''
        self.sender = None
        return

    def get_sender(self):
        return self.sender

    def set_response(self, socket, response):
        self.rec[socket] = response

    def send_packet(self, sock, send_buffer, host):
        host.ip.receive_message(self, send_buffer)
        return True

    def receive_packet(self, socket):
        data = self.rec
        self.rec = ''
        if len(data) > 0:
            return (data, len(data))
        return ('', 0)

    def start_udp_connection(self):
        """ Starts a udp connection, returning socket and port. """
        sock = random.randint(0, 80)
        return sock