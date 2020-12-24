# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_request_attachments_info.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceRequestAttachmentsInfo(Model):
    """Represents the service request ticket attachment.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param workspace_id: Gets or sets the service Request Id
    :type workspace_id: str
    :param attachments: Gets or sets the attachments in a SR.
    :type attachments:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1FileInfo]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'workspace_id': {'key': 'workspaceId', 'type': 'str'}, 'attachments': {'key': 'attachments', 'type': '[MicrosoftPartnerSdkContractsV1FileInfo]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, workspace_id=None, attachments=None):
        super(MicrosoftPartnerSdkContractsV1ServiceRequestAttachmentsInfo, self).__init__()
        self.workspace_id = workspace_id
        self.attachments = attachments
        self.attributes = None
        return