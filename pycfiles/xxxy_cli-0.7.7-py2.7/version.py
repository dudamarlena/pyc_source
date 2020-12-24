# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/version.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from russell.model.base import BaseModel

class CliVersionSchema(Schema):
    """
    Russell cli versions schema
    """
    latest_version = fields.Str()
    min_version = fields.Str()

    @post_load
    def make_credentials(self, data):
        return CliVersion(**data)


class CliVersion(BaseModel):
    """
    Latest version is the newest cli available on PIP
    Minimum version is the version below which CLI should fail
    """
    schema = CliVersionSchema(strict=True)

    def __init__(self, latest_version, min_version):
        self.latest_version = latest_version
        self.min_version = min_version