# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/telnet/protocol.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 4884 bytes
__doc__ = '\nParser for the Telnet protocol. (Not a complete implementation of the telnet\nspecification, but sufficient for a command line interface.)\n\nInspired by `Twisted.conch.telnet`.\n'
from __future__ import unicode_literals
import struct
from six import int2byte, binary_type, iterbytes
from .log import logger
__all__ = ('TelnetProtocolParser', )
NOP = int2byte(0)
SGA = int2byte(3)
IAC = int2byte(255)
DO = int2byte(253)
DONT = int2byte(254)
LINEMODE = int2byte(34)
SB = int2byte(250)
WILL = int2byte(251)
WONT = int2byte(252)
MODE = int2byte(1)
SE = int2byte(240)
ECHO = int2byte(1)
NAWS = int2byte(31)
LINEMODE = int2byte(34)
SUPPRESS_GO_AHEAD = int2byte(3)
DM = int2byte(242)
BRK = int2byte(243)
IP = int2byte(244)
AO = int2byte(245)
AYT = int2byte(246)
EC = int2byte(247)
EL = int2byte(248)
GA = int2byte(249)

class TelnetProtocolParser(object):
    """TelnetProtocolParser"""

    def __init__(self, data_received_callback, size_received_callback):
        self.data_received_callback = data_received_callback
        self.size_received_callback = size_received_callback
        self._parser = self._parse_coroutine()
        self._parser.send(None)

    def received_data(self, data):
        self.data_received_callback(data)

    def do_received(self, data):
        """ Received telnet DO command. """
        logger.info('DO %r', data)

    def dont_received(self, data):
        """ Received telnet DONT command. """
        logger.info('DONT %r', data)

    def will_received(self, data):
        """ Received telnet WILL command. """
        logger.info('WILL %r', data)

    def wont_received(self, data):
        """ Received telnet WONT command. """
        logger.info('WONT %r', data)

    def command_received(self, command, data):
        if command == DO:
            self.do_received(data)
        else:
            if command == DONT:
                self.dont_received(data)
            else:
                if command == WILL:
                    self.will_received(data)
                else:
                    if command == WONT:
                        self.wont_received(data)
                    else:
                        logger.info('command received %r %r', command, data)

    def naws(self, data):
        """
        Received NAWS. (Window dimensions.)
        """
        if len(data) == 4:
            columns, rows = struct.unpack(str('!HH'), data)
            self.size_received_callback(rows, columns)
        else:
            logger.warning('Wrong number of NAWS bytes')

    def negotiate(self, data):
        """
        Got negotiate data.
        """
        command, payload = data[0:1], data[1:]
        if not isinstance(command, bytes):
            raise AssertionError
        else:
            if command == NAWS:
                self.naws(payload)
            else:
                logger.info('Negotiate (%r got bytes)', len(data))

    def _parse_coroutine(self):
        """
        Parser state machine.
        Every 'yield' expression returns the next byte.
        """
        while 1:
            d = yield
            if d == int2byte(0):
                pass
            else:
                if d == IAC:
                    d2 = yield
                    if d2 == IAC:
                        self.received_data(d2)
                    else:
                        if d2 in (NOP, DM, BRK, IP, AO, AYT, EC, EL, GA):
                            self.command_received(d2, None)
                        else:
                            if d2 in (DO, DONT, WILL, WONT):
                                d3 = yield
                                self.command_received(d2, d3)
                            elif d2 == SB:
                                data = []
                                while True:
                                    d3 = yield
                                    if d3 == IAC:
                                        d4 = yield
                                        if d4 == SE:
                                            break
                                        else:
                                            data.append(d4)
                                    else:
                                        data.append(d3)

                                self.negotiate(''.join(data))
                else:
                    self.received_data(d)

    def feed(self, data):
        """
        Feed data to the parser.
        """
        assert isinstance(data, binary_type)
        for b in iterbytes(data):
            self._parser.send(int2byte(b))