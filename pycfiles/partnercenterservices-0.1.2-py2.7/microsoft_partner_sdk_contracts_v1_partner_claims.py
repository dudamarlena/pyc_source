# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_claims.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerClaims(Model):
    """Represents a set of claims for the partner principal, the primary ones
    being the partner type and the authorization roles.

    :param authorization_claims: Gets or sets the applicable authorization
     claims (the account roles and user roles for each of the accounts in the
     connected account system).
    :type authorization_claims:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1AuthorizationClaims]
    :param cloud_instance_name: Gets or sets the national cloud instance name
     (ex. Global, China, Germany, UnitedStatesGovernment etc.).
    :type cloud_instance_name: str
    :param graph_access_token: Gets or sets the graph access token.
    :type graph_access_token: str
    :param is_incomplete: Gets or sets a value indicating whether the
     authorization claims list is incomplete or not.
    :type is_incomplete: bool
    """
    _attribute_map = {'authorization_claims': {'key': 'authorizationClaims', 'type': '[MicrosoftPartnerSdkContractsV1AuthorizationClaims]'}, 'cloud_instance_name': {'key': 'cloudInstanceName', 'type': 'str'}, 'graph_access_token': {'key': 'graphAccessToken', 'type': 'str'}, 'is_incomplete': {'key': 'isIncomplete', 'type': 'bool'}}

    def __init__(self, authorization_claims=None, cloud_instance_name=None, graph_access_token=None, is_incomplete=None):
        super(MicrosoftPartnerSdkContractsV1PartnerClaims, self).__init__()
        self.authorization_claims = authorization_claims
        self.cloud_instance_name = cloud_instance_name
        self.graph_access_token = graph_access_token
        self.is_incomplete = is_incomplete