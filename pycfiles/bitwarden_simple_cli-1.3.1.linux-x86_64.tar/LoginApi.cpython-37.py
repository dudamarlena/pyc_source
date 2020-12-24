# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/api/LoginApi.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 385 bytes
import bitwarden_simple_cli.models.response.BaseResponse as BaseResponse

class LoginApi(BaseResponse):
    username: str
    password: str

    def __init__(self, data):
        super().__init__(data)
        if data is None:
            return
        self.username = self.get_response_property_name('Username')
        self.password = self.get_response_property_name('Password')