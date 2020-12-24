# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/tests/mockup_net.py
# Compiled at: 2010-02-07 17:28:31
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
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
            return (
             data, len(data))
        return ('', 0)

    def start_udp_connection(self):
        """ Starts a udp connection, returning socket and port. """
        sock = random.randint(0, 80)
        return sock