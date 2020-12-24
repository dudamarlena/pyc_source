# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\resource_operation.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class ResourceOperation(Model):
    """Resource operation.

    :param name: Name of this operation.
    :type name: str
    :param display: Display of the operation
    :type display: :class:`ResourceOperationDisplay
     <modelmanagementaccounts.models.ResourceOperationDisplay>`
    :param origin: The operation origin
    :type origin: str
    """
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'display': {'key': 'display', 'type': 'ResourceOperationDisplay'}, 'origin': {'key': 'origin', 'type': 'str'}}

    def __init__(self, name=None, display=None, origin=None):
        self.name = name
        self.display = display
        self.origin = origin