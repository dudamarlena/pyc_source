# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/web_server/message_util.py
# Compiled at: 2019-06-17 12:18:47
# Size of source mod 2**32: 1015 bytes
from mailbox import MaildirMessage
from typing import Collection
from typing import Type
import marshmallow as ma
from mailparser import mailparser
from .message import Message

class MessageUtil:

    @classmethod
    def to_dict(cls, message: Message, schema: Type[ma.Schema]) -> dict:
        return schema().dump(message)

    @classmethod
    def to_json(cls, message: Message, schema: Type[ma.Schema]) -> str:
        return schema().dumps(message)

    @classmethod
    def to_dict_many(cls, emails: Collection[Message], schema: Type[ma.Schema]) -> dict:
        return schema(many=True).dump(emails)

    @classmethod
    def to_json_many(cls, emails: Collection[Message], schema: Type[ma.Schema]) -> str:
        return schema(many=True).dumps(emails)

    @classmethod
    def parse_message(cls, local_message_id: str, message: MaildirMessage) -> Message:
        obj = mailparser.parse_from_string(message.as_string())
        return Message.from_mailparser(local_message_id=local_message_id, obj=obj)