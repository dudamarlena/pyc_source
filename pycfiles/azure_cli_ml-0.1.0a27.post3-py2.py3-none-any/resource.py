# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\resource.py
# Compiled at: 2017-09-20 13:50:34
from msrest.serialization import Model

class Resource(Model):
    """ARM resource envelope.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Specifies the resource ID.
    :vartype id: str
    :ivar name: Specifies the name of the resource.
    :vartype name: str
    :param location: Specifies the location of the resource.
    :type location: str
    :ivar type: Specifies the type of the resource.
    :vartype type: str
    :param tags: Contains resource tags defined as key/value pairs.
    :type tags: dict
    :param sku: The SKU of Model Management Account
    :type sku: :class:`Sku <modelmanagementaccounts.models.Sku>`
    """
    _validation = {'id': {'readonly': True}, 'name': {'readonly': True}, 'type': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'location': {'key': 'location', 'type': 'str'}, 'type': {'key': 'type', 'type': 'str'}, 'tags': {'key': 'tags', 'type': '{str}'}, 'sku': {'key': 'sku', 'type': 'Sku'}}

    def __init__(self, location=None, tags=None, sku=None):
        self.id = None
        self.name = None
        self.location = location
        self.type = None
        self.tags = tags
        self.sku = sku
        return