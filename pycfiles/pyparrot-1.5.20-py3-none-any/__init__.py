# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyparport/__init__.py
# Compiled at: 2017-11-28 16:49:13
import _interface
PortError = _interface.PortError

class Port(object):
    """ Abstraction layer for a more comfortable use """

    def __init__(self, port, addr):
        self.port = port
        self.addr = addr

    def read(self):
        return _interface.read(self.port, self.addr)

    def write(self, value):
        return _interface.write(value, self.port, self.addr)


class PyParport(object):
    """ The main class which implements the interface to the port """

    def __init__(self, base_addres=888):
        self.data_address = base_addres
        self.status_address = base_addres + 1
        self.control_address = base_addres + 2
        self.data = Port('d', self.data_address)
        self.status = Port('s', self.status_address)
        self.control = Port('c', self.control_address)