# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/discordaio/exceptions.py
# Compiled at: 2018-02-25 13:02:06
# Size of source mod 2**32: 529 bytes
import sys

class WebSocketCreationError(Exception):

    def __init__(self):
        print('Error creating a websocket to connect to discord.', file=sys.stderr)


class EventTypeError(Exception):
    pass


class AuthorizationError(Exception):

    def __init__(self):
        print('You requested a api endpoint which you have no authorization', file=sys.stderr)


class UnhandledEndpointStatusError(Exception):
    pass


__all__ = [
 'WebSocketCreationError',
 'EventTypeError',
 'AuthorizationError']