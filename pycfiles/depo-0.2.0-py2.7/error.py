# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/depo/error.py
# Compiled at: 2019-09-29 18:08:01
from __future__ import absolute_import, division, print_function

class DepoError(Exception):

    def __init__(self, message=None, http_body=None):
        super(DepoError, self).__init__(message)
        self.http_body = http_body


class PlaceUnavailableError(DepoError):
    pass


class APIError(DepoError):
    pass


class APIConnectionError(APIError):
    pass