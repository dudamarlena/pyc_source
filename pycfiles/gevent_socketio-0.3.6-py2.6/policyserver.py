# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socketio/policyserver.py
# Compiled at: 2014-02-03 00:13:04
from gevent.server import StreamServer
import socket
__all__ = ['FlashPolicyServer']

class FlashPolicyServer(StreamServer):
    policyrequest = '<policy-file-request/>'
    policy = '<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">\n<cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>'

    def __init__(self, listener=None, backlog=None):
        if listener is None:
            listener = ('0.0.0.0', 10843)
        StreamServer.__init__(self, listener=listener, backlog=backlog)
        return

    def handle(self, sock, address):
        sock.settimeout(3)
        try:
            input = sock.recv(128)
            if input.startswith(FlashPolicyServer.policyrequest):
                sock.sendall(FlashPolicyServer.policy)
        except socket.timeout:
            pass

        sock.close()