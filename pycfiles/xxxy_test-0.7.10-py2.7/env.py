# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/env.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from floyd.model.base import BaseModel

class EnvSchema(Schema):
    arch = fields.Str()
    name = fields.Str()
    image = fields.Str()

    @post_load
    def make_env(self, data):
        return Env(**data)


class Env(BaseModel):
    schema = EnvSchema(strict=True)

    def __init__(self, arch, name, image):
        self.name = name
        self.image = image
        self.arch = arch