# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_authorization_claims.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1AuthorizationClaims(Model):
    """Represent the authorization claims.

    :param account_id: Gets or sets the account id.
    :type account_id: str
    :param account_type: Gets or sets the account type (ex. Tenant,
     PartnerLocation, PartnerGlobal).
    :type account_type: str
    :param account_roles: Gets or sets the account roles for the above
     account.
    :type account_roles: list[str]
    :param user_roles: Gets or sets the applicable user roles for the above
     account and the user in context.
    :type user_roles: list[str]
    """
    _attribute_map = {'account_id': {'key': 'accountId', 'type': 'str'}, 'account_type': {'key': 'accountType', 'type': 'str'}, 'account_roles': {'key': 'accountRoles', 'type': '[str]'}, 'user_roles': {'key': 'userRoles', 'type': '[str]'}}

    def __init__(self, account_id=None, account_type=None, account_roles=None, user_roles=None):
        super(MicrosoftPartnerSdkContractsV1AuthorizationClaims, self).__init__()
        self.account_id = account_id
        self.account_type = account_type
        self.account_roles = account_roles
        self.user_roles = user_roles