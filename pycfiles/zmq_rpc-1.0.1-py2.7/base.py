# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zmq_rpc/base.py
# Compiled at: 2016-12-27 13:29:54
"""zmq-rpc implementation with pyzmq.
This file contains stuff common to both the client and the server.
"""
from zmq_rpc.packer import Packer

class ZmqRpcConnector(object):
    """Base class for zmq-rpc client & server implementations with pyzmq.
    """

    def __init__(self):
        self.packer = Packer()

    def send(self, data):
        """Send data to the connected peer.
        :type data: List.
        """
        return self.socket.send_multipart(data)

    def receive(self):
        """Receive data sent by the connected peer.
        :rtype: List.
        """
        return self.socket.recv_multipart()