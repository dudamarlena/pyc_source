# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rudieshahinian/Projects/rudie/teslajsonpy2/teslajsonpy2/Exceptions.py
# Compiled at: 2018-06-14 15:41:27
# Size of source mod 2**32: 777 bytes


class TeslaException(Exception):

    def __init__(self, code, *args, **kwargs):
        self.message = ''
        (super().__init__)(*args, **kwargs)
        self.code = code
        if self.code == 401:
            self.message = 'UNAUTHORIZED'
        else:
            if self.code == 404:
                self.message = 'NOT_FOUND'
            else:
                if self.code == 405:
                    self.message = 'MOBILE_ACCESS_DISABLED'
                else:
                    if self.code == 423:
                        self.message = 'ACCOUNT_LOCKED'
                    else:
                        if self.code == 429:
                            self.message = 'TOO_MANY_REQUESTS'
                        else:
                            if self.code == 500:
                                self.message = 'SERVER_ERROR'
                            else:
                                if self.code == 503:
                                    self.message = 'SERVICE_MAINTENANCE'
                                elif self.code > 299:
                                    self.message = 'UNKNOWN_ERROR'