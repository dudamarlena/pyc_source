# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\available_operations.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class AvailableOperations(Model):
    """Available operation list.

    :param value: An array of available operations
    :type value: list of :class:`ResourceOperation
     <modelmanagementaccounts.models.ResourceOperation>`
    """
    _attribute_map = {'value': {'key': 'value', 'type': '[ResourceOperation]'}}

    def __init__(self, value=None):
        self.value = value