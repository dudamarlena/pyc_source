# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/console.py
# Compiled at: 2017-05-01 00:38:10
"""
Console Communications
"""
import sys, asyncore
from .debugging import bacpypes_debugging, ModuleLogger
from .core import deferred
from .comm import PDU, Client, Server
_debug = 0
_log = ModuleLogger(globals())
try:
    asyncore.file_dispatcher
except:

    class _barf:

        def __init__(self, *args):
            pass


    asyncore.file_dispatcher = _barf

@bacpypes_debugging
class ConsoleClient(asyncore.file_dispatcher, Client):

    def __init__(self, cid=None):
        if _debug:
            ConsoleClient._debug('__init__ cid=%r', cid)
        asyncore.file_dispatcher.__init__(self, sys.stdin)
        Client.__init__(self, cid)

    def readable(self):
        return True

    def writable(self):
        return False

    def handle_read(self):
        if _debug:
            deferred(ConsoleClient._debug, 'handle_read')
        data = sys.stdin.read().encode('utf-8')
        if _debug:
            deferred(ConsoleClient._debug, '    - data: %r', data)
        deferred(self.request, PDU(data))

    def confirmation(self, pdu):
        if _debug:
            deferred(ConsoleClient._debug, 'confirmation %r', pdu)
        try:
            data = pdu.pduData.decode('utf-8')
            if _debug:
                deferred(ConsoleClient._debug, '    - data: %r', data)
            sys.stdout.write(data)
        except Exception as err:
            ConsoleClient._exception('Confirmation sys.stdout.write exception: %r', err)


@bacpypes_debugging
class ConsoleServer(asyncore.file_dispatcher, Server):

    def __init__(self, sid=None):
        if _debug:
            ConsoleServer._debug('__init__ sid=%r', sid)
        asyncore.file_dispatcher.__init__(self, sys.stdin)
        Server.__init__(self, sid)

    def readable(self):
        return True

    def writable(self):
        return False

    def handle_read(self):
        if _debug:
            deferred(ConsoleServer._debug, 'handle_read')
        data = sys.stdin.read().encode('utf-8')
        if _debug:
            deferred(ConsoleServer._debug, '    - data: %r', data)
        deferred(self.response, PDU(data))

    def indication(self, pdu):
        if _debug:
            deferred(ConsoleServer._debug, 'indication %r', pdu)
        try:
            data = pdu.pduData.decode('utf-8')
            if _debug:
                deferred(ConsoleServer._debug, '    - data: %r', data)
            sys.stdout.write(data)
        except Exception as err:
            ConsoleServer._exception('indication sys.stdout.write exception: %r', err)