# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\error_response.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model
from msrest.exceptions import HttpOperationError

class ErrorResponse(Model):
    """Model Management Account error object.

    :param code: error code
    :type code: str
    :param message: Error message
    :type message: str
    :param details: An array of error detail objects.
    :type details: list of :class:`ErrorDetail
     <modelmanagementaccounts.models.ErrorDetail>`
    """
    _validation = {'code': {'required': True}, 'message': {'required': True}}
    _attribute_map = {'code': {'key': 'code', 'type': 'str'}, 'message': {'key': 'message', 'type': 'str'}, 'details': {'key': 'details', 'type': '[ErrorDetail]'}}

    def __init__(self, code, message, details=None):
        self.code = code
        self.message = message
        self.details = details


class ErrorResponseException(HttpOperationError):
    """Server responsed with exception of type: 'ErrorResponse'.

    :param deserialize: A deserializer
    :param response: Server response to be deserialized.
    """

    def __init__(self, deserialize, response, *args):
        super(ErrorResponseException, self).__init__(deserialize, response, 'ErrorResponse', *args)