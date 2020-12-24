# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/model/service.py
# Compiled at: 2018-12-27 05:19:41
from marshmallow import Schema, fields, post_load
from russell.model.base import BaseModel

class ServiceSchema(Schema):
    """
    Russell cloud service schema
    """
    service_status = fields.Int()

    @post_load
    def make_credentials(self, data):
        return Service(**data)


class Service(BaseModel):
    """
    Service status for russell cloud
    """
    schema = ServiceSchema(strict=True)

    def __init__(self, service_status):
        self.service_status = service_status