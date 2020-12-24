# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/user.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from russell.model.base import BaseModel

class UserSchema(Schema):
    uid = fields.Str()
    username = fields.Str()
    email = fields.Str()
    type = fields.Str(allow_none=True)

    @post_load
    def make_user(self, data):
        return User(**data)


class User(BaseModel):
    schema = UserSchema(strict=True)

    def __init__(self, uid, username, email, type):
        self.uid = uid
        self.username = username
        self.email = email
        self.type = type