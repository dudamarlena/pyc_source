# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/exceptions/validation_error.py
# Compiled at: 2019-09-29 04:07:46
from jet_bridge_base import status
from jet_bridge_base.exceptions.api import APIException

class ValidationError(APIException):
    default_detail = 'Invalid input'
    default_code = 'invalid'
    default_status_code = status.HTTP_400_BAD_REQUEST