# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/commandlogging.py
# Compiled at: 2016-10-06 14:34:19
"""
Command Logging
"""
import logging
from .debugging import Logging, LoggingFormatter, ModuleLogger
from .comm import PDU, Client, Server
_debug = 0
_log = ModuleLogger(globals())

class CommandLoggingHandler(logging.Handler):

    def __init__(self, commander, addr, loggerName):
        logging.Handler.__init__(self, logging.DEBUG)
        self.setFormatter(LoggingFormatter())
        self.commander = commander
        self.addr = addr
        self.loggerName = loggerName

    def emit(self, record):
        msg = self.format(record) + '\n'
        self.commander.emit(msg, self.addr)


class CommandLogging(Logging):

    def __init__(self):
        if _debug:
            CommandLogging._debug('__init__')
        self.handlers = {}

    def process_command(self, cmd, addr):
        if _debug:
            CommandLogging._debug('process_command %r', cmd, addr)
        if addr not in self.handlers:
            handlers = self.handlers[addr] = {}
        else:
            handlers = self.handlers[addr]
        args = cmd.strip().split()
        logger = None
        if len(args) > 1:
            loggerName = args[1]
            if loggerName in logging.Logger.manager.loggerDict:
                logger = logging.getLogger(loggerName)
        if not args:
            response = '-'
        elif args[0] == '?':
            if len(args) == 1:
                if not handlers:
                    response = 'no handlers'
                else:
                    response = 'handlers: ' + (', ').join(loggerName for loggerName in handlers)
            elif not logger:
                response = 'not a valid logger name'
            elif loggerName in handlers:
                response = 'yes'
            else:
                response = 'no'
        elif args[0] == '+':
            if not logger:
                response = 'not a valid logger name'
            elif loggerName in handlers:
                response = loggerName + ' already has a handler'
            else:
                handler = CommandLoggingHandler(self, addr, loggerName)
                handlers[loggerName] = handler
                logger.addHandler(handler)
                if not addr:
                    response = 'handler to %s added' % (loggerName,)
                else:
                    response = 'handler from %s to %s added' % (addr, loggerName)
        elif args[0] == '-':
            if not logger:
                response = 'not a valid logger name'
            elif loggerName not in handlers:
                response = 'no handler for ' + loggerName
            else:
                handler = handlers[loggerName]
                del handlers[loggerName]
                logger.removeHandler(handler)
                if not addr:
                    response = 'handler to %s removed' % (loggerName,)
                else:
                    response = 'handler from %s to %s removed' % (addr, loggerName)
        else:
            if _debug:
                CommandLogging._warning('bad command %r', cmd)
            response = 'bad command'
        return response + '\n'

    def emit(self, msg, addr):
        if _debug:
            CommandLogging._debug('emit %r %r', msg, addr)
        raise NotImplementedError('emit must be overridden')


class CommandLoggingServer(CommandLogging, Server, Logging):

    def __init__(self):
        if _debug:
            CommandLoggingServer._debug('__init__')
        CommandLogging.__init__(self)

    def indication(self, pdu):
        if _debug:
            CommandLoggingServer._debug('indication %r', pdu)
        addr = pdu.pduSource
        resp = self.process_command(pdu.pduData, addr)
        self.response(PDU(resp, source=addr))

    def emit(self, msg, addr):
        if _debug:
            CommandLoggingServer._debug('emit %r %r', msg, addr)
        self.response(PDU(msg, source=addr))


class CommandLoggingClient(CommandLogging, Client, Logging):

    def __init__(self):
        if _debug:
            CommandLoggingClient._debug('__init__')
        CommandLogging.__init__(self)

    def confirmation(self, pdu):
        if _debug:
            CommandLoggingClient._debug('confirmation %r', pdu)
        addr = pdu.pduSource
        resp = self.process_command(pdu.pduData, addr)
        self.request(PDU(resp, destination=addr))

    def emit(self, msg, addr):
        if _debug:
            CommandLoggingClient._debug('emit %r %r', msg, addr)
        self.request(PDU(msg, destination=addr))