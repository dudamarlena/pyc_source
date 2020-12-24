# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssb/rpc/muxrpc.py
# Compiled at: 2019-04-03 13:57:56
# Size of source mod 2**32: 4856 bytes
import logging
logger = logging.getLogger('ssb/rpc/muxrpc')
from functools import wraps
from async_generator import async_generator, yield_
from ssb.rpc.packet_stream import PSMessageType

class MuxRPCAPIException(Exception):
    pass


class MuxRPCHandler(object):

    def check_message(self, msg):
        body = msg.body
        if isinstance(body, dict):
            if 'name' in body:
                if body['name'] == 'Error':
                    raise MuxRPCAPIException(body['message'])


class MuxRPCRequestHandler(MuxRPCHandler):

    def __init__(self, ps_handler):
        self.ps_handler = ps_handler

    def __await__(self):
        msg = yield from self.ps_handler.__await__()
        self.check_message(msg)
        return msg
        if False:
            yield None


class MuxRPCSourceHandler(MuxRPCHandler):

    def __init__(self, ps_handler):
        self.ps_handler = ps_handler

    @async_generator
    async def __aiter__(self):
        async for msg in self.ps_handler:
            try:
                self.check_message(msg)
                await yield_(msg)
            except MuxRPCAPIException:
                raise


class MuxRPCSinkHandlerMixin(object):

    def send(self, msg, msg_type=PSMessageType.JSON, end=False):
        self.connection.send(msg, stream=True, msg_type=msg_type, req=(self.req), end_err=end)


class MuxRPCDuplexHandler(MuxRPCSinkHandlerMixin, MuxRPCSourceHandler):

    def __init__(self, ps_handler, connection, req):
        super(MuxRPCDuplexHandler, self).__init__(ps_handler)
        self.connection = connection
        self.req = req


class MuxRPCSinkHandler(MuxRPCHandler, MuxRPCSinkHandlerMixin):

    def __init__(self, connection, req):
        self.connection = connection
        self.req = req


def _get_appropriate_api_handler(type_, connection, ps_handler, req):
    if type_ in {'async', 'sync'}:
        return MuxRPCRequestHandler(ps_handler)
    if type_ == 'source':
        return MuxRPCSourceHandler(ps_handler)
    if type_ == 'sink':
        return MuxRPCSinkHandler(connection, req)
    if type_ == 'duplex':
        return MuxRPCDuplexHandler(ps_handler, connection, req)


class MuxRPCRequest(object):

    @classmethod
    def from_message(cls, message):
        body = message.body
        return cls('.'.join(body['name']), body['args'])

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return '<MuxRPCRequest {0.name} {0.args}>'.format(self)


class MuxRPCMessage(object):

    @classmethod
    def from_message(cls, message):
        return cls(message.body)

    def __init__(self, body):
        self.body = body

    def __repr__(self):
        return '<MuxRPCMessage {0.body}}>'.format(self)


class MuxRPCAPI(object):

    def __init__(self):
        self.handlers = {}
        self.connection = None

    async def __await__(self):
        async for req_message in self.connection:
            if not req_message is None:
                if req_message.body is None:
                    return
                body = req_message.body
                self.process(self.connection, req_message)

    def add_connection(self, connection, aux=None):
        self.connection = connection
        self.aux = aux

    def define(self, name):

        def _handle(f):
            self.handlers[name] = f

            @wraps(f)
            def _f(*args, **kwargs):
                return f(*args, **kwargs)

            return f

        return _handle

    def process(self, connection, req_message):
        handler = self.handlers.get('.'.join(req_message.body['name']))
        if not handler:
            logger.info(' not handler' + '.'.join(req_message.body['name']))
            return
        handler(connection, req_message, self.aux)

    def call(self, name, args, type_='sync'):
        old_counter = self.connection.req_counter
        ps_handler = self.connection.send({'name':name.split('.'), 
         'args':args, 
         'type':type_},
          stream=(type_ in {'source', 'sink', 'duplex'}))
        return _get_appropriate_api_handler(type_, self.connection, ps_handler, old_counter)