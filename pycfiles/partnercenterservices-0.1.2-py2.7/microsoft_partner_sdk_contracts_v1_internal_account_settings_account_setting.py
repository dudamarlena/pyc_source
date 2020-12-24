# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_internal_account_settings_account_setting.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1InternalAccountSettingsAccountSetting(Model):
    """Represents an account setting key-value pair.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param key: Gets or sets the setting key. Possible values include:
     'third_party_domain_purchases', 'public_site_purchases'
    :type key: str or ~microsoft.store.partnercenterservices.models.enum
    :param value: Gets or sets a value indicating whether the setting is
     active or not.
    :type value: bool
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'key': {'key': 'key', 'type': 'str'}, 'value': {'key': 'value', 'type': 'bool'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, key=None, value=None):
        super(MicrosoftPartnerSdkContractsV1InternalAccountSettingsAccountSetting, self).__init__()
        self.key = key
        self.value = value
        self.attributes = None
        return