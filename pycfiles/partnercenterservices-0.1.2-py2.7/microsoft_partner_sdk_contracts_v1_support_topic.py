# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_support_topic.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SupportTopic(Model):
    """Describes a support topic. Service requests specify a support topic to
    ensure that they are processed quickly and effectively.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param name: Gets or sets the name of the support topic.
    :type name: str
    :param description: Gets or sets the description of the support topic.
    :type description: str
    :param id: Gets or sets the unique identifier of the support topic.
    :type id: int
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'id': {'key': 'id', 'type': 'int'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, name=None, description=None, id=None):
        super(MicrosoftPartnerSdkContractsV1SupportTopic, self).__init__()
        self.name = name
        self.description = description
        self.id = id
        self.attributes = None
        return