# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\mms_update_props.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class ModelManagementAccountUpdateProperties(Model):
    """The payload for patching the Model Management Account.

    :param tags: Contains resource tags defined as key/value pairs.
    :type tags: dict
    :param sku: The SKU of Model Management Account
    :type sku: :class:`Sku <modelmanagementaccounts.models.Sku>`
    :param description: The description of the Model Management Account.
    :type description: str
    """
    _attribute_map = {'tags': {'key': 'tags', 'type': '{str}'}, 'sku': {'key': 'sku', 'type': 'Sku'}, 'description': {'key': 'properties.description', 'type': 'str'}}

    def __init__(self, tags=None, sku=None, description=None):
        self.tags = tags
        self.sku = sku
        self.description = description