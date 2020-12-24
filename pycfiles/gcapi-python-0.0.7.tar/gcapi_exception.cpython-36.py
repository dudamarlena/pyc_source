# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\R and L\Dropbox\Coding Notes and Programming\gcapi-python\gcapi\gcapi_exception.py
# Compiled at: 2020-01-14 10:20:45
# Size of source mod 2**32: 675 bytes


class GCapiException(Exception):

    def __init__(self, exception):
        self.exception = exception

    def get_exception(self):
        return self.exception

    def get_error_message(self):
        if self.exception['ErrorMessage']:
            return self.exception['ErrorMessage']

    def get_status_code(self):
        if self.exception['StatusCode']:
            return self.exception['StatusCode']

    def get_additional_info(self):
        if self.exception['AdditionalInfo']:
            return self.exception['AdditionalInfo']

    def get_http_status(self):
        if self.exception['HttpStatus']:
            return self.exception['HttpStatus']

    def get_error_code(self):
        if self.exception['ErrorCode']:
            return self.exception['ErrorCode']