# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_internal_account_roles_account_role.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1InternalAccountRolesAccountRole(Model):
    """Represents an account role.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param value: Gets or sets the account role enum. Possible values include:
     'none', 'company', 'limited', 'limited_mpn', 'mpn', 'advisor',
     'advisor_with_dap', 'value_added_reseller', 'cloud_solution_provider',
     'distributor', 'incentive', 'referrals', 'basic_mpn', 'limited_basic_mpn',
     'publisher', 'control_panel_vendor', 'offboarding_cloud_solution_provider'
    :type value: str or ~microsoft.store.partnercenterservices.models.enum
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'value': {'key': 'value', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, value=None):
        super(MicrosoftPartnerSdkContractsV1InternalAccountRolesAccountRole, self).__init__()
        self.value = value
        self.attributes = None
        return