# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\sku.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class Sku(Model):
    """The SKU of the Model Management Account account.

    :param name: Gets or sets the sku name. Required for account creation,
     optional for update. Possible values include: 'S1', 'S2', 'S3', 'DevTest'
    :type name: str or :class:`SkuName
     <modelmanagementaccounts.models.SkuName>`
    :param capacity: Gets or sets the capacity of current SKU.
    :type capacity: int
    """
    _validation = {'name': {'required': True}, 'capacity': {'required': True, 'maximum': 16, 'minimum': 1}}
    _attribute_map = {'name': {'key': 'name', 'type': 'SkuName'}, 'capacity': {'key': 'capacity', 'type': 'int'}}

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity