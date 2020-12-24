# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/erlport/erlproto.py
# Compiled at: 2010-02-24 13:18:08
"""Erlang port protocol."""
__author__ = 'Dmitry Vasiliev <dima@hlabs.spb.ru>'
import os, errno
from struct import pack, unpack
from erlport.erlterms import Atom, encode, decode

class Protocol(object):
    """Erlang port protocol."""

    def run(self, port):
        """Run processing loop."""
        while True:
            try:
                message = port.read()
            except EOFError:
                break

            self.handle(port, message)

    def handle(self, port, message):
        """Handle incoming message."""
        if not (isinstance(message, Atom) or isinstance(message, tuple) and len(message) > 0):
            response = (
             Atom('error'), Atom('badarg'))
        else:
            if isinstance(message, Atom):
                name = message
                args = ()
            else:
                name = message[0]
                args = message[1:]
            if not isinstance(name, Atom):
                response = (
                 Atom('error'), Atom('badarg'))
            else:
                handler = getattr(self, 'handle_%s' % name, None)
                if handler is None:
                    response = (
                     Atom('error'), Atom('undef'))
                else:
                    try:
                        response = handler(*args)
                    except TypeError:
                        response = (
                         Atom('error'), Atom('function_clause'))

            port.write(response)
            return


class Port(object):
    """Erlang port."""
    _formats = {1: 'B', 
       2: '>H', 
       4: '>I'}

    def __init__(self, packet=1, use_stdio=False, compressed=False, descriptors=None):
        self._format = self._formats.get(packet)
        if self._format is None:
            raise ValueError('invalid packet size value: %s' % packet)
        self.packet = packet
        self.compressed = compressed
        if descriptors is not None:
            (self.in_d, self.out_d) = descriptors
        elif use_stdio:
            (self.in_d, self.out_d) = (0, 1)
        else:
            (self.in_d, self.out_d) = (3, 4)
        return

    def _read_data(self, length):
        data = ''
        while len(data) != length:
            try:
                buf = os.read(self.in_d, length)
            except IOError, why:
                if why.errno == errno.EPIPE:
                    raise EOFError()
                raise

            if not buf:
                raise EOFError()
            data += buf

        return data

    def read(self):
        """Read incoming message."""
        data = self._read_data(self.packet)
        (length,) = unpack(self._format, data)
        data = self._read_data(length)
        return decode(data)[0]

    def write(self, message):
        """Write outgoing message."""
        data = encode(message, compressed=self.compressed)
        data = pack(self._format, len(data)) + data
        length = len(data)
        if length != 0:
            try:
                n = os.write(self.out_d, data)
            except IOError, why:
                if why.errno == errno.EPIPE:
                    raise EOFError()
                raise
            else:
                if n == 0:
                    raise EOFError()
                length -= n

    def close(self):
        """Close port."""
        os.close(self.in_d)
        os.close(self.out_d)