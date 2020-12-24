# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_request_note.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceRequestNote(Model):
    """Describes a note attached to a service request.

    :param created_by_name: Gets or sets the name of the creator of the note.
    :type created_by_name: str
    :param created_date: Gets or sets the date and time when the note was
     created.
    :type created_date: datetime
    :param text: Gets or sets the text of the note.
    :type text: str
    :param updated_by_name: Gets or sets the name of the updated user of the
     note.
    :type updated_by_name: str
    """
    _attribute_map = {'created_by_name': {'key': 'createdByName', 'type': 'str'}, 'created_date': {'key': 'createdDate', 'type': 'iso-8601'}, 'text': {'key': 'text', 'type': 'str'}, 'updated_by_name': {'key': 'updatedByName', 'type': 'str'}}

    def __init__(self, created_by_name=None, created_date=None, text=None, updated_by_name=None):
        super(MicrosoftPartnerSdkContractsV1ServiceRequestNote, self).__init__()
        self.created_by_name = created_by_name
        self.created_date = created_date
        self.text = text
        self.updated_by_name = updated_by_name