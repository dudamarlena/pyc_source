# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_common_link.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1CommonLink(Model):
    """Link represents a URI and the HTTP method which indicates the desired
    action for accessing the resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar uri: The URI.
    :vartype uri: str
    :ivar method: The method.
    :vartype method: str
    :ivar headers: Gets the link headers.
    :vartype headers:
     list[~microsoft.store.partnercenterservices.models.SystemCollectionsGenericKeyValuePairSystemStringSystemString]
    """
    _validation = {'uri': {'readonly': True}, 'method': {'readonly': True}, 'headers': {'readonly': True}}
    _attribute_map = {'uri': {'key': 'uri', 'type': 'str'}, 'method': {'key': 'method', 'type': 'str'}, 'headers': {'key': 'headers', 'type': '[SystemCollectionsGenericKeyValuePairSystemStringSystemString]'}}

    def __init__(self):
        super(MicrosoftPartnerSdkContractsV1CommonLink, self).__init__()
        self.uri = None
        self.method = None
        self.headers = None
        return