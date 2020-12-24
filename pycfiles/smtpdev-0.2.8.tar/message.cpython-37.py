# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/web_server/message.py
# Compiled at: 2019-06-18 09:28:15
# Size of source mod 2**32: 1134 bytes
from __future__ import annotations
import datetime as dt
from dataclasses import dataclass
from mailparser import MailParser
SEEN = 'S'

@dataclass
class Message:
    local_message_id: 'str'
    to: 'str'
    subject: 'str'
    date: 'dt.datetime'
    html: 'str'
    text: 'str'
    headers: 'dict'
    is_new: 'bool'

    @classmethod
    def from_mailparser(cls, local_message_id: 'str', obj: 'MailParser') -> 'Message':
        flags = obj.flags
        return Message(local_message_id=local_message_id,
          to=(cls._format_to(obj)),
          subject=(obj.subject),
          date=(obj.date),
          html=(cls._format_html(obj)),
          text=(cls._format_text(obj)),
          headers=(obj.headers),
          is_new=(SEEN in flags))

    @staticmethod
    def _format_to(obj):
        to = ', '.join([' '.join([i for i in x if i]) for x in obj.to])
        return to or obj.headers.get('X-RcptTo', '')

    @staticmethod
    def _format_html(obj):
        if obj.text_html:
            return obj.text_html[0]
        return ''

    @staticmethod
    def _format_text(obj):
        if obj.text_plain:
            return obj.text_plain[0]
        return ''