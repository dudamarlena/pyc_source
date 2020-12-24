# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuiows/exc.py
# Compiled at: 2016-12-22 09:51:49
# Size of source mod 2**32: 379 bytes


class WebsocketError(Exception):
    __doc__ = '\n    The base class for all websocket exceptions.\n    '


class WebsocketClosedError(WebsocketError):
    __doc__ = '\n    Raised when a connection is closed.\n\n    :ivar code: The close code.\n    :ivar reason: The reason for the close.\n    '

    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason