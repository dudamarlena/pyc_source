# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/Projekte/pyparport/pyparport/__init__.py
# Compiled at: 2017-11-28 16:49:13
# Size of source mod 2**32: 853 bytes
import _interface
PortError = _interface.PortError

class Port(object):
    __doc__ = ' Abstraction layer for a more comfortable use '

    def __init__(self, port, addr):
        self.port = port
        self.addr = addr

    def read(self):
        return _interface.read(self.port, self.addr)

    def write(self, value):
        return _interface.write(value, self.port, self.addr)


class PyParport(object):
    __doc__ = ' The main class which implements the interface to the port '

    def __init__(self, base_addres=888):
        self.data_address = base_addres
        self.status_address = base_addres + 1
        self.control_address = base_addres + 2
        self.data = Port('d', self.data_address)
        self.status = Port('s', self.status_address)
        self.control = Port('c', self.control_address)