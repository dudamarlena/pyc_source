# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modpypes/client.py
# Compiled at: 2017-04-28 15:47:42
"""
Client
======

This executable module is a console application for generating
read and write MODBUS PDUs.
"""
import os, math
from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolecmd import ConsoleCmd
from bacpypes.consolelogging import ArgumentParser
from bacpypes.core import run, deferred
from bacpypes.iocb import IOCB
from .pdu import ExceptionResponse, ReadCoilsRequest, ReadCoilsResponse, ReadDiscreteInputsRequest, ReadDiscreteInputsResponse, ReadInputRegistersRequest, ReadInputRegistersResponse, ReadMultipleRegistersRequest, ReadMultipleRegistersResponse, WriteSingleCoilRequest, WriteSingleCoilResponse, WriteSingleRegisterRequest, WriteSingleRegisterResponse, ModbusStruct
from .app import ModbusClientController
_debug = 0
_log = ModuleLogger(globals())
CONNECT_TIMEOUT = int(os.getenv('CONNECT_TIMEOUT', 0)) or None
IDLE_TIMEOUT = int(os.getenv('IDLE_TIMEOUT', 0)) or None

@bacpypes_debugging
class ConsoleClient(ConsoleCmd):
    """
    Console Client
    """

    def __init__(self, controller):
        if _debug:
            ConsoleClient._debug('__init__ %r', controller)
        ConsoleCmd.__init__(self)
        self.controller = controller

    def do_read(self, args):
        """read <addr> <unitID> <register> [ <count> ]

        :param addr: IP address of the MODBUS/TCP device or gateway
        :param unitID: unit identifier
        :param register: register in 5-digit or 6-digit format
        :param count: number of registers to read, defaults to one

        This command generates a :class:`ReadCoilsRequest`,
        :class:`ReadDiscreteInputsRequest`, :class:`ReadInputRegistersRequest`,
        or :class:`ReadMultipleRegistersRequest` depending on the address
        prefix; 0, 1, 3, or 4.
        """
        args = args.split()
        if _debug:
            ConsoleClient._debug('do_read %r', args)
        if len(args) < 3:
            print 'address, unit and register required'
            return
        addr, unitID, register = args[:3]
        if ':' in addr:
            addr, port = addr.split(':')
            server_address = (addr, int(port))
        else:
            server_address = (
             addr, 502)
        unitID = int(unitID)
        if _debug:
            ConsoleClient._debug('    - addr, unitID: %r, %r', addr, unitID)
        register = int(register)
        if len(args) == 4:
            rcount = int(args[3])
        else:
            rcount = 1
        if _debug:
            ConsoleClient._debug('    - register, rcount: %r, %r', register, rcount)
        digits = int(math.log10(register)) + 1
        if digits <= 4:
            registerType = 0
        else:
            if digits == 5:
                registerType = register // 10000
                register = register % 10000
            elif digits == 6:
                registerType = register // 100000
                register = register % 100000
            else:
                print '5 or 6 digit addresses please'
                return
            if _debug:
                ConsoleClient._debug('    - registerType, register: %r, %r', registerType, register)
            if registerType == 0:
                req = ReadCoilsRequest(register - 1, rcount)
            elif registerType == 1:
                req = ReadDiscreteInputsRequest(register - 1, rcount)
            elif registerType == 3:
                req = ReadInputRegistersRequest(register - 1, rcount)
            elif registerType == 4:
                req = ReadMultipleRegistersRequest(register - 1, rcount)
            else:
                print 'unsupported register type'
                return
            req.pduDestination = server_address
            req.mpduUnitID = unitID
            if _debug:
                ConsoleClient._debug('    - req: %r', req)
            iocb = IOCB(req)
            if _debug:
                ConsoleClient._debug('    - iocb: %r', iocb)
            deferred(self.controller.request_io, iocb)
            iocb.wait()
            if iocb.ioError:
                print 'error: %r' % (iocb.ioError,)
                return
        resp = iocb.ioResponse
        if _debug:
            ConsoleClient._debug('    - resp: %r', resp)
        if isinstance(resp, ExceptionResponse):
            print '  ::= ' + str(resp)
        elif isinstance(resp, ReadCoilsResponse):
            print '  ::= ' + str(resp.bits)
        elif isinstance(resp, ReadDiscreteInputsResponse):
            print '  ::= ' + str(resp.bits)
        elif isinstance(resp, ReadInputRegistersResponse):
            print '  ::= ' + str(resp.registers)
            for dtype, codec in ModbusStruct.items():
                try:
                    value = codec.unpack(resp.registers)
                    print '   ' + dtype + ' ::= ' + str(value)
                except Exception as err:
                    if _debug:
                        ConsoleClient._debug('unpack exception %r: %r', codec, err)

        elif isinstance(resp, ReadMultipleRegistersResponse):
            print '  ::= ' + str(resp.registers)
            for dtype, codec in ModbusStruct.items():
                try:
                    value = codec.unpack(resp.registers)
                    print '   ' + dtype + ' ::= ' + str(value)
                except Exception as err:
                    if _debug:
                        ConsoleClient._debug('unpack exception %r: %r', codec, err)

        else:
            raise TypeError('unsupported response')

    def do_write(self, args):
        """write <addr> <unitID> <register> <value>

        :param addr: IP address of the MODBUS/TCP device or gateway
        :param unitID: unit identifier
        :param register: register in 5-digit or 6-digit format
        :param value: value to write

        This command generates a :class:`WriteSingleCoil`,
        or :class:`WriteSingleRegisterRequest` depending on the address
        prefix; 0 or 4.
        """
        args = args.split()
        if _debug:
            ConsoleClient._debug('do_write %r', args)
        if len(args) < 3:
            print 'address, unit and register required'
            return
        addr, unitID, register, value = args
        if ':' in addr:
            addr, port = addr.split(':')
            server_address = (addr, int(port))
        else:
            server_address = (
             addr, 502)
        unitID = int(unitID)
        if _debug:
            ConsoleClient._debug('    - addr, unitID: %r, %r', server_address, unitID)
        register = int(register)
        if _debug:
            ConsoleClient._debug('    - register: %r', register)
        digits = int(math.log10(register)) + 1
        if digits <= 4:
            registerType = 0
        else:
            if digits == 5:
                registerType = register // 10000
                register = register % 10000
            elif digits == 6:
                registerType = register // 100000
                register = register % 100000
            else:
                print '5 or 6 digit addresses please'
                return
            if _debug:
                ConsoleClient._debug('    - registerType, register: %r, %r', registerType, register)
            value = int(value)
            if _debug:
                ConsoleClient._debug('    - value: %r', value)
            if registerType == 0:
                req = WriteSingleCoilRequest(register - 1, value)
            elif registerType == 4:
                req = WriteSingleRegisterRequest(register - 1, value)
            else:
                print 'unsupported register type'
                return
            req.pduDestination = server_address
            req.mpduUnitID = unitID
            if _debug:
                ConsoleClient._debug('    - req: %r', req)
            iocb = IOCB(req)
            if _debug:
                ConsoleClient._debug('    - iocb: %r', iocb)
            deferred(self.controller.request_io, iocb)
            iocb.wait()
            if iocb.ioError:
                print 'error: %r' % (iocb.ioError,)
                return
        resp = iocb.ioResponse
        if _debug:
            ConsoleClient._debug('    - resp: %r', resp)
        if isinstance(iocb.ioResponse, WriteSingleCoilResponse):
            print '  ::= ' + str(iocb.ioResponse.value)
        elif isinstance(iocb.ioResponse, WriteSingleRegisterResponse):
            print '  ::= ' + str(iocb.ioResponse.value)
        else:
            raise TypeError('unsupported response')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--connect-timeout', nargs='?', type=int, help='idle connection timeout', default=CONNECT_TIMEOUT)
    parser.add_argument('--idle-timeout', nargs='?', type=int, help='idle connection timeout', default=IDLE_TIMEOUT)
    args = parser.parse_args()
    if _debug:
        _log.debug('initialization')
    if _debug:
        _log.debug('    - args: %r', args)
    this_controller = ModbusClientController(connect_timeout=args.connect_timeout, idle_timeout=args.idle_timeout)
    if _debug:
        _log.debug('    - this_controller: %r', this_controller)
    this_console = ConsoleClient(this_controller)
    if _debug:
        _log.debug('    - this_console: %r', this_console)
    _log.debug('running')
    run()
    _log.debug('fini')


if __name__ == '__main__':
    main()