# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\client.py
# Compiled at: 2017-03-03 18:58:43
# Size of source mod 2**32: 5647 bytes
"""
A small simple port of aioyoyo to use asyncio instead of its original
threading client. Creating an IRCClient instance will create the protocol
instance.

To start the connection run IRCClient.connect(); (coroutine)
"""
import logging
from .oyoyo.parse import *
from .protocol import ClientProtocol
from aioyoyo.oyoyo.cmdhandler import IRCClientError

class IRCClient(object):

    def __init__(self, loop, address=None, port=None, protocol=ClientProtocol):
        """
        A basic Async IRC client. Use coroutine IRCClient.connect to initiate
        the connection. Takes the event loop, a host (address, port) and if
        wanted an alternate protocol can be defined. By default will use the
        ClientProtocol class, which just uses the IRCClient's tracebacks and
        passes received data to the client.
        """
        self.loop = loop
        self.host = (address, port)
        self.address = address
        self.port = port
        self.protocol = protocol(self)
        self.logger = logging.getLogger('aioyoyo')
        self.logger.setLevel(logging.INFO)

    async def connect(self):
        """Initiate the connection, creates a connection using the defined
        protocol"""
        await self.loop.create_connection(lambda : self.protocol, self.address, self.port)

    async def connection_made(self):
        """Called on a successful connection, by default forwarded by
        protocol.connection_made"""
        logging.info('connecting to %s:%s' % self.host)

    async def data_received(self, data):
        """Called when data is received by the connection, by default
        forwarded by protocol.data_received, passes bytes not str"""
        logging.info('received: %s' % data.decode())

    async def connection_lost(self, exc):
        """Called when the connection is dropped, by default prints
        the exception if there is one. Forwarded by protocol.connection_lost"""
        logging.info('connection lost: %s' % exc)

    async def send(self, *args):
        """Send a message to the connected server. all arguments are joined
        with a space for convenience, for example the following are identical

        >>> cli.send("JOIN %s" % some_room)
        >>> cli.send("JOIN", some_room)

        In python 3, all args must be of type str or bytes, *BUT* if they are
        str they will be converted to bytes with the encoding specified by the
        'encoding' keyword argument (default 'utf8').
        """
        bargs = []
        for arg in args:
            if isinstance(arg, str):
                bargs.append(arg.encode())
            else:
                if isinstance(arg, bytes):
                    bargs.append(arg)
                else:
                    raise IRCClientError('Refusing to send one of the args from provided: %s' % repr([(type(arg), arg) for arg in args]))

        msg = (b' ').join(bargs)
        await self.protocol.send_raw(msg + b'\r\n')
        logging.info('---> send "%s"' % msg)

    async def send_msg(self, message):
        """Send a str to the server from absolute raw, none of the formatting
        from IRCClient.send"""
        await self.protocol.send(message)

    async def send_raw(self, data):
        """Send raw bytes to the server, none of the formatting from IRCClient.send"""
        await self.protocol.send_raw(data)

    async def close(self):
        """Close the connection"""
        logging.info('close transport')
        self.protocol.transport.close()


class CommandClient(IRCClient):
    __doc__ = 'IRCClient, using a command handler'

    def __init__(self, loop, cmd_handler, address=None, port=None, protocol=ClientProtocol, **kwargs):
        """Takes a command handler (see oyoyo.cmdhandler.CommandHandler)
        whose attributes are the commands you want callable, for example
        with a privmsg cmdhandler.privmsg will be awaited with the
        appropriate *args, decorate methods with @protected to make it
        uncallable as a command"""
        (IRCClient.__init__)(self, loop, address=address, port=port, protocol=protocol, **kwargs)
        self.command_handler = cmd_handler(self)

    async def data_received(self, data):
        """On IRCClient.data_received parse for a command and pass to the
        command_handler to run()"""
        prefix, command, args = parse_raw_irc_command(data)
        await (self.command_handler.run)(command, prefix, *args)