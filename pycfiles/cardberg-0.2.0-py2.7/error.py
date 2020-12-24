# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cardberg/error.py
# Compiled at: 2019-10-03 03:22:15
from __future__ import absolute_import, division, print_function

class CardbergError(Exception):

    def __init__(self, message=None, http_body=None):
        super(CardbergError, self).__init__(message)
        self.http_body = http_body


class APIError(CardbergError):
    pass


class APIConnectionError(APIError):
    pass