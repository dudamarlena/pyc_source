# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/data/LoginData.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 338 bytes
import bitwarden_simple_cli.models.api.LoginApi as LoginApi

class LoginData:
    username: str
    password: str

    def __init__(self, data: LoginApi):
        if data is None:
            return
        self.username = data.username
        self.password = data.password

    def __getattr__(self, item):
        return self.item