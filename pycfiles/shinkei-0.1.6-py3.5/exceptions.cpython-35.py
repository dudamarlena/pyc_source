# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shinkei/exceptions.py
# Compiled at: 2019-12-14 12:45:46
# Size of source mod 2**32: 1690 bytes


class ShinkeiException(Exception):
    __doc__ = 'Base exception for this library.\n\n    All following exceptions inherit from this.\n    '


class NoMoreItems(ShinkeiException):
    pass


class ShinkeiHTTPException(ShinkeiException):
    __doc__ = 'Generic HTTP exception.\n\n    Attributes\n    ----------\n    request: :class:`aiohttp.ClientResponse`\n        The failed request.\n    code: :class:`int`\n        The request status code.\n    message: :class:`str`\n        A error message.\n    '

    def __init__(self, request, code, message):
        self.request = request
        self.code = code
        self.message = message
        super().__init__(message)


class ShinkeiWSException(ShinkeiException):
    __doc__ = 'Generic WebSocket exception.\n\n    Attributes\n    ----------\n    message: :class:`str`\n        A error message.\n    '

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ShinkeiResumeWS(ShinkeiException):
    __doc__ = 'An internal exception raised when the WebSocket has been disconnected but can resume.\n\n    Attributes\n    ----------\n    message: :class:`str`\n        A error message.\n    '

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ShinkeiWSClosed(ShinkeiException):
    __doc__ = "An internal exception raised when the WebSocket has been disconnected and can't resume.\n\n    Attributes\n    ----------\n    code: :class:`int`\n        The WebSocket status code.\n    message: :class:`str`\n        A error message.\n    "

    def __init__(self, message, code):
        self.code = code
        self.message = message
        super().__init__(message)