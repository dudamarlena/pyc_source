# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmq/socket.py
# Compiled at: 2016-08-18 05:25:41
__docformat__ = 'restructuredtext'
import zmq

def zmq_socket(address, socket_type=zmq.REQ, linger=0, protocol='tcp'):
    u"""Get ØMQ socket"""
    context = zmq.Context()
    socket = context.socket(socket_type)
    socket.setsockopt(zmq.LINGER, linger)
    socket.connect(('{0}://{1}').format(protocol, address))
    return socket


def zmq_response(socket, flags=zmq.POLLIN, timeout=10):
    """Get response from given socket"""
    poller = zmq.Poller()
    poller.register(socket, flags)
    if poller.poll(timeout * 1000):
        return socket.recv_json()
    else:
        return [
         503, 'Connection timeout']