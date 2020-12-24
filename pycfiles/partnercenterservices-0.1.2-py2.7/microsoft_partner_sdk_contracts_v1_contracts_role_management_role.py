# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_role_management_role.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsRoleManagementRole(Model):
    """Represents a role object used as a contract for role operations.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param name: Gets or sets the name of the role.
    :type name: str
    :param id: Gets or sets the id of the role.
    :type id: str
    :param category: Gets or sets the category of the role. Possible values
     include: 'tenant', 'partner_agent', 'incentive', 'mpn', 'marketing',
     'referrals', 'account_admin'
    :type category: str or ~microsoft.store.partnercenterservices.models.enum
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'id': {'key': 'id', 'type': 'str'}, 'category': {'key': 'category', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, name=None, id=None, category=None, links=None):
        super(MicrosoftPartnerSdkContractsV1ContractsRoleManagementRole, self).__init__()
        self.name = name
        self.id = id
        self.category = category
        self.links = links
        self.attributes = None
        return