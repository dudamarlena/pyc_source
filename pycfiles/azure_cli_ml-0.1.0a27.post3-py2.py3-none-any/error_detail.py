# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\error_detail.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class ErrorDetail(Model):
    """Model Management Account error detail.

    :param code: error code
    :type code: str
    :param message: error message
    :type message: str
    """
    _validation = {'code': {'required': True}, 'message': {'required': True}}
    _attribute_map = {'code': {'key': 'code', 'type': 'str'}, 'message': {'key': 'message', 'type': 'str'}}

    def __init__(self, code, message):
        self.code = code
        self.message = message