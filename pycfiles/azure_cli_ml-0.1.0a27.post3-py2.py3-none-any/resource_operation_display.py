# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\resource_operation_display.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class ResourceOperationDisplay(Model):
    """Display of the operation.

    :param provider: The resource provider name
    :type provider: str
    :param resource: The resource name
    :type resource: str
    :param operation: The operation
    :type operation: str
    :param description: The description of the operation
    :type description: str
    """
    _attribute_map = {'provider': {'key': 'provider', 'type': 'str'}, 'resource': {'key': 'resource', 'type': 'str'}, 'operation': {'key': 'operation', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}}

    def __init__(self, provider=None, resource=None, operation=None, description=None):
        self.provider = provider
        self.resource = resource
        self.operation = operation
        self.description = description