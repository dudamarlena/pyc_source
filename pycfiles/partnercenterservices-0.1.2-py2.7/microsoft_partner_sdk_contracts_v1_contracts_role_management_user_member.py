# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_role_management_user_member.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsRoleManagementUserMember(Model):
    """Describes a user's member information.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param display_name: Gets or sets the display name for the user.
    :type display_name: str
    :param user_principal_name: Gets or sets the name of the user principal.
    :type user_principal_name: str
    :param role_id: The identifier of the user's role.
    :type role_id: str
    :param id: The identifier of the member.
    :type id: str
    :param account_id: Gets or sets the account id where role assignment is
     tied.
    :type account_id: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'display_name': {'key': 'displayName', 'type': 'str'}, 'user_principal_name': {'key': 'userPrincipalName', 'type': 'str'}, 'role_id': {'key': 'roleId', 'type': 'str'}, 'id': {'key': 'id', 'type': 'str'}, 'account_id': {'key': 'accountId', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, display_name=None, user_principal_name=None, role_id=None, id=None, account_id=None):
        super(MicrosoftPartnerSdkContractsV1ContractsRoleManagementUserMember, self).__init__()
        self.display_name = display_name
        self.user_principal_name = user_principal_name
        self.role_id = role_id
        self.id = id
        self.account_id = account_id
        self.attributes = None
        return