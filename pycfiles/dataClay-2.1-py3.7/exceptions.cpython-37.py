# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/exceptions/exceptions.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 1726 bytes
""" Class description goes here. """
from dataclay.exceptions.ErrorDefs import ErrorCodes
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'

class DataClayException(Exception):
    __doc__ = 'Base class for exceptions in this module.'


class ImproperlyConfigured(DataClayException):
    __doc__ = 'Raised when the settings are not well-formed.'


class IdentifierNotFound(DataClayException):
    __doc__ = 'Raised when a certain identifier (UUID, name...) has not been found.'


class InvalidPythonSignature(DataClayException):
    __doc__ = 'Raised when trying to use a not recognizable Python-signature.'


class RemoteException(RuntimeError):
    __doc__ = 'Exception thrown in client code after a RPC call return with an exception.'

    def __init__(self, error_code, error_string):
        self.error_code = error_code
        self.error_string = error_string
        try:
            self.error_name = ErrorCodes.error_codes[error_code]
        except KeyError:
            self.error_name = 'UNDEFINED'.format(error_code)

        super(RuntimeError, self).__init__('Error [{}: {}]. Server response: {}'.format(self.error_code, self.error_name, self.error_string))


class NetworkError(RuntimeError):
    __doc__ = 'Exception when some socket input/output recv or similar operation\n    does not behave as expected.'

    def __init__(self, *args):
        (super(RuntimeError, self).__init__)(*args)


class ClientError(RuntimeError):
    __doc__ = 'Exception when a client has sent some invalid request.'

    def __init__(self, *args):
        (super(RuntimeError, self).__init__)(*args)