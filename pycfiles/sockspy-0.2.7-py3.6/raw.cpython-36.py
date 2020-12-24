# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sockspy/socket/raw.py
# Compiled at: 2017-07-20 12:45:53
# Size of source mod 2**32: 595 bytes
import socket

def server_socket(address, backlog=5):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(backlog)
    server.setblocking(False)
    return server


def client_socket(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    in_blocking = False
    try:
        sock.connect(address)
    except BlockingIOError:
        in_blocking = True

    return (
     sock, in_blocking)