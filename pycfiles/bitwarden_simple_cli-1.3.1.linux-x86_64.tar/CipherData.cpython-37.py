# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/data/CipherData.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1171 bytes
import bitwarden_simple_cli.enums.CipherType as CipherType
import bitwarden_simple_cli.models.data.FieldData as FieldData
import bitwarden_simple_cli.models.data.LoginData as LoginData
import bitwarden_simple_cli.models.response.CipherResponse as CipherResponse

class CipherData:
    collectionIds: []
    fields: []
    id: str
    login: LoginData
    organizationId: str
    type: CipherType
    userId: str

    def __init(self, response: CipherResponse, user_id: str, collection_ids: []):
        if response is None:
            return
        else:
            self.id = response.id
            self.organizationId = response.organizationId
            self.type = CipherType(int(response.type))
            self.userId = user_id
            if collection_ids:
                self.collectionIds = collection_ids
            else:
                self.collectionIds = response.collectionsIds
        if self.type == CipherType.Login:
            self.login = LoginData(response.login)
        if response.fields:
            self.fields = []
            for field in response.fields:
                self.fields.append(FieldData(field))

    def __getattr__(self, item):
        return self.item