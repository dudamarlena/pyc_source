# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/web_server/schemas.py
# Compiled at: 2019-06-17 12:18:47
# Size of source mod 2**32: 327 bytes
import marshmallow as ma

class MessageSchema(ma.Schema):
    local_message_id = ma.fields.String()
    to = ma.fields.String()
    subject = ma.fields.String()
    date = ma.fields.DateTime()


class FullMessageSchema(MessageSchema):
    html = ma.fields.String()
    text = ma.fields.String()
    headers = ma.fields.Dict()