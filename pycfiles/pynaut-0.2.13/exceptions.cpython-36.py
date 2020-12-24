# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynats2/exceptions.py
# Compiled at: 2019-10-24 22:18:34
# Size of source mod 2**32: 1591 bytes
__all__ = ('NATSConnectionError', 'NATSError', 'NATSInvalidResponse', 'NATSInvalidSchemeError',
           'NATSInvalidUrlError', 'NATSTCPConnectionRequiredError', 'NATSTLSConnectionRequiredError',
           'NATSUnexpectedResponse', 'NATSRequestTimeoutError')

class NATSError(Exception):
    pass


class NATSUnexpectedResponse(NATSError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        super().__init__()


class NATSInvalidResponse(NATSError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        super().__init__()


class NATSConnectionError(NATSError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        super().__init__()


class NATSTCPConnectionRequiredError(NATSConnectionError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        (super().__init__)(line, *args, **kwargs)


class NATSTLSConnectionRequiredError(NATSConnectionError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        (super().__init__)(line, *args, **kwargs)


class NATSInvalidUrlError(NATSConnectionError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        (super().__init__)(line, *args, **kwargs)


class NATSInvalidSchemeError(NATSConnectionError):

    def __init__(self, line, *args, **kwargs):
        self.line = line
        (super().__init__)(line, *args, **kwargs)


class NATSRequestTimeoutError(NATSError):
    pass