# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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