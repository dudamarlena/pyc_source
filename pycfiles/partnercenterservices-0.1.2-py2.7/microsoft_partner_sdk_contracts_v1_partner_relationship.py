# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_relationship.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerRelationship(Model):
    """Represents a relationship between two partners.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Gets or sets the partner identifier.
     the partner identifier specifies the tenant ID of the partner who is
     in the recipient (from) side of the partner relationship.
    :type id: str
    :param name: Gets or sets the name of the friendly.
    :type name: str
    :param relationship_type: Gets or sets the type of relationship. Possible
     values include: 'none', 'is_indirect_reseller_of',
     'is_indirect_cloud_solution_provider_of'
    :type relationship_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param state: Gets or sets the state of the relationship. (Example :
     "active")
    :type state: str
    :param mpn_id: Gets or sets the Microsoft Partner Network (MPN) identifier
     of the partner.
    :type mpn_id: str
    :param location: Gets or sets the location of the partner.
    :type location: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'relationship_type': {'key': 'relationshipType', 'type': 'str'}, 'state': {'key': 'state', 'type': 'str'}, 'mpn_id': {'key': 'mpnId', 'type': 'str'}, 'location': {'key': 'location', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, id=None, name=None, relationship_type=None, state=None, mpn_id=None, location=None):
        super(MicrosoftPartnerSdkContractsV1PartnerRelationship, self).__init__()
        self.id = id
        self.name = name
        self.relationship_type = relationship_type
        self.state = state
        self.mpn_id = mpn_id
        self.location = location
        self.attributes = None
        return