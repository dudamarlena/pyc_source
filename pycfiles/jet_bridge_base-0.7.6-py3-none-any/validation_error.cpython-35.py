# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/exceptions/validation_error.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 250 bytes
from jet_bridge_base import status
from jet_bridge_base.exceptions.api import APIException

class ValidationError(APIException):
    default_detail = 'invalid input'
    default_code = 'invalid'
    default_status_code = status.HTTP_400_BAD_REQUEST