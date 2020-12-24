# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_connect_us_language.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsConnectUsLanguage(Model):
    """Represent the Connect Us Language object.

    :param iso_code: Gets or sets the ISO code.
    :type iso_code: str
    :param name: Gets or sets the name.
    :type name: str
    """
    _attribute_map = {'iso_code': {'key': 'isoCode', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}}

    def __init__(self, iso_code=None, name=None):
        super(MicrosoftPartnerSdkContractsV1ContractsConnectUsLanguage, self).__init__()
        self.iso_code = iso_code
        self.name = name