# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/sockfilter/sockfilter/real.py
# Compiled at: 2014-07-07 21:22:55
__all__ = [
 'restore', 'socket', 'socks', 'socket__socket']
import socket
socket__socket = socket.socket
socks__socksocket = None
try:
    import socks
    socks__socksocket = socks.socksocket
except ImportError:
    socks = None

from .util import apply_attr_and_dict

def restore():
    apply_attr_and_dict(socket, 'socket', socket__socket)
    apply_attr_and_dict(socket, 'SocketType', socket__socket)
    apply_attr_and_dict(socket, '_socketobject', socket__socket)
    apply_attr_and_dict(socks, 'socksocket', socks__socksocket)