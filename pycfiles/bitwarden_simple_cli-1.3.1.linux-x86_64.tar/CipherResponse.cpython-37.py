# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/response/CipherResponse.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 999 bytes
import bitwarden_simple_cli.models.api.LoginApi as LoginApi
import bitwarden_simple_cli.models.api.FieldApi as FieldApi
import bitwarden_simple_cli.models.response.BaseResponse as BaseResponse

class CipherResponse(BaseResponse):
    collectionsIds = None
    id = None
    name = None
    organizationId = None
    type = None

    def __init__(self, response):
        super().__init__(response)
        self.collectionIds = self.get_response_property_name('CollectionIds')
        self.name = self.get_response_property_name('Name')
        self.id = self.get_response_property_name('Id')
        self.organizationId = self.get_response_property_name('OrganizationId')
        self.type = self.get_response_property_name('Type')
        login = self.get_response_property_name('Login')
        if login:
            self.login = LoginApi(login)
        fields = self.get_response_property_name('Fields')
        if fields:
            self.fields = [FieldApi(field) for field in fields]