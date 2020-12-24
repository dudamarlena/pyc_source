# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/exceptions/missing_argument_error.py
# Compiled at: 2019-10-06 09:50:32
from jet_bridge_base import status
from jet_bridge_base.exceptions.api import APIException

class MissingArgumentError(APIException):
    default_detail = 'Invalid input'
    default_code = 'invalid'
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(detail='Missing argument %s' % arg_name)
        self.arg_name = arg_name