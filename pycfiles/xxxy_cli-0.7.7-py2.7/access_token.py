# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/access_token.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from russell.model.base import BaseModel

class AccessTokenSchema(Schema):
    username = fields.Str()
    token = fields.Str()
    expiry = fields.Number(allow_none=True)

    @post_load
    def make_access_token(self, data):
        return AccessToken(**data)


class AccessToken(BaseModel):
    schema = AccessTokenSchema(strict=True)

    def __init__(self, username, token, expiry=None):
        self.username = username
        self.token = token
        self.expiry = expiry