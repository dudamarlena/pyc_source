# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/errors.py
# Compiled at: 2017-08-29 09:44:06


class UnexpectedPyrplError(Exception):
    """Raise when an unexpected error occurs that should be reported"""
    STARTC = '\x1b[35m'
    ENDC = '\x1b[0m'
    pyrpl_error_message = STARTC + '\n\n\n        An unexpected error occured in PyRPL. Please help us to improve the\n        program by copy-pasting the full error message and optionally some\n        additional information regarding your setup on\n        https://www.github.com/lneuhaus/pyrpl/issues as a new issue. It is\n        possible that we can help you to get rid of the error. If your error\n        is related to improper usage of the PyRPL API, your report will\n        help us improve the documentation. Thanks! ' + ENDC

    def __init__(self, message='', *args):
        self.message = message + self.pyrpl_error_message
        super(UnexpectedPyrplError, self).__init__(self.message, *args)


class ExpectedPyrplError(Exception):
    """Raise when an unexpected error occurs that should be reported"""
    STARTC = '\x1b[35m'
    ENDC = '\x1b[0m'
    pyrpl_error_message = STARTC + '\n\n\n        An expected error occured in PyRPL. Please follow the instructions\n        in this error message and retry! ' + ENDC

    def __init__(self, message='', *args):
        self.message = message + self.pyrpl_error_message
        super(ExpectedPyrplError, self).__init__(self.message, *args)


class NotReadyError(ValueError):
    pass