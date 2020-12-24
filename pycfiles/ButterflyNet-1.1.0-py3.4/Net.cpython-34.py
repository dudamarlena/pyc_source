# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bfnet/Net.py
# Compiled at: 2015-11-23 15:02:13
# Size of source mod 2**32: 4396 bytes
import asyncio, logging, types, re
from bfnet import Butterfly

class Net((...).__class__.__class__.__base__):
    __doc__ = '\n    A Net is an object that catches :class:`Butterfly` connections that happen to wander in to your net.\n    '

    def __init__(self, ip: str, port: int, loop: asyncio.AbstractEventLoop=None,
                 server: asyncio.AbstractServer=None):
        """
        Create a new :class:`Net` object.

        This should not be called directly - instead use :func:`bfnet.structures.ButterflyHandler.create_server`
        to create a server.
        :param ip: The IP to bind on.
        :param port: The port to use.
        :param loop: The event loop to use.
        :param server: The asyncio server to use.
        """
        self.loop = loop
        self.port = port
        self.ip = ip
        self.bf_handler = None
        self.server = server
        self.handlers = []
        self.logger = logging.getLogger('ButterflyNet')
        self.logger.info('Net running on {}:{}. Press Ctrl+C to stop.'.format(ip, port))
        print('Net running on {}:{}. Press Ctrl+C to stop.'.format(ip, port))

    def _set_bf_handler(self, handler):
        self.bf_handler = handler

    @asyncio.coroutine
    def stop(self):
        """
        Stops the Net.
        """
        yield from self.server.wait_closed()

    @asyncio.coroutine
    def handle(self, butterfly: Butterfly):
        """
        Default handler.

        This, by default, distributes the incoming data around into handlers.
        After failing these, it will drop down to `default_data` handler.
        :param butterfly: The butterfly to use for handling.
        """
        self.logger.debug('Dropped into default handler for new client')
        while True:
            data = yield from butterfly.read()
            if data is None or data == b'':
                return
            self.logger.debug('Handling data: {}'.format(data))
            for handler in self.handlers:
                matched = handler(data)
                if matched is not None:
                    yield from matched(data, butterfly, self.bf_handler)
                    break
            else:
                self.logger.error('No valid handler')

    def any_data--- This code section failed: ---

 L.  84         0  LOAD_GLOBAL              bytes
                3  LOAD_CONST               ('data',)
                6  LOAD_CLOSURE             'func'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object match>
               15  LOAD_STR                 'Net.any_data.<locals>.match'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'match'

 L.  86        27  LOAD_FAST                'self'
               30  LOAD_ATTR                handlers
               33  LOAD_ATTR                append
               36  LOAD_FAST                'match'
               39  CALL_FUNCTION_1       1  '1 positional, 0 named'
               42  POP_TOP          

 L.  87        43  LOAD_DEREF               'func'
               46  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def regexp_match--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              types
                3  LOAD_ATTR                FunctionType
                6  LOAD_CONST               ('func',)
                9  LOAD_CLOSURE             'regexp'
               12  LOAD_CLOSURE             'self'
               15  BUILD_TUPLE_2         2 
               18  LOAD_CODE                <code_object real_decorator>
               21  LOAD_STR                 'Net.regexp_match.<locals>.real_decorator'
               24  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               30  STORE_FAST               'real_decorator'

 L. 113        33  LOAD_FAST                'real_decorator'
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def prefix_match--- This code section failed: ---

 L. 122         0  LOAD_GLOBAL              types
                3  LOAD_ATTR                FunctionType
                6  LOAD_CONST               ('func',)
                9  LOAD_CLOSURE             'end'
               12  LOAD_CLOSURE             'prefix'
               15  LOAD_CLOSURE             'self'
               18  LOAD_CLOSURE             'start'
               21  BUILD_TUPLE_4         4 
               24  LOAD_CODE                <code_object real_decorator>
               27  LOAD_STR                 'Net.prefix_match.<locals>.real_decorator'
               30  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               36  STORE_FAST               'real_decorator'

 L. 132        39  LOAD_FAST                'real_decorator'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1