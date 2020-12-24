# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\message\builder.py
# Compiled at: 2018-05-16 03:48:33
# Size of source mod 2**32: 1567 bytes
import time
from wechat.utils import serialize_dict_to_xml
from .models import XMLMessage

def _build_reply_msg_bytes(receive_message, **kwrags):
    unicode_msg = serialize_dict_to_xml(ToUserName=receive_message.FromUserName, 
     FromUserName=receive_message.ToUserName, 
     CreateTime=int(time.time()), **kwrags)
    return unicode_msg.encode('utf-8')


class XMLMessageBuilder(object):

    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def parse(raw_xml):
        return XMLMessage(raw_xml)

    @staticmethod
    def build_reply_textmsg_for(message, content):
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        return _build_reply_msg_bytes(message,
          MsgType='text',
          Content=content)

    @staticmethod
    def build_reply_imgmsg_for(message, media_id):
        raise NotImplementedError()

    @staticmethod
    def build_reply_voicemsg_for(message, media_id):
        raise NotImplementedError()

    @staticmethod
    def build_reply_videomsg_for(message, media_id, title=None, description=None):
        raise NotImplementedError()

    @staticmethod
    def build_reply_musicmsg_for(message, media_id, title=None, music_url=None, description=None, hqmusic_url=None):
        raise NotImplementedError()

    @staticmethod
    def build_reply_newsmsg_for(message, articles):
        raise NotImplementedError()