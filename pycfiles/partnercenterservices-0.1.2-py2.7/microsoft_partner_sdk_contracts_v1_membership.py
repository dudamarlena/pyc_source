# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_membership.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1Membership(Model):
    """Represents a membership object used as a contract for an object's
    membership.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param role_id: Gets or sets the id of the role.
    :type role_id: str
    :param member_id: Gets or sets the id of the member object.
    :type member_id: str
    :param account_id: Gets or sets the account id where role assignment is
     tied.
    :type account_id: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'role_id': {'key': 'roleId', 'type': 'str'}, 'member_id': {'key': 'memberId', 'type': 'str'}, 'account_id': {'key': 'accountId', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, role_id=None, member_id=None, account_id=None):
        super(MicrosoftPartnerSdkContractsV1Membership, self).__init__()
        self.role_id = role_id
        self.member_id = member_id
        self.account_id = account_id
        self.attributes = None
        return