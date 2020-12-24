# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_mpn_profile.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1MpnProfile(Model):
    """Describes a partner's Microsoft Partner Network profile.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param partner_name: Gets or sets the company or organization name.
    :type partner_name: str
    :param mpn_id: Gets or sets the Microsoft Partner Network ID.
    :type mpn_id: str
    :ivar profile_type: Gets the partner profile type. Possible values
     include: 'mpn_profile', 'billing_profile', 'support_profile',
     'legal_business_profile', 'organization_profile'
    :vartype profile_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'profile_type': {'readonly': True}, 'attributes': {'readonly': True}}
    _attribute_map = {'partner_name': {'key': 'partnerName', 'type': 'str'}, 'mpn_id': {'key': 'mpnId', 'type': 'str'}, 'profile_type': {'key': 'profileType', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, partner_name=None, mpn_id=None, links=None):
        super(MicrosoftPartnerSdkContractsV1MpnProfile, self).__init__()
        self.partner_name = partner_name
        self.mpn_id = mpn_id
        self.profile_type = None
        self.links = links
        self.attributes = None
        return