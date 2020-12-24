# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/sockfilter/sockfilter/fake.py
# Compiled at: 2014-07-08 16:06:54
__all__ = [
 'Fake', 'instance']
from . import real
from .address import Address
from .error import SockFilterError
from .util import apply_attr_and_dict
instance = None

class Fake(object):

    def __init__(self, predicate):

        class Socket(object):

            def __init__(self, *args, **kwargs):
                self._real_socket = real.socket__socket(*args, **kwargs)

            def connect(self, address):
                a = Address(*address)
                if not predicate(a):
                    raise SockFilterError(a)
                self._real_socket.connect(address)

            def __getattr__(self, attr):
                return getattr(self._real_socket, attr)

        self.socket = Socket

    def apply(self):
        apply_attr_and_dict(real.socket, 'socket', self.socket)
        apply_attr_and_dict(real.socket, '_socketobject', self.socket)
        apply_attr_and_dict(real.socket, 'SocketType', self.socket)
        apply_attr_and_dict(real.socks, 'socksocket', self.socket)