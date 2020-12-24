# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/credentials.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from russell.model.base import BaseModel

class CredentialsSchema(Schema):
    """
    Russell credentials schema
    """
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make_credentials(self, data):
        return Credentials(**data)


class Credentials(BaseModel):
    """
    Russell credentials consists of username and password
    """
    schema = CredentialsSchema(strict=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class SignupRequestSchema(Schema):
    """
    Russell signup schema
    """
    username = fields.Str()
    password = fields.Str()
    password_confirmation = fields.Str()
    email = fields.Str()
    invite_code = fields.Str()

    @post_load
    def make_credentials(self, data):
        return SignupRequest(**data)


class SignupRequest(BaseModel):
    """
    Russell credentials consists of username and password
    """
    schema = SignupRequestSchema(strict=True)

    def __init__(self, username, password, password_confirmation, email, invite_code=None):
        self.username = username
        self.password = password
        self.password_confirmation = password_confirmation
        self.email = email
        self.invite_code = invite_code