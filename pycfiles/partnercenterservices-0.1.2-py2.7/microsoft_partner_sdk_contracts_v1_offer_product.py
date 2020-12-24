# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_offer_product.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1OfferProduct(Model):
    """Summarizes an offer's product.
    A product or service created by Microsoft. In some cases, the product may
    be created by
    a third party and listed in a catalog by Microsoft. A product may have more
    than one
    offer associated with it, each with different sets of features and targeted
    at different customer needs.

    :param id: Gets or sets the product identifier.
    :type id: str
    :param name: Gets or sets the product name.
    :type name: str
    :param unit: Gets or sets the product unit.
    :type unit: str
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'unit': {'key': 'unit', 'type': 'str'}}

    def __init__(self, id=None, name=None, unit=None):
        super(MicrosoftPartnerSdkContractsV1OfferProduct, self).__init__()
        self.id = id
        self.name = name
        self.unit = unit