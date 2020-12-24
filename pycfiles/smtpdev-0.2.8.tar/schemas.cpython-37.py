# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/web_server/schemas.py
# Compiled at: 2019-12-13 02:25:27
# Size of source mod 2**32: 360 bytes
import marshmallow as ma

class MessageSchema(ma.Schema):
    local_message_id = ma.fields.String()
    to = ma.fields.String()
    subject = ma.fields.String()
    date = ma.fields.DateTime()
    is_new = ma.fields.Boolean()


class FullMessageSchema(MessageSchema):
    html = ma.fields.String()
    text = ma.fields.String()
    headers = ma.fields.Dict()