# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ksoftapi\errors.py
# Compiled at: 2020-04-19 14:32:46
# Size of source mod 2**32: 292 bytes


class NoResults(Exception):
    pass


class Forbidden(Exception):
    pass


class APIError(Exception):

    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message