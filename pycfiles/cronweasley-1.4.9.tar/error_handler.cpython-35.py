# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cronutils/error_handler.py
# Compiled at: 2020-01-20 19:53:20
# Size of source mod 2**32: 6007 bytes
__doc__ = '\nThe MIT License (MIT)\n\nCopyright (c) 2014 Zagaran, Inc.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in\nall copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\nTHE SOFTWARE.\n\n@author: Zags (Benjamin Zagorsky)\n'
from sys import stderr
from traceback import format_tb
from bdb import BdbQuit
from raven import Client as SentryClient

class BundledError(Exception):
    pass


class ErrorHandler(object):
    """ErrorHandler"""

    def __init__(self, descriptor=None, data_limit=100):
        self.errors = {}
        self.descriptor = descriptor
        self.data = None
        self.data_limit = data_limit

    def __call__(self, data=None):
        self.data = data
        return self

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        if isinstance(exec_value, KeyboardInterrupt) or isinstance(exec_value, BdbQuit):
            return False
        if isinstance(exec_value, Exception):
            traceback = self.format_traceback_key(exec_value, traceback)
            if traceback in self.errors:
                self.errors[traceback].append(self.data)
        else:
            self.errors[traceback] = [
             self.data]
        return True

    def __repr__(self):
        output = ''
        if self.descriptor:
            output += '*** %s ***\n' % self.descriptor
        for traceback, errors in self.errors.items():
            output += '===============\n'
            output += 'OCCURRED %s TIMES:\n' % len(errors)
            output += traceback
            if any(errors):
                output += '%s\n' % errors[:self.data_limit]
            output += '===============\n'

        return output

    def raise_errors(self):
        output = self.__repr__()
        if self.errors:
            stderr.write(output)
            stderr.write('\n\n')
            raise BundledError()

    @staticmethod
    def format_traceback_key(exec_value, traceback):
        return repr(exec_value) + '\n' + str().join(format_tb(traceback))


class ErrorSentry(ErrorHandler):
    """ErrorSentry"""

    def __init__(self, sentry_dsn, descriptor=None, data_limit=100, sentry_client_kwargs=None, sentry_report_limit=0):
        if sentry_client_kwargs:
            self.sentry_client = SentryClient(dsn=sentry_dsn, **sentry_client_kwargs)
        else:
            self.sentry_client = SentryClient(dsn=sentry_dsn)
        super(ErrorSentry, self).__init__(descriptor=descriptor, data_limit=data_limit)
        self.sentry_report_limit = sentry_report_limit

    def __exit__(self, exec_type, exec_value, traceback):
        ret = super(ErrorSentry, self).__exit__(exec_type, exec_value, traceback)
        if ret and isinstance(exec_value, Exception):
            traceback_key = self.format_traceback_key(exec_value, traceback)
            report_limit_not_exceeded = self.sentry_report_limit < 1 or len(self.errors[traceback_key]) <= self.sentry_report_limit
            if report_limit_not_exceeded:
                self.sentry_client.captureException(exc_info=True)
        return ret


class NullErrorHandler:
    """NullErrorHandler"""

    def __init__(self, *args, **kwargs):
        """ Attach attributes found in ErrorHandler and ErrorSentry, provides correct defaults. """
        self.errors = {}
        self.descriptor = kwargs.get('descriptor', None)
        self.data = None
        self.data_limit = kwargs.get('data_limit', 100)
        self.sentry_report_limit = kwargs.get('sentry_report_limit', 0)

    def __call__(self, data=None):
        return self

    def __enter__(self):
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        return False

    def raise_errors(self):
        pass


null_error_handler = NullErrorHandler()