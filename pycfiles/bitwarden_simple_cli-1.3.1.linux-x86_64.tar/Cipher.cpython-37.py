# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/Cipher.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 2634 bytes
import bitwarden_simple_cli.models.data.CipherData as CipherData
from bitwarden_simple_cli.models.domain.DomainBase import Domain
import bitwarden_simple_cli.models.domain.Field as Field
import bitwarden_simple_cli.enums.CipherType as CipherType
import bitwarden_simple_cli.models.domain.Login as Login
import bitwarden_simple_cli.exceptions.ManagedException as ManagedException

class Cipher(Domain):
    id = None
    fields = None
    login = None
    folderId = None
    name = None
    response = None
    type: CipherType
    userId = None
    organizationId = None

    def __init__(self, obj, already_encrypted=False, local_data=None):
        super().__init__()
        if obj is None:
            return
        self.build_domain_model(self, obj, {'id':None, 
         'userId':None, 
         'organizationId':None, 
         'folderId':None, 
         'name':None, 
         'notes':None}, already_encrypted, [
         'id',
         'userId',
         'organizationId',
         'folderId'])
        self.type = CipherType(int(obj['type']))
        if self.type == CipherType.Login:
            self.login = Login(obj['login'], already_encrypted)
        if obj.get('fields'):
            self.fields = []
            for field in obj['fields']:
                self.fields.append(Field(field, already_encrypted))

    def decrypt_field(self, field):
        if field in ('name', 'notes'):
            return self.__getattribute__(field).decrypt(self.organizationId)
        if field in ('username', 'password'):
            return self.login.decrypt_field(field, self.organizationId)
        if field == 'uri':
            return self.login.decrypt_uri(self.organizationId, 1)
        if field == 'uris':
            return [self.login.decrypt_uri(self.organizationId, i) for i in range(1, len(self.login.uris) + 1)]
        if len(self.fields) > 0:
            for custom_field in self.fields:
                if str(custom_field.name.decrypt(self.organizationId), 'utf-8') == field:
                    return custom_field.value.decrypt(self.organizationId)

            raise ManagedException('Unable to find field %s for entry with id: %s' % (field, self.id))