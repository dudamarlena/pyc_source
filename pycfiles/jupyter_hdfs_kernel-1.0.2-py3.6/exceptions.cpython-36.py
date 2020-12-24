# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/exceptions.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 2761 bytes
import traceback
from functools import wraps
from hdfs_kernel.constants import EXPECTED_ERROR_MSG, INTERNAL_ERROR_MSG
from hdfs.util import HdfsError

class SessionManagementException(Exception):
    pass


class CommandNotAllowedException(Exception):
    pass


class CommandExecuteException(Exception):
    pass


class OptionParsingError(RuntimeError):
    pass


class OptionParsingExit(Exception):

    def __init__(self, status, msg):
        self.msg = msg
        self.status = status


EXPECTED_EXCEPTIONS = [
 HdfsError, SessionManagementException, CommandNotAllowedException,
 CommandExecuteException, OptionParsingExit, OptionParsingError]

def handle_expected_exceptions(f):
    """A decorator that handles expected exceptions. Self can be any object with
    an "ipython_display" attribute.
    Usage:
    @handle_expected_exceptions
    def fn(self, ...):
        etc..."""
    exceptions_to_handle = tuple(EXPECTED_EXCEPTIONS)

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        try:
            out = f(self, *args, **kwargs)
        except exceptions_to_handle as err:
            self.send_error(EXPECTED_ERROR_MSG.format(err))
            return
        else:
            return out

    return wrapped


def wrap_unexpected_exceptions(f, execute_if_error=None):
    """A decorator that catches all exceptions from the function f and alerts the user about them.
    Self can be any object with a "logger" attribute and a "ipython_display" attribute.
    All exceptions are logged as "unexpected" exceptions, and a request is made to the user to file an issue
    at the Github repository. If there is an error, returns None if execute_if_error is None, or else
    returns the output of the function execute_if_error.
    Usage:
    @wrap_unexpected_exceptions
    def fn(self, ...):
        ..etc """

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        try:
            out = f(self, *args, **kwargs)
        except Exception as e:
            self.logger.error('ENCOUNTERED AN INTERNAL ERROR: {}\n\tTraceback:\n{}'.format(e, traceback.format_exc()))
            self.send_error(INTERNAL_ERROR_MSG.format(e))
            if execute_if_error is None:
                return
            return execute_if_error()
        else:
            return out

    return wrapped