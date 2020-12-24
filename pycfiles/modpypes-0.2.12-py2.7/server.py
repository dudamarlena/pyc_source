# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modpypes/server.py
# Compiled at: 2017-08-10 22:45:32
"""
This executable module is a console application for presenting itself as a
MODBUS server accepting read and write MODBUS PDUs.
"""
import os, logging
from bacpypes.debugging import bacpypes_debugging, ModuleLogger
from bacpypes.consolecmd import ConsoleCmd
from bacpypes.consolelogging import ArgumentParser
from bacpypes.comm import Client, bind
from bacpypes.core import run
from .pdu import ExceptionResponse, ReadCoilsResponse, ReadDiscreteInputsResponse, ReadMultipleRegistersResponse, WriteSingleCoilResponse, WriteSingleRegisterResponse, WriteMultipleRegistersResponse
from .app import ModbusServer, ModbusException
_debug = 0
_log = ModuleLogger(globals())
_commlog = logging.getLogger(__name__ + '._commlog')
SERVER_HOST = os.getenv('SERVER_HOST', '')
SERVER_PORT = int(os.getenv('SERVER_PORT', 502))
IDLE_TIMEOUT = int(os.getenv('IDLE_TIMEOUT', 0)) or None

@bacpypes_debugging
class SimpleServer(Client):
    """
    Simple Server
    """

    def __init__(self, unitNumber=1):
        if _debug:
            SimpleServer._debug('__init__')
        Client.__init__(self)
        self.unitNumber = unitNumber
        self.coils = [
         False] * 10
        self.registers = [0] * 10

    def confirmation(self, req):
        """Got a request from a client."""
        if _debug:
            SimpleServer._debug('confirmation %r', req)
        _commlog.debug('>>> %r %r', req.pduSource, req)
        if isinstance(req, Exception):
            if _debug:
                SimpleServer._debug('    - punt exceptions')
            return
        if req.mpduUnitID != self.unitNumber:
            if _debug:
                SimpleServer._debug('    - not for us')
            return
        try:
            try:
                fn = getattr(self, 'do_' + req.__class__.__name__)
            except AttributeError:
                raise ModbusException(ExceptionResponse.ILLEGAL_FUNCTION)

            resp = fn(req)
        except ModbusException as err:
            resp = ExceptionResponse(req.mpduFunctionCode, err.errCode)

        resp.pduDestination = req.pduSource
        resp.mpduTransactionID = req.mpduTransactionID
        resp.mpduUnitID = req.mpduUnitID
        _commlog.debug('<<< %r %r', resp.pduDestination, resp)
        self.request(resp)

    def pull_coils(self, address, count):
        """Called when there is a request for the current value of a coil."""
        if _debug:
            SimpleServer._debug('pull_coils %r %r', address, count)

    def push_coils(self, address, count):
        """Called when a MODBUS service has changed the value of one or more coils."""
        if _debug:
            SimpleServer._debug('push_coils %r %r', address, count)

    def pull_registers(self, address, count):
        """Called when a MODBUS client is requesting the current value of one
        or more registers."""
        if _debug:
            SimpleServer._debug('pull_registers %r %r', address, count)

    def push_registers(self, address, count):
        """Called when a MODBUS service has changed the value of one or more
        registers."""
        if _debug:
            SimpleServer._debug('push_registers %r %r', address, count)

    def do_ReadCoilsRequest(self, req):
        SimpleServer._debug('do_ReadCoilsRequest %r', req)
        if req.address + req.count > len(self.coils):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        self.pull_coils(req.address, req.count)
        return ReadCoilsResponse(self.coils[req.address:req.address + req.count])

    def do_WriteSingleCoilRequest(self, req):
        SimpleServer._debug('do_WriteSingleCoilRequest %r', req)
        if req.address > len(self.coils):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        if req.value == 0:
            self.coils[req.address] = 0
        elif req.value == 65280:
            self.coils[req.address] = 1
        else:
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_VALUE)
        self.push_coils(req.address, 1)
        return WriteSingleCoilResponse(req.address, req.value)

    def do_ReadDescreteInputsRequest(self, req):
        SimpleServer._debug('do_ReadDescreteInputsRequest %r', req)
        if req.address + req.count > len(self.coils):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        self.pull_coils(req.address, req.count)
        return ReadDiscreteInputsResponse(self.coils[req.address:req.address + req.count])

    def do_ReadMultipleRegistersRequest(self, req):
        SimpleServer._debug('do_ReadMultipleRegistersRequest %r', req)
        if req.address + req.count > len(self.registers):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        self.pull_registers(req.address, req.count)
        return ReadMultipleRegistersResponse(self.registers[req.address:req.address + req.count])

    def do_WriteSingleRegisterRequest(self, req):
        SimpleServer._debug('do_WriteSingleRegisterRequest %r', req)
        if req.address > len(self.registers):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        self.registers[req.address] = req.value
        self.push_registers(req.address, 1)
        return WriteSingleRegisterResponse(req.address, req.value)

    def do_WriteMultipleRegistersRequest(self, req):
        SimpleServer._debug('do_WriteMultipleRegistersRequest %r', req)
        if req.address + req.count > len(self.registers):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        for i in range(req.count):
            self.registers[req.address + i] = req.registers[i]

        self.push_registers(req.address, req.count)
        return WriteMultipleRegistersResponse(req.address, req.count)

    def do_ReadInputRegistersRequest(self, req):
        SimpleServer._debug('do_ReadInputRegistersRequest %r', req)
        if req.address + req.count > len(self.registers):
            raise ModbusException(ExceptionResponse.ILLEGAL_DATA_ADDRESS)
        self.pull_registers(req.address, req.count)
        return ReadMultipleRegistersResponse(self.registers[req.address:req.address + req.count])


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--host', type=str, help=('address of host (default {!r})').format(SERVER_HOST), default=SERVER_HOST)
    parser.add_argument('--port', type=int, help=('server port (default {!r})').format(SERVER_PORT), default=SERVER_PORT)
    parser.add_argument('--idle-timeout', nargs='?', type=int, help='idle connection timeout', default=IDLE_TIMEOUT)
    args = parser.parse_args()
    if _debug:
        _log.debug('initialization')
    if _debug:
        _log.debug('    - args: %r', args)
    bind(SimpleServer(), ModbusServer(port=args.port, idle_timeout=args.idle_timeout))
    _log.debug('running')
    run()
    _log.debug('fini')


if __name__ == '__main__':
    main()