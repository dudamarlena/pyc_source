# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_relationship_request.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1RelationshipRequest(Model):
    """Represents a relationship request. Provides the URL by which a customer can
    establish a relationship with a partner.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param url: Gets or sets the relationship request URL.
    :type url: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'url': {'key': 'url', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, url=None):
        super(MicrosoftPartnerSdkContractsV1RelationshipRequest, self).__init__()
        self.url = url
        self.attributes = None
        return